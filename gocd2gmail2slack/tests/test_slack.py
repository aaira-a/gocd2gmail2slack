
import ast
import unittest

import responses

from gocd2gmail2slack.slack import (
    send_to_slack,
    is_matching_send_rule,
    get_pipeline_url,
    message_builder,
)

TEST_WEBHOOK_URL = 'https://web.hook.url/123/456'
TEST_GOCD_DASHBOARD_URL = 'http://domain:port/go'


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

    def test_tick_icon_for_passing_build(self):
        body = message_builder('', 'package', 'passed', '', '', '')
        self.assertEqual(':white_check_mark:', body['icon_emoji'])

    def test_tick_icon_for_fixed_build(self):
        body = message_builder('', 'package', 'is fixed', '', '', '')
        self.assertEqual(':white_check_mark:', body['icon_emoji'])

    def test_x_icon_for_failing_build(self):
        body = message_builder('', 'package', 'failed', '', '', '')
        self.assertEqual(':x:', body['icon_emoji'])


class SlackSendingRuleTests(unittest.TestCase):

    def factory(pipeline='pipe1', stage='stage1', status='status1'):
        return {'pipeline': pipeline, 'stage': stage, 'status': status}

    def test_all_failed_builds_are_sent_regardless_of_stage(self):
        for stage in ['Package', 'Deploy', 'Default', 'defaultStage', 'DeployAll']:
            details = self.factory(stage=stage, status='failed')
            self.assertTrue(is_matching_send_rule(details))

    def test_list_of_allowed_passing_build_stage(self):
        for stage in ['Package', 'Deploy', 'Default', 'defaultStage', 'DeployAll']:
            details = self.factory(stage=stage, status='passed')
            self.assertTrue(is_matching_send_rule(details))

    def test_list_of_allowed_fixed_build_stage(self):
        for stage in ['Package', 'Deploy', 'Default', 'defaultStage', 'DeployAll']:
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
