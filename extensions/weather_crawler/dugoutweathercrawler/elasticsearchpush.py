#!/usr/bin/env python

import json
import sys
import logging
from elasticsearch import Elasticsearch

class ElasticsearchPush():
    def __init__(self, address, port, username, password):
        url = 'http://{}:{}@{}:{}/'.format(username,password,address,port)
        self.es = Elasticsearch(hosts=[url])

    def create_index(self, index, mapping):
        logging.info('Creating Elasticsearch index \'{}\''.format(index))
        self.es.indices.create(index=index, ignore=400, body=mapping)

    def push(self, index, id_, data):
        logging.info('Pushing data to index \'{}\''.format(index))
        self.es.index(index=index, id=id_, body=data)
