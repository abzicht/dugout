import requests
import logging
import json

class DugoutPull():

    def __init__(self, address, port, path=''):
        self.url = 'http://{}:{}{}'.format(address, port, path)
        self.session = requests.Session()

    def pull(self):
        logging.info('Requesting sensor data from {}'.format(self.url))
        response = self.session.get(self.url)
        if not response.ok:
            raise Exception('Sensor data request was responded with a bad status code: {}'.format(response.status_code))
        try:
            json_response = json.loads(response.text)
        except Exception as msg:
            raise Exception('Failed to parse response: {}'.format(msg))
        else:
            return json_response

