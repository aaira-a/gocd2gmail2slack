
import unittest

from ..messages import (
    get_subject,
    is_gocd_pattern,
    get_gocd_details,
)

from ..fixtures.gmail_message_detail_1 import MESSAGE1


class MessageDetailsTests(unittest.TestCase):

    def test_get_subject(self):
        actual = get_subject(MESSAGE1)
        expected = 'FW: Stage [product.branch.CI/100/Package/1] passed'
        self.assertEqual(expected, actual)


class GocdDetailsTests(unittest.TestCase):

    def test_check_gocd_subject_pattern_valid(self):
        subjects = ['FW: Stage [proDuct.branch.CI/100/Package/1] passed',
                    'Stage [product.braNch.Deploy.Test0/212/Package/1] passed',
                    'Stage [product2.branch2.CI/10999/Package/1] failed']
        for subject in subjects:
            self.assertTrue(is_gocd_pattern(subject))

    def test_check_gocd_subject_pattern_invalid(self):
        subjects = ['FW: Stage [product.branch.CI/100/Package/1] unknown',
                    'Stage [product.branch.CI/a/Package/1] passed']
        for subject in subjects:
            self.assertFalse(is_gocd_pattern(subject))

    def test_get_gocd_details(self):
        subject = 'FW: Stage [pr0duct5.br4nch.CI/100/Package/1] passed'
        expected = {'pipeline': 'pr0duct5.br4nch.CI',
                    'stage': 'Package',
                    'status': 'passed'}
        self.assertEqual(expected, get_gocd_details(subject))
