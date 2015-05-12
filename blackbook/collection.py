__author__ = 'ievans3024'
"""
Helper module for collection_json classes
"""

from collection_json import Collection, Link, Template
from math import ceil

# TODO: Convert to https://github.com/ievans3024/CollectionPlusJSON

MIMETYPE = 'application/vnd.collection+json'


def parse_template(template):
    """
    Parse a collection_json.Template object into key/value pairs.
    :param template: The template to parse.
    :type template: collection_json.Template
    :return: The Template data represented as a dict, with prompt and other non-key/value data stripped.
    """
    if not isinstance(template, Template):
        raise TypeError('Param "template" must be an instance of ' + Template.__name__)

    as_dict = {}
    properties = template.to_dict()['data']
    for prop in properties:
        as_dict[prop.get('name')] = prop.get('value')
    return as_dict


def paginate(collection, endpoint='', uri_template='{endpoint_uri}?page={page}&per_page={per_page}',
             page=None, per_page=5, leading=2, trailing=2):
    """
    Paginate this collection into a list of collections representing "pages" of this collection.
    :type collection: collection_json.Collection
    :type endpoint: str
    :type uri_template: str
    :type page: int
    :type per_page: int
    :type leading: int
    :type trailing: int
    :param endpoint: The URI for this resource.
    :param uri_template: A string providing a template for paginated URI structure. May include the following keys:
        "{endpoint_uri}" - This will evaluate to the value of the 'endpoint' param.
        "{page}" - The page number will be inserted here.
        "{per_page}" - The number of items to display per page will be inserted here.
    :param page: The page number to get.
    :param per_page: The number of items per page for this representation.
    :param leading: The number of leading pages before a page to add to its "links".
    :param trailing: The number of trailing pages after a page to add to its "links".
    :return tuple: A tuple of Collections representing ordered subsets of this collection. If the
        page parameter is supplied, the tuple will contain a single Collection representing one
        particular subset ("page") from this collection.

    """

    def sanitize_int(o, default=None):
        if type(o) is not int:
            try:
                number = abs(int(o))
            except (ValueError, TypeError) as e:
                if default is not None:
                    number = default
                else:
                    raise e
        else:
            number = o
        return number

    per_page = sanitize_int(per_page, default=5)
    if page is not None:
        page = sanitize_int(page, default=1)
    pages = []
    number_of_pages = int(ceil(len(collection.items) / per_page))

    def assemble_page():
        page_index_begin = ((page * per_page) - per_page)
        page_index_end = (page * per_page)
        new_page = Collection(href=collection.href, items=collection.items[page_index_begin:page_index_end])
        if collection.error:
            new_page.error = collection.error
        if collection.links:
            new_page.links = collection.links
        if collection.queries:
            new_page.queries = collection.qeuries
        if collection.template:
            new_page.template = collection.template
        if page > 1:
            new_page.links.append(Link(
                uri_template.format(endpoint_uri=endpoint, page=1, per_page=per_page),
                'first',
                prompt='First'
            ))

            new_page.links.append(Link(
                uri_template.format(endpoint_uri=endpoint, page=(page - 1), per_page=per_page),
                'prev',
                prompt='Previous'
            ))

            if page - trailing > 0:
                new_page.links.append(Link(
                    '',
                    'skip',
                    prompt='…'
                ))

            for lead_page in range(trailing, 0, -1):
                page_num = page - lead_page
                if page_num > 0 and page_num != page:
                    new_page.links.append(Link(
                        uri_template.format(endpoint_uri=endpoint, page=page_num, per_page=per_page),
                        'more',
                        prompt=str(page_num)
                    ))

        new_page.links.append(Link(
            uri_template.format(endpoint_uri=endpoint, page=page, per_page=per_page),
            'self',
            prompt=str(page)
        ))

        if page <= number_of_pages:
            for trail_page in range(1, leading + 1):
                page_num = page + trail_page
                if page_num <= number_of_pages:
                    new_page.links.append(Link(
                        uri_template.format(endpoint_uri=endpoint, page=page_num, per_page=per_page),
                        'more',
                        prompt=str(page_num)
                    ))

            if page + trailing < number_of_pages:
                new_page.links.append(Link(
                    '',
                    'skip',
                    prompt='…'
                ))

            if page <= number_of_pages:
                new_page.links.append(Link(
                    uri_template.format(endpoint_uri=endpoint, page=page + 1, per_page=per_page),
                    'next',
                    prompt='Next'
                ))

                new_page.links.append(Link(
                    uri_template.format(endpoint_uri=endpoint, page=number_of_pages, per_page=per_page),
                    'last',
                    prompt='Last'
                ))
        return new_page

    if page:
        pages.append(assemble_page())
    else:
        page = 1
        while page <= number_of_pages:
            pages.append(assemble_page())
            page += 1
    return tuple(pages)