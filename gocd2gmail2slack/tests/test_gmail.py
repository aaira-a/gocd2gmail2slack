
import unittest

from ..gmail import (
    get_label_id,
    query_builder,
)

from ..fixtures.gmail_labels import LABELS


class LabelTests(unittest.TestCase):

    def test_get_labels_id_by_name_returns_id(self):
        actual = get_label_id('GOCD_PATTERN', LABELS)
        self.assertEqual('Label_2', actual)


class MessageQueryBuilderTests(unittest.TestCase):

    def test_single_include_label(self):
        actual = query_builder(include_labels=['Label_1'])
        self.assertEqual('label:Label_1', actual)

    def test_two_include_labels(self):
        actual = query_builder(include_labels=['Label_1', 'Label_2'])
        self.assertEqual('label:Label_1 label:Label_2', actual)

    def test_single_exclude_label(self):
        actual = query_builder(exclude_labels=['Label_1'])
        self.assertEqual('-label:Label_1', actual)

    def test_two_exclude_labels(self):
        actual = query_builder(exclude_labels=['Label_1', 'Label_2'])
        self.assertEqual('-label:Label_1 -label:Label_2', actual)
