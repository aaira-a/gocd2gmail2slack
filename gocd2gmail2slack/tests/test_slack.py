
import unittest

import responses

from ..slack import (
    send_to_slack,
    is_matching_send_rule,
)

TEST_WEBHOOK_URL = 'https://web.hook.url/123/456'


class SlackIncomingWebhookTests(unittest.TestCase):

    @responses.activate
    def test_calling_correct_webhook_url(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'passed', TEST_WEBHOOK_URL)
        self.assertEqual(TEST_WEBHOOK_URL, responses.calls[0].request.url)

    @responses.activate
    def test_tick_icon_for_passing_build(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'passed', TEST_WEBHOOK_URL)
        expected = """icon_emoji": ":white_check_mark:"""
        self.assertIn(expected, responses.calls[0].request.body)

    @responses.activate
    def test_x_icon_for_failing_build(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'failed', TEST_WEBHOOK_URL)
        expected = """icon_emoji": ":x:"""
        self.assertIn(expected, responses.calls[0].request.body)

    @responses.activate
    def test_no_sending_for_other_status(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'error', TEST_WEBHOOK_URL)
        self.assertEqual(0, len(responses.calls))


class SlackSendingRuleTests(unittest.TestCase):

    def factory(pipeline='pipe1', stage='stage1', status='status1'):
        return {'pipeline': pipeline, 'stage': stage, 'status': status}

    def test_all_failed_builds_are_sent_regardless_of_stage(self):
        details = self.factory(status='failed')
        self.assertTrue(is_matching_send_rule(details))

    def test_list_of_allowed_passing_build_stage(self):
        for stage in ['Package', 'Deploy', 'Default', 'defaultStage']:
            details = self.factory(stage=stage, status='passed')
            self.assertTrue(is_matching_send_rule(details))

    def test_list_of_ignored_passing_build_stage(self):
        for stage in ['Build', 'Test', 'Unit']:
            details = self.factory(stage=stage, status='passed')
            self.assertFalse(is_matching_send_rule(details))
