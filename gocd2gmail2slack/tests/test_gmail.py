
import unittest

from ..gmail import get_label_id
from ..fixtures.gmail_labels import LABELS


class GmailLabelTests(unittest.TestCase):

    def test_get_labels_id_by_name_returns_id(self):
        actual = get_label_id('GOCD_PATTERN', LABELS)
        self.assertEqual('Label_2', actual)
