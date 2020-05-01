#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon Analytics utils unit tests
"""

from app.modules.process \
    import get_stat, get_df, get_pie, get_datetime, get_delay
import unittest


class TestAnalyticsProcessing(unittest.TestCase):

    def setUp(self):
        # Fixture
        self.users = [
            'tiTi#', 'Lulu_9', 'RophY', 'tiTi#', 'tiTi#',
            'Lulu_9', 'Yog@Z', 'tiTi#', 'Lulu_9', 'RophY'
        ]
        self.img_ = [
            'http://img_1.png', 'http://img_2.png', 'http://img_3.png',
            'http://img_4.png', 'http://img_4.png', 'http://img_5.png'
        ]
        self.vid_ = ['https://www.youtube.com/super-video']
        self.source_ = ['https://www.wikipedia.fr/super-article']
        self.quotes = [
            'D\'accord avec toi !', 'Regarde ici aussi', 'Merci',
            'Intéressant !', 'Vous avez vu la vidéo ?'
        ]
        self.emoticons = [
            'approbation', 'joie', 'approbation',
            'sourire', 'sourire', 'rire', 'doute'
        ]
        self.posts = len(self.users)
        self.medias = self.img_ + self.vid_ + self.source_

    def test_get_stat(self):
        # Check point 1:
        # Are the returned rate, share and
        # list items values accurate?
        img = get_stat(self.img_, self.posts, self.medias)
        self.assertEqual(img['rate'], 60.0)
        self.assertEqual(img['share'], 75.0)
        self.assertEqual(img['list'], [
            'http://img_1.png', 'http://img_2.png',
            'http://img_3.png', 'http://img_4.png',
            'http://img_5.png'
        ])

    def test_get_df(self):
        # Check point 2:
        # Is a data frame generated and
        # does it contain the expected values?
        users = get_df(self.users)
        self.assertEqual(len(users), 4)
        self.assertEqual(users['labels'][0], 'tiTi#')
        self.assertEqual(users['counts'][0], 4)
        self.assertEqual(users['rates'][0], 40.0)

    def test_get_pie(self):
        # Check point 3:
        # Does it return a Bokeh object?
        df = get_df(self.users)
        fig = get_pie(df)
        self.assertEqual(
            str(type(fig)), "<class 'bokeh.plotting.figure.Figure'>"
        )

    def test_get_datetime(self):
        # Check point 4:
        # Is the output a list containing
        # the sliced datetime?
        date_time = get_datetime('2020-04-01T12:00:00')
        self.assertEqual(date_time, [2020, 4, 1, 12, 0, 0])

    def test_get_delay(self):
        # Check point 5:
        # Is the returned delay accurate?
        start_ = '2020-04-01T12:00:00'
        end_ = '2020-04-01T18:00:00'
        delay = get_delay(start_, end_)
        self.assertEqual(delay, (6.0, 0.25))
