__author__ = 'ievans3024'
# Based on Collection+JSON format by Mike Amundsen
# See http://amundsen.com/media-types/collection/format/

# Prefer json provided by flask
try:
    from flask import json
except ImportError:
    import json

from math import ceil

COLLECTION_JSON = 'application/vnd.collection+json'


class CollectionPlusJSON(object):

    # TODO: Make this subclass dict with some fancy extras

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


class CollectionPlusJSONItem(dict):

    def __contains__(self, item):

        if item in self.data:

            return True

        else:

            return False

    def __delitem__(self, key):

        del self.data[key]

    def __init__(self, uri=None, **kwargs):

        if uri is not None:
            self.href = uri

        self.data = kwargs

        super(dict, self).__init__(href=uri, data=self.data)

    def __getitem__(self, item):

        return self.data[item]

    def __setitem__(self, key, value):

        self.data[key] = value

    def __str__(self):

        return json.dumps(self.__dict__)

    __repr__ = __str__

    def get(self, k, d=None):

        if k in self.data:

            return self.data[k]

        else:

            return d

