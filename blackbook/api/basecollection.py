from blackbook.api import API_URI_PREFIX
from blackbook.lib import collection_plus_json

__author__ = 'ievans3024'


class ContactCreateTemplate(collection_plus_json.Template):
    pass


class ContactUpdateTemplate(collection_plus_json.Template):
    pass


class ContactCollection(collection_plus_json.Collection):
    pass


class UserCreateTemplate(collection_plus_json.Template):

    def __init__(self, public=True, **kwargs):
        data = [
            {'name': 'email', 'prompt': 'Email', 'placeholder': 'user@example.com', 'value': ''},
            {'name': 'name', 'prompt': 'Name', 'placeholder': '"BlackBookUser123" or "John Doe"', 'value': ''}
        ]
        if public:
            data.append({'name': 'password', 'prompt': 'Password', 'value': ''})
            data.append({'name': 'password2', 'prompt': 'Verify Password', 'value': ''})
        else:
            data.append({'name': 'groups', 'prompt': 'User Groups', 'value': []})
            data.append({'name': 'permissions', 'prompt': 'User Permissions', 'value': []})
        super(UserCreateTemplate, self).__init__(data=data, **kwargs)


class UserUpdateTemplate(collection_plus_json.Template):

    def __init__(self, self_reference=True, **kwargs):
        data = [
            {'name': 'email', 'prompt': 'Email', 'placeholder': 'user@example.com', 'value': ''},
            {'name': 'name', 'prompt': 'Name', 'placeholder': '"BlackBookUser123" or "John Doe"', 'value': ''}
        ]
        if self_reference:
            data.append({'name': 'password', 'prompt': 'Password', 'value': ''})
            data.append({'name': 'password2', 'prompt': 'Verify Password', 'value': ''})
        else:
            data.append({'name': 'groups', 'prompt': 'User Groups', 'value': []})
            data.append({'name': 'permissions', 'prompt': 'User Permissions', 'value': []})
        super(UserUpdateTemplate, self).__init__(data=data, **kwargs)


class UserCollection(collection_plus_json.Collection):

    def __init__(self, href, version="1.0", error=None, items=[],
                 links=[], queries=[], template=UserCreateTemplate(), **kwargs):
        uri = API_URI_PREFIX + href
        uri = '/'.join([p for p in uri.split('/') if p != ''])
        super(UserCollection, self).__init__(
            href=uri, version=version,
            error=error, items=items,
            links=links, queries=queries,
            template=template, **kwargs)
