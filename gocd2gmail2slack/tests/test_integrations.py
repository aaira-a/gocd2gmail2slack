
import ast
import unittest
from unittest.mock import patch

from integrations import (
    initialize,
    process,
)

from fixtures.gmail_labels import LABELS
from fixtures.gmail_message_detail_1 import MESSAGE1


@patch('integrations.gm')
class GmailInitializerIntegrationsTests(unittest.TestCase):

    def test_gmail_service_is_initiated(self, mock):
        initialize()
        self.assertEqual(1, mock.get_service.call_count)

    def test_get_all_labels(self, mock):
        initialize()
        self.assertEqual(1, mock.get_labels.call_count)

    def test_get_initial_emails_with_unread_label(self, mock):
        initialize()
        expected_argument = {'include_labels': ['UNREAD']}
        self.assertIn(expected_argument, mock.get_messages.call_args)

    def test_get_message_details_from_initial_emails(self, mock):
        initialize()
        self.assertEqual(1, mock.get_messages_details.call_count)


@patch('integrations.slack.send_to_slack')
@patch('integrations.gm')
class ProcessingIntegrationsTests(unittest.TestCase):

    def setUp(self):
        self.messages_details = [MESSAGE1]
        self.labels = LABELS

    def test_unread_label_is_removed_after_processing(self,
                                                      mock_gm, mock_slack):
        process('service', LABELS, self.messages_details)
        expected = 'UNREAD'
        self.assertIn(expected, mock_gm.remove_label.call_args[0])

    def test_sent_slack_label_is_added_after_processing(self,
                                                        mock_gm, mock_slack):
        process('service', LABELS, self.messages_details)
        expected = 'SENT_TO_SLACK'
        self.assertIn(expected, mock_gm.add_label.call_args[0])

    def test_data_extraction_complete_and_sent_to_slack(self,
                                                        mock_gm, mock_slack):
        process('service', LABELS, self.messages_details)
        self.assertEqual(1, mock_slack.call_count)
