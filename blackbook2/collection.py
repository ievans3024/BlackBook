__author__ = 'ievans3024'


from flask import json

COLLECTION_JSON = 'application/vnd.collection+json'


class CollectionPlusJSON(object):

    mimetype = COLLECTION_JSON

    def __init__(self):
        self.collection = {
            'collection': {
                'version': '1.0',
                'href': '/api/',
                'items': [],
                'links': [],
                'queries': [
                    {
                        'href': '/api/search/',
                        'rel': 'search',
                        'prompt': 'Find a specific entry',
                        'data': [{'name': 'query', 'value': ''}]
                    }
                ]
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

    def __call__(self):
        return {
            'href': self.uri,
            'data': [{'name': key, 'value': value} for (key, value) in self.data.items()]
        }

    def __delitem__(self, key):
        del self.data[key]

    def __init__(self, uri, **kwargs):
        self.uri = uri
        self.data = kwargs

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        return json.dumps(self.__call__())