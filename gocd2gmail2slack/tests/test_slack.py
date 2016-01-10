
import unittest

import responses

import gocd2gmail2slack.slack

from ..slack import (
    send_to_slack,
)


TEST_WEBHOOK_URL = 'https://web.hook.url/123/456'


class SlackIncomingWebhookTests(unittest.TestCase):

    def setUp(self):
        gocd2gmail2slack.slack.WEBHOOK_URL = TEST_WEBHOOK_URL

    @responses.activate
    def test_calling_correct_webhook_url(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'passed')
        self.assertEqual(TEST_WEBHOOK_URL, responses.calls[0].request.url)

    @responses.activate
    def test_tick_icon_for_passing_build(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'passed')
        expected = """icon_emoji": ":white_check_mark:"""
        self.assertIn(expected, responses.calls[0].request.body)

    @responses.activate
    def test_x_icon_for_failing_build(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'failed')
        expected = """icon_emoji": ":x:"""
        self.assertIn(expected, responses.calls[0].request.body)

    @responses.activate
    def test_no_sending_for_other_status(self):
        responses.add(responses.POST, TEST_WEBHOOK_URL)
        send_to_slack('pipeline1', 'package', 'unknown')
        self.assertEqual(0, len(responses.calls))
