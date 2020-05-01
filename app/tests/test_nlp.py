#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon NLP Analyzer tests
"""

from app.modules.nlp import NlProcess
import unittest


class TestNlProcess(unittest.TestCase):

    def setUp(self):
        self.nlp_ = NlProcess('test corpus')
        self.nlp_.get_corpus()

    def test_get_title(self):
        # Check point 1:
        # As the ref is not digit,
        # the title should be the ref itself.
        # Check that.
        self.assertEqual(self.nlp_.title, 'test corpus')

    def test_get_ner(self):
        # Check point 2:
        # Are the appropriate filtering jobs done
        # and the data frame generated?
        # If so, is the expected first entity returned?
        self.assertEqual(self.nlp_.ner['labels'][0], 'lr')

    def test_get_nouns(self):
        # Check point 3:
        # Are the appropriate filtering jobs done
        # and the data frame generated?
        # If so, is the expected first noun returned?
        self.assertEqual(self.nlp_.nouns['labels'][0], 'smic')
