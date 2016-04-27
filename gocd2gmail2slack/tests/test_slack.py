
import ast
import unittest

import responses

from slack import (
    send_to_slack,
    is_matching_send_rule,
    get_pipeline_url,
    message_builder,
)

TEST_WEBHOOK_URL = 'https://web.hook.url/123/456'
TEST_GOCD_DASHBOARD_URL = 'http://domain:port/go'

TEST_CI_STAGES = ['Build', 'Test', 'Unit', 'Package']

TEST_DEPLOY_STAGES = ['Deploy', 'Default', 'defaultStage',
                      'DeployAll', 'DeployEU', 'deploy-eu']


class SlackIncomingWebhookTests(unittest.TestCase):

    @responses.activate
    def test_calling_correct_webhook_url(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('body', TEST_WEBHOOK_URL)
        self.assertEqual(TEST_WEBHOOK_URL, responses.calls[0].request.url)

    @responses.activate
    def test_sending_correct_payload(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        expected = {'username': 'user', 'text': 'abc'}
        send_to_slack(expected, TEST_WEBHOOK_URL)
        self.assertDictEqual(expected, ast.literal_eval(responses.calls[0].request.body))


class MessageBuilderTests(unittest.TestCase):

    @staticmethod
    def factory(pipeline='pipe1', stage='stage1', status='status1',
                changeset={'id': '12345', 'url': 'http://url',
                           'author': 'anon', 'comment': 'fixed'},
                dashboard_url='http://dash'):

        return {'gocd_details': {'pipeline': pipeline,
                                 'stage': stage, 'status': status},

                'changeset': changeset, 'dashboard_url': dashboard_url}

    def test_tick_icon_for_passing_build(self):
        params = self.factory(stage='package', status='passed')
        body = message_builder(**params)
        self.assertEqual(':white_check_mark:', body['icon_emoji'])

    def test_tick_icon_for_fixed_build(self):
        params = self.factory(stage='package', status='is fixed')
        body = message_builder(**params)
        self.assertEqual(':white_check_mark:', body['icon_emoji'])

    def test_x_icon_for_failing_build(self):
        params = self.factory(stage='package', status='failed')
        body = message_builder(**params)
        self.assertEqual(':x:', body['icon_emoji'])

    def test_x_icon_for_broken_build(self):
        params = self.factory(stage='package', status='is broken')
        body = message_builder(**params)
        self.assertEqual(':x:', body['icon_emoji'])

    def test_include_changeset_for_ci_stages(self):
        for stage in TEST_CI_STAGES:
            params = self.factory(stage=stage, status='passed')
            body = message_builder(**params)
            self.assertIn('Changeset:', body['text'])

    def test_exclude_changeset_for_deploy_stages(self):
        for stage in TEST_DEPLOY_STAGES:
            params = self.factory(stage=stage, status='passed')
            body = message_builder(**params)
            self.assertNotIn('Changeset:', body['text'])

    def test_include_stage_for_failing_builds(self):
        params = self.factory(status='failed')
        body = message_builder(**params)
        self.assertIn('Stage:', body['text'])

    def test_include_stage_for_broken_builds(self):
        params = self.factory(status='is broken')
        body = message_builder(**params)
        self.assertIn('Stage:', body['text'])

    def test_exclude_stage_for_passing_builds(self):
        params = self.factory(status='passed')
        body = message_builder(**params)
        self.assertNotIn('Stage:', body['text'])


class SlackSendingRuleTests(unittest.TestCase):

    @staticmethod
    def factory(pipeline='pipe1', stage='stage1', status='status1'):
        return {'pipeline': pipeline, 'stage': stage, 'status': status}

    def test_all_failed_builds_are_sent_regardless_of_stage(self):
        for stage in TEST_CI_STAGES + TEST_DEPLOY_STAGES:
            details = self.factory(stage=stage, status='failed')
            self.assertTrue(is_matching_send_rule(details))

    def test_all_broken_builds_are_sent_regardless_of_stage(self):
        for stage in TEST_CI_STAGES + TEST_DEPLOY_STAGES:
            details = self.factory(stage=stage, status='is broken')
            self.assertTrue(is_matching_send_rule(details))

    def test_list_of_allowed_passing_build_stage(self):
        for stage in ['Package'] + TEST_DEPLOY_STAGES:
            details = self.factory(stage=stage, status='passed')
            self.assertTrue(is_matching_send_rule(details))

    def test_list_of_allowed_fixed_build_stage(self):
        for stage in ['Package'] + TEST_DEPLOY_STAGES:
            details = self.factory(stage=stage, status='is fixed')
            self.assertTrue(is_matching_send_rule(details))

    def test_list_of_ignored_passing_build_stage(self):
        for stage in ['Build', 'Test', 'Unit']:
            details = self.factory(stage=stage, status='passed')
            self.assertFalse(is_matching_send_rule(details))

    def test_unknown_build_status(self):
        for status in ['unknown', 'error']:
            details = self.factory(status=status)
            self.assertFalse(is_matching_send_rule(details))


class SlackPipelineUrlBuilder(unittest.TestCase):

    def test_build_url_1(self):
        pipeline = 'product.branch.action.environment'
        expected = TEST_GOCD_DASHBOARD_URL + '/tab/pipeline/history/' + pipeline
        self.assertEqual(expected, get_pipeline_url(TEST_GOCD_DASHBOARD_URL, pipeline))
