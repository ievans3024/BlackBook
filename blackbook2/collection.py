__author__ = 'ievans3024'


import json


API_ROOT_URI = '/api/'
API_SEARCH_URI = '/api/search/'


class CollectionPlusJSON(object):

    def __init__(self):
        self.collection = {
            'collection': {
                'version': '1.0',
                'href': API_ROOT_URI,
                'items': [],
                'links': [],
                'queries': [
                    {
                        'href': API_SEARCH_URI,
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
        if not isinstance(item, CollectionPlusJSONItem):
            raise TypeError('Item supplied must be an instance of collection.CollectionPlusJSONItem')
        self.collection['items'].append(item)

    def append_link(self, uri, rel, prompt):
        self.collection['links'].append({'href': uri, 'rel': rel, 'prompt': prompt})


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