#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon ES Client
"""

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from scrapinghub import ScrapinghubClient

# Load environment variables
load_dotenv()

# Call ScrapingHub Python client
CL_ = ScrapinghubClient(os.environ.get('SH_KEY'))
SC_ = CL_.get_project(os.environ.get('SH_PROJ'))

# Call Elasticsearch Python client
ES_ = Elasticsearch(
    [os.environ.get('ES_PATH')],
    timeout=30,
    max_retries=10,
    retry_on_timeout=True
)
