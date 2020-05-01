#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon topic / thematic filtering module
"""

import os
from app.modules.clients import SC_, CL_, ES_
from app.modules.process import hour, F_PATH
from app.modules.constants import THEMATIC_, LEXICON_
from bs4 import BeautifulSoup as bS
from datetime import datetime, date, timedelta
from dateparser import parse
import pandas as pd


class TopicSeeker:
    """
    This class filters and delivers topics stored
    in ES main index based on the user type of search.
    """

    def __init__(self, target):
        self.target = target
        self.search = str()
        self.spider = str()
        self.refs = []
        self.source = {}
        self.info = {}
        self.counter = []
        self.targeted_topic = {}

    def switch(self):

        # If the user opts for a thematic search
        # then the associated lexicon is to be implemented
        # and the data are to be retrieved in the index.
        if self.target in THEMATIC_:
            self.search = LEXICON_['{}'.format(self.target)]
            self.return_data()
        else:
            self.search = '"{}"'.format(self.target)
            self.get_sources()

    def get_sources(self):
        # Different spiders are to be launched
        # according to the user query.
        if self.target == 'récent':
            SC_.jobs.run('recent')
        else:
            SC_.jobs.run('searcher', job_args={'search': self.target})
        while list(SC_.activity.iter(count=1))[0]['event'] != 'job:completed':
            pass
        else:
            job_key = list(SC_.activity.iter(count=1))[0]['job']
            job = CL_.get_job(job_key)
            i = 0
            for item in job.items.iter():
                self.source.update({i: item['source']})
                i += 1

            self.parse()

    def parse(self):
        for i in range(len(self.source)):
            soup = bS(self.source[i], features='lxml')
            content = soup.find_all("li", class_="")
            ref_ = [
                c.get('data-id') for c in content
                if c.get('data-id') is not None
            ]
            for j in range(len(ref_)):
                data = soup.find(attrs={'data-id': '{}'.format(ref_[j])})
                ref = ref_[j]
                topic_ = data.find("a", class_="lien-jv topic-title")
                topic = topic_.text.strip()
                t_link = os.environ.get('BASE_') + topic_.get('href')
                count = data.find("span", class_="topic-count").text.strip()
                time = data.find("span", class_="topic-date").text.strip()
                today = date.today()
                if hour.match(time):
                    date_ = str(today) + 'T' + str(time)
                else:
                    date_ = parse(time)
                topics = {'topic': topic,
                          'topic_link': t_link,
                          'ref': ref,
                          'keywords': self.search,
                          'post_count': int(count),
                          'indexed': 0,
                          'last_msg_date': date_,
                          'collection_date': datetime.now()}
                ES_.index(index=os.environ.get('INDEX_'), id=ref, body=topics)
                self.counter.append(1)
            self.refs.extend(ref_)
        CL_.close()

        self.update_index()

    def update_index(self):
        for ref in self.refs:
            if ES_.indices.exists(index=ref) is True:
                ES_.indices.refresh(index=ref)
                count = ES_.count(index=ref)['count']
                ES_.update(
                    index=os.environ.get('INDEX_'),
                    id=ref,
                    body={
                        "doc": {
                            "indexed": count
                        }
                    }
                )
            else:
                pass
        ES_.indices.refresh(index=os.environ.get('INDEX_'))

        self.return_data()

    def return_data(self):

        # Execute the appropriate query
        # according to the type of search
        if self.target == 'récent':
            yesterday = datetime.now() - timedelta(days=1)
            res = ES_.search(
                index=os.environ.get('INDEX_'),
                body={
                    "size": 10000,
                    "query": {
                        "range": {
                            "collection_date": {
                                "gte": yesterday
                            }
                        }
                    }
                }
            )
        elif self.target in THEMATIC_:
            res = ES_.search(
                index=os.environ.get('INDEX_'),
                body={"size": 10000,
                      "query": {
                          "match": {
                              "topic": {
                                  "query": self.search,
                                  "analyzer": "french",
                                  "fuzziness": 1,
                                  "max_expansions": 10,
                                  "prefix_length": 5
                              }
                          }
                      },
                      "sort": [
                          {
                              "post_count": {
                                  "order": "desc"}
                          },
                          "_score"]
                      }
            )
        else:
            res = ES_.search(
                index=os.environ.get('INDEX_'),
                body={"size": 10000,
                      "query": {
                        "query_string": {
                            "query": self.search,
                            "default_field": "topic"}
                        },
                      "sort": [
                          {
                              "post_count": {
                                  "order": "desc"}
                          },
                          "_score"]
                      }
            )

        # Return a message to the user
        # in case of query success / fail
        if res['hits']['total']['value'] > 0:
            self.targeted_topic = res['hits']['hits'][:200]
            self.info.update({
                'success': "{} document(s)".format(
                    res['hits']['total']['value']
                )
            })
        else:
            self.info.update({'fail': "Aucun résultat pour cette recherche."})

        # Store text corpus in a dataframe
        # for NLP jobs and to allow the user
        # to download it for further analysis
        df = pd.DataFrame(data={
            "topics": [hit['_source']['topic'] for hit in res['hits']['hits']]
        })
        file = '-'.join(self.target.split())
        path = os.path.join(F_PATH, 'data/' + file + '.csv')
        df.to_csv(path, sep=',', index=True)
