import blackbook.database

from blackbook.api import API_URI_PREFIX
from blackbook.lib import collection_plus_json

__author__ = 'ievans3024'


class ModelCollection(collection_plus_json.Collection):

    def __init__(self, href, **kwargs):
        uri = API_URI_PREFIX + href
        uri = '/'.join([p for p in uri.split('/') if p != ''])
        super(ModelCollection, self).__init__(href=uri, **kwargs)

    def add_items(self, item):
        if isinstance(item, blackbook.database.Model):
            self.items = self.items + item.get_collection_items()


class ContactCreateTemplate(collection_plus_json.Template):
    pass


class ContactUpdateTemplate(ContactCreateTemplate):
    pass


class ContactCollection(ModelCollection):

    def __init__(self, href, template=ContactCreateTemplate(), **kwargs):
        super(ContactCollection, self).__init__(href, template=template, **kwargs)


class SessionCreateTemplate(collection_plus_json.Template):

    def __init__(self, **kwargs):
        data = [
            {'name': 'email', 'placeholder': 'user@example.com', 'prompt': 'Email', 'value': ''},
            {'name': 'password', 'placeholder': '', 'prompt': 'Password', 'value': ''}
        ]
        super(SessionCreateTemplate, self).__init__(data=data, **kwargs)


class SessionCollection(ModelCollection):

    def __init__(self, href, template=SessionCreateTemplate(), **kwargs):
        super(SessionCollection, self).__init__(href, template=template, **kwargs)


class UserCreateTemplate(collection_plus_json.Template):

    def __init__(self, public=True, **kwargs):
        data = [
            {'name': 'email', 'placeholder': 'user@example.com', 'prompt': 'Email', 'value': ''},
            {'name': 'name', 'placeholder': '"BlackBookUser123" or "John Doe"', 'prompt': 'Name', 'value': ''}
        ]
        if public:
            data.append({'name': 'password', 'prompt': 'Password', 'value': ''})
            data.append({'name': 'password2', 'prompt': 'Verify Password', 'value': ''})
        else:
            # comma separated list of group ids?
            data.append({'name': 'groups', 'prompt': 'User Groups', 'value': ''})
            # comma separated list of permission names?
            data.append({'name': 'permissions', 'prompt': 'User Permissions', 'value': ''})
        super(UserCreateTemplate, self).__init__(data=data, **kwargs)


class UserUpdateTemplate(UserCreateTemplate):

    def __init__(self, self_reference=True, **kwargs):
        super(UserUpdateTemplate, self).__init__(public=self_reference, **kwargs)


class UserCollection(ModelCollection):

    def __init__(self, href, template=UserCreateTemplate(), **kwargs):
        super(UserCollection, self).__init__(href=href, template=template, **kwargs)
