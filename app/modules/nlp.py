#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon analytics module - level 2 (NLP)
"""

import os
from app.modules.clients import ES_
from app.modules.process import get_df, F_PATH
from app.modules.constants import STOP_
import pandas as pd
import unidecode
import spacy


class NlProcess:
    """
    This class performs the jobs related to
    the natural language processing functionality,
    from getting and preprocessing the corpus
    to extracting named entities and nouns from according
    to the data selected by the user.
    """

    def __init__(self, ref):
        # Read the csv which contains the corpus
        # identified by its reference
        self.ref = ref
        file = '-'.join(ref.split())
        path = os.path.join(F_PATH, 'data/{}.csv'.format(file))
        self.df = pd.read_csv(path)
        self.title = str()
        self.corpus = str()
        self.ner = pd.DataFrame()
        self.nouns = pd.DataFrame()

    def get_corpus(self):
        """
        This method determines the type of corpus
        and the title to give to the dataset.
        """
        if self.ref.isdigit():
            # If the reference is a number,
            # the type of corpus is topic-related,
            # else it is thematic-related.
            res = ES_.search(
                index=os.environ.get('INDEX_'),
                body={
                    "size": 10000,
                    "query": {
                        "match": {
                            "ref": self.ref
                        }
                    }
                }
            )
            self.title = res['hits']['hits'][0]['_source']['topic']
            # If the corpus comes from a topic,
            # it contains usernames which can be
            # identified as named entities.
            # So they are removed.
            corpus = self.df.posts.astype(str).str.strip()
            users = self.df.users.unique().tolist()
            posts = ' '.join(corpus).split()
            self.corpus = [w for w in posts if w not in users]
        else:
            self.title = self.ref
            self.corpus = self.df.topics.astype(str).str.strip()

        self.corpus = ' '.join(self.corpus)
        self.get_nlp()

    def get_nlp(self):
        """
        This method performs the extraction
        of named entities and nouns from the corpus.
        """

        # Load spaCy pretrained model
        nlp = spacy.load('fr_core_news_md')

        """
        A - Named entities recognition
        """

        # NER: Keep the capitals in place
        # to avoid loss of information
        doc_ner = nlp(self.corpus)

        # Discard 'MISC' labels from
        # the entities detected as well as
        # special chars and potential noise
        ner_ = [
            unidecode.unidecode(e.text) for e in doc_ner.ents
            if e.label_ != 'MISC'
            if e.text.isalnum()
            if len(e.text) > 1
        ]

        # Then normalize the dataset
        # by putting all the entities
        # in lowercase and remove undesired
        # words that may remain
        ner_ = [
            e.lower() for e in ner_
            if e.lower() not in STOP_
        ]

        # Apply statistics to the entity dataset
        self.ner = get_df(ner_)

        """
        B - Nouns extraction
        """

        doc_nouns = nlp(self.corpus.lower())

        # Add custom stop words given
        # the style of communication
        for w in STOP_:
            nlp.vocab[w].is_stop = True

        # Clean and extract nouns
        nouns_ = [
            unidecode.unidecode(n.text) for n in doc_nouns
            if n.is_stop is False
            if n.pos_ == 'NOUN'
            if n.text not in ner_
            if n.text.isalnum()
            if len(n.text) > 1
        ]

        self.nouns = get_df(nouns_)
