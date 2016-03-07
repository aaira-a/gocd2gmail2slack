
import ast
import unittest
from unittest.mock import patch

import integrations

from fixtures.gmail_labels import LABELS
from fixtures.gmail_message_detail_1 import MESSAGE1


integrations.WEBHOOK_URL = 'http://hook.url'
integrations.GOCD_DASHBOARD_URL = 'http://dash.url'


@patch('integrations.gm')
class GmailInitializerIntegrationsTests(unittest.TestCase):

    def test_gmail_service_is_initiated(self, mock):
        integrations.initialize()
        self.assertEqual(1, mock.get_service.call_count)

    def test_get_all_labels(self, mock):
        integrations.initialize()
        self.assertEqual(1, mock.get_labels.call_count)

    def test_get_initial_emails_with_unread_label(self, mock):
        integrations.initialize()
        expected_argument = {'include_labels': ['UNREAD']}
        self.assertIn(expected_argument, mock.get_messages.call_args)

    def test_get_message_details_from_initial_emails(self, mock):
        integrations.initialize()
        self.assertEqual(1, mock.get_messages_details.call_count)


@patch('integrations.slack.send_to_slack')
@patch('integrations.gm')
class ProcessingIntegrationsTests(unittest.TestCase):

    def setUp(self):
        self.messages_details = [MESSAGE1]
        self.labels = LABELS

    def test_unread_label_is_removed_after_processing(self,
                                                      mock_gm, mock_slack):
        integrations.process('service', LABELS, self.messages_details)
        expected = 'UNREAD'
        self.assertIn(expected, mock_gm.remove_label.call_args[0])

    def test_sent_slack_label_is_added_after_processing(self,
                                                        mock_gm, mock_slack):
        integrations.process('service', LABELS, self.messages_details)
        expected = 'SENT_TO_SLACK'
        self.assertIn(expected, mock_gm.add_label.call_args[0])

    def test_data_extraction_complete_and_sent_to_slack(self,
                                                        mock_gm, mock_slack):
        integrations.process('service', LABELS, self.messages_details)

        self.assertEqual(1, mock_slack.call_count)
        self.assertEqual('http://hook.url', mock_slack.call_args[0][1])

        expected_body = {'username': 'go build status - passed',
                         'icon_emoji': ':white_check_mark:',
                         'text': '<http://dash.url/tab/pipeline/history/product.branch.CI|product.branch.CI>\n'
                         'Changeset: '
                         '<https://code.domain.com/tfs/products/_versionControl/changeset/01234|01234> '
                         '- committer: cloud config changes'
                         }
        actual_body = ast.literal_eval(str(mock_slack.call_args[0][0]))
        self.assertDictEqual(expected_body, actual_body)
