__author__ = 'ievans3024'
# Based on Collection+JSON format by Mike Amundsen
# See http://amundsen.com/media-types/collection/format/

from flask import json
from math import ceil

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

    def paginate(self, uri_template='{endpoint_uri}?page={page}&per_page={per_page}', page=1, per_page=5, leading=2,
                 trailing=2):
        if (type(page) is not int) or (type(per_page) is not int):

            try:
                page = abs(int(page))
            except (ValueError, TypeError):
                page = 1

            try:
                per_page = abs(int(per_page))
            except (ValueError, TypeError):
                per_page = 5

            if not page:
                page = 1
            if not per_page:
                per_page = 5

        number_of_pages = int(ceil(len(self.collection['collection']['items']) / per_page))

        if page > number_of_pages:
            page = number_of_pages

        page_index_begin = ((page * per_page) - per_page)
        page_index_end = (page * per_page)

        self.collection['collection']['items'] = self.collection['collection']['items'][page_index_begin:page_index_end]

        if page > 1:
            self.append_link(
                uri_template.format(endpoint_uri=self.collection['collection']['href'], page=1, per_page=per_page),
                'first',
                'First'
            )

            self.append_link(
                uri_template.format(endpoint_uri=self.collection['collection']['href'], page=(page - 1),
                                    per_page=per_page),
                'prev',
                'Previous'
            )

        if page - leading > 0:
            self.append_link(
                '',
                'skip',
                '&hellip;'
            )

        for lead_page in range(leading):
            page_num = page - lead_page
            if page_num > 0:
                self.append_link(
                    uri_template.format(endpoint_uri=self.collection['collection']['href'], page=page_num,
                                        per_page=per_page),
                    'more',
                    str(page_num)
                )

        self.append_link(
            uri_template.format(endpoint_uri=self.collection['collection']['href'], page=page,
                                per_page=per_page),
            'self',
            str(page)
        )

        for trail_page in range(trailing):
            page_num = page + trail_page
            if page_num < number_of_pages:
                self.append_link(
                    uri_template.format(endpoint_uri=self.collection['collection']['href'], page=page_num,
                                        per_page=per_page),
                    'more',
                    str(page_num)
                )

        if page + leading < number_of_pages:
            self.append_link(
                '',
                'skip',
                '&hellip;'
            )

        if page < number_of_pages:
            self.append_link(
                uri_template.format(endpoint_uri=self.collection['collection']['href'], page=page + 1,
                                    per_page=per_page),
                'next',
                'Next'
            )

            self.append_link(
                uri_template.format(endpoint_uri=self.collection['collection']['href'], page=number_of_pages,
                                    per_page=per_page),
                'last',
                'Last'
            )


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