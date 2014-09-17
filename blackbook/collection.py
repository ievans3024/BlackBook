__author__ = 'ievans3024'
# Based on Collection+JSON format by Mike Amundsen
# See http://amundsen.com/media-types/collection/format/

from flask import json

COLLECTION_JSON = 'application/vnd.collection+json'


class CollectionPlusJSON(object):

    mimetype = COLLECTION_JSON

    def __init__(self, version=1.0, href='/api/'):
        # TODO: accept params to specify in collection
        self.collection = {
            'collection': {
                'version': str(version),
                'href': href,
                'items': [],
                'links': [],
                'queries': [
                    {
                        'href': '/api/search/',
                        'rel': 'search',
                        'prompt': 'Find a specific entry',
                        'data': [{'name': 'query', 'value': ''}]
                    }
                ],
                'template': {
                    'data': []
                },
                'error': {}
            }
        }

    def __str__(self):
        return json.dumps(self.collection)

    def append_item(self, item):
        if not type(item) is dict:
            raise TypeError('item must be a dict!')
        self.collection['collection']['items'].append(item)

    def append_link(self, uri, rel, prompt):
        self.collection['collection']['links'].append({'href': uri, 'rel': rel, 'prompt': prompt})


class CollectionPlusJSONItem(object):

    # TODO: make href optional (non-existent if not specified)
    # TODO: make this subclass dict with some fancy extras for proper Collection+JSON form

    def __dict__(self):
        package = {}

        if self.uri:
            package['href'] = self.uri

        package['data'] = [{'name': key, 'value': value} for (key, value) in self.data.items()]

        return package

    def __delitem__(self, key):
        del self.data[key]

    def __init__(self, uri=None, **kwargs):
        self.uri = uri
        self.data = kwargs

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        return json.dumps(self.get_dict())