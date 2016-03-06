
import unittest
from unittest.mock import patch

from integrations import (
    main,
    WEBHOOK_URL,
    GOCD_DASHBOARD_URL
)


@patch('integrations.gm')
class GmailIntegrationsTests(unittest.TestCase):

    def test_gmail_service_is_initiated(self, mock):
        main()
        self.assertEqual(1, mock.get_service.call_count)

    def test_get_all_labels(self, mock):
        main()
        self.assertEqual(1, mock.get_labels.call_count)

    def test_get_initial_emails_with_unread_label(self, mock):
        main()
        expected_argument = {'include_labels': ['UNREAD']}
        self.assertIn(expected_argument, mock.get_messages.call_args)

    def test_get_message_details_from_initial_emails(self, mock):
        main()
        self.assertEqual(1, mock.get_messages_details.call_count)
