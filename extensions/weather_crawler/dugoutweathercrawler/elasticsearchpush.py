#!/usr/bin/env python

import json
import sys
import logging
from elasticsearch import Elasticsearch

try:
    from dugoutdew import dewpoint
except ImportError:
    from dugoutcrawler.dugoutdew import dewpoint

class ElasticsearchPush():
    def __init__(self, address, port, username, password):
        url = 'http://{}:{}@{}:{}/'.format(username,password,address,port)
        self.es = Elasticsearch(hosts=[url])

    def create_index(self, index, mapping):
        logging.info('Creating Elasticsearch index \'{}\''.format(index))
        self.es.indices.create(index=index, ignore=400, body=mapping)

    def bulk_push(self, index, sensor_data):
        logging.info('Pushing data to index \'{}\''.format(index))
        sensors = sensor_data['sensors']
        bulk_data = []
        for sensor_id in sensors.keys():
            op_dict = {
               "index": {
                    "_index": index,
                    "_id": '{}-{}'.format(sensor_data['timestamp'], sensor_id)
                }
            }
            dp = dewpoint(sensors[sensor_id]['temperature'], sensors[sensor_id]['humidity'])
            body = {
                    "timestamp":     sensor_data['timestamp'],
                    "sensor_id":     sensor_id,
                    "temperature":   sensors[sensor_id]['temperature'],
                    "humidity":      sensors[sensor_id]['humidity'],
                    "dewpoint":      dp,
                    "success_t":     sensors[sensor_id]['success_t'],
                    "success_h":     sensors[sensor_id]['success_h'],
                    }
            bulk_data.append(op_dict)
            bulk_data.append(body)
        #self.es.index(index=index_dugout, id=id_, body=body)
        #self.es.index(index=index_dugout, body=body)
        self.es.bulk(index=index, body=bulk_data, refresh=False)
