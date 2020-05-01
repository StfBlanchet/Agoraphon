#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon Topic getter functional tests
"""

from app.modules.search import TopicSeeker
import unittest


class TestTopicSeeker(unittest.TestCase):

    def setUp(self):
        self.q_1 = TopicSeeker('raoult')
        self.q_2 = TopicSeeker('politique')
        self.q_3 = TopicSeeker('grtyukjl')

    def test_switch_1(self):
        # The user opts for the open search "raoult".
        # Check the search term is the expected one.
        self.q_1.switch()
        self.assertEqual(self.q_1.search, '"raoult"')

    def test_switch_2(self):
        # The user opts for the thematic search 'politique'.
        # Check that the associated lexicon is well implemented.
        self.q_2.switch()
        self.assertIn('macron', self.q_2.search)

    def test_info(self):
        # The user enters a search term that refers to nothing
        # in the index.
        # Check the expected message is generated.
        self.q_3.switch()
        self.assertEqual(self.q_3.info, {
            'fail': "Aucun résultat pour cette recherche."
        })
