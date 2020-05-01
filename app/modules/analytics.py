#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon analytics module - level 1
"""

import os
from app.modules.clients import ES_
from app.modules.process import get_df, get_stat, get_delay, F_PATH
from urllib.parse import urlparse
import pandas as pd
import collections as coll
import statistics as st


class Analyzer:
    """
    This class gathers the posts related to
    the topic selected by the user and applies
    analytics - descriptive statistics.
    """

    def __init__(self, ref):
        self.ref = ref
        self.count = int()
        self.title = str()
        self.data = {}
        self.user_unique = []
        self.medias = []
        self.sample = {}
        self.stat = {}
        self.df_dom = pd.DataFrame()
        self.df_tone = pd.DataFrame()

    def gather_data(self):

        # Query the index
        ES_.indices.refresh(index=self.ref)
        self.count = ES_.count(index=self.ref)['count']
        res = ES_.search(
            index=self.ref,
            body={
                "size": 10000,
                "query": {
                    "match_all": {}
                },
                "sort": [
                    {
                        "date": {
                            "order": "asc"}
                    }
                ]
            }
        )

        data_ = res['hits']['hits']

        # Extract a sample to display on the dashboard
        self.sample = data_[:5] + data_[-5:]

        # Extract the title of the topic
        self.title = data_[0]['_source']['topic']

        # Store data in a dictionary
        self.data.update({
            "users": [hit['_source']['user'] for hit in data_],
            "posts": [hit['_source']['post'] for hit in data_],
            "date": [hit['_source']['date'] for hit in data_],
            "quotes": [hit['_source']['quotes'][0] for hit in data_
                       if hit['_source']['quotes']],
            "imgs": [hit['_source']['post_img'][0] for hit in data_
                     if hit['_source']['post_img']],
            "vids": [hit['_source']['post_vid'][0] for hit in data_
                     if hit['_source']['post_vid']],
            "sources": [hit['_source']['post_sources'][0] for hit in data_
                        if hit['_source']['post_sources']],
            "emoticons": [hit['_source']['post_tone'][0] for hit in data_
                          if hit['_source']['post_tone']]
        })

        self.analyze_data()

    def analyze_data(self):

        # Data to calculate participation
        self.user_unique = list(dict.fromkeys(self.data['users']))
        users = len(self.user_unique)
        user_set = [u for u in coll.Counter(self.data['users']).values()]

        # Data to calculate medias share
        self.medias = \
            self.data['imgs'] + self.data['vids'] + self.data['sources']
        domains = [urlparse(m).netloc for m in self.data['sources']]
        self.df_dom = get_df(domains)

        # Data to calculate emoticon tones
        self.df_tone = get_df(self.data['emoticons'])

        # Data to calculate persistence
        start = self.data['date'][0]
        end = self.data['date'][-1]
        lasting = get_delay(start, end)

        # Store information and statistical indicators
        # in a dictionary
        self.stat.update({
            "creation": start,
            "last_post": end,
            "persistence": round(lasting[1], 2),
            "hours": round(lasting[0], 2),
            "users": users,
            "posts": self.count,
            "avg_posting_per_hour": round(self.count / lasting[0], 1),
            "median_participation": st.median(user_set),
            "quote_rate":
                round((len(self.data['quotes']) / self.count) * 100, 1),
            "medias_rate": round((len(self.medias) / self.count) * 100, 1),
            "imgs": get_stat(self.data['imgs'], self.count, self.medias),
            "vids": get_stat(self.data['vids'], self.count, self.medias),
            "sources": get_stat(self.data['sources'], self.count, self.medias),
            "emoticons": len(self.data['emoticons'])
        })

        # Store text corpus in a dataframe
        # for NLP jobs and to allow the user
        # to download it for further analysis
        df = pd.DataFrame(data={
            "users": self.data['users'],
            "posts": self.data['posts']
        })
        path = os.path.join(F_PATH, 'data/' + str(self.ref) + '.csv')
        df.to_csv(path, sep=',', index=True)
