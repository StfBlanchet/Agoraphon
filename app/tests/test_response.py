#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon response tests
"""

from app import app
import unittest


class TestResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # And propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # Check home route
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_error_status_code(self):
        # Check error page is displayed
        # in case the user tries a fake path
        resp = self.app.get('/fakereq')
        self.assertEqual(resp.status_code, 404)

    def test_download_status_code(self):
        # Check the status is 400 when
        # there is no file to download.
        resp = self.app.get('/download')
        self.assertEqual(resp.status_code, 400)

    def test_search_status_code(self):
        # Check the status is ok when the user
        # launches a nominal search
        resp = self.app.get('/topics?q=gilets+jaunes')
        self.assertEqual(resp.status_code, 200)

    def test_analytics_status_code(self):
        # The user launches an analysis on an indexed
        # topic and the status is ok.
        resp = self.app.get('/analytics?ref=62742007')
        self.assertEqual(resp.status_code, 200)

    def test_scrap_status_code(self):
        # The user launches a collect on a topic that
        # does not exist anymore and the status is ok.
        resp = self.app.get('/posts?ref=62861859')
        self.assertEqual(resp.status_code, 200)
