__author__ = 'ievans3024'

"""
FlatfileDatabase data models
"""

from blackbook.collection import parse_template
from collection_json import Data, Item, Template
from flask_crudsdb import Model, ModelError


class FlatDatabaseModel(Model):

    def __init__(self, pk, data):
        super(FlatDatabaseModel, self).__init__(data)
        self.id = abs(int(pk))
        self.update(data)

    def get_collection_item(self, as_dict=False):
        return super(FlatDatabaseModel, self).get_collection_item(as_dict)

    @staticmethod
    def get_template(as_dict=False):
        return super(FlatDatabaseModel).get_template(as_dict)

    def update(self, data):
        data = parse_template(data)
        for required in self.__required__:
            if required not in data:
                raise ModelError('%s not found in provided data but is a required attribute.' % required)
        for k, v in data.iteritems():
            if hasattr(self.__class__, k):
                setattr(self, k, v)
            else:
                print('attribute {key} not found in class {type}'.format(key=k, type=self.__class__.__name__))


class Person(FlatDatabaseModel):

    __required__ = [
        'first_name',
        'last_name'
    ]

    __indexed__ = [
        'first_name',
        'last_name',
        'address_line_1',
        'address_line_2',
        'city',
        'state',
        'zip',
        'country'
    ]

    first_name = str
    last_name = str
    emails = list
    phone_numbers = list
    address_line_1 = str
    address_line_2 = str
    city = str
    state = str
    zip_code = str
    country = str

    def __init__(self, pk, data):
        super(Person, self).__init__(pk, data)
        for attr in (self.emails, self.phone_numbers):
            if not isinstance(attr, type) and hasattr(attr, '__iter__'):
                for value in attr:
                    if attr is self.emails:
                        if not isinstance(value, Email):
                            raise ModelError('emails must be instances of %s' % Email.__name__)
                    else:
                        if not isinstance(value, PhoneNumber):
                            raise ModelError('phone numbers must be instances of %s' % PhoneNumber.__name__)

    def get_collection_item(self, short=False, as_dict=False):
        # TODO: Make this utilize Collection+JSON item data array better
        uri = '/api/entry/%d/' % self.id
        phone_numbers = [{'data': phone_number.get_collection_item()} for phone_number in self.phone_numbers]

        if not short:
            data = {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'emails': [{'data': email.get_collection_item()} for email in self.emails],
                'phone_numbers': phone_numbers,
                'address_line_1': self.address_line_1,
                'address_line_2': self.address_line_2,
                'city': self.city,
                'state': self.state,
                'zip_code': self.zip_code,
                'country': self.country
            }
        else:
            data = {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'phone_numbers': phone_numbers
            }
        if as_dict:
            return dict({'uri': uri}, **data)
        else:
            return Item(href=uri, data=[{'name': k, 'value': v} for k, v in data.items()])

    @staticmethod
    def get_template(as_dict=False):
        """
        Get the empty template for ReSTful API usage.
        :return: A template for Person data represented as a Template instance.
        """
        data = [
            {'name': 'first_name', 'value': '', 'prompt': 'First Name'},
            {'name': 'last_name', 'value': '', 'prompt': 'Last Name'},
            {'name': 'emails', 'value': [
                {
                    'data': [
                        {'name': 'email', 'prompt': 'name@example.com', 'value': ''},
                        {'name': 'email_type', 'prompt': 'Type (e.g., Home, Work)', 'value': ''}
                    ]
                }
            ], 'prompt': 'Emails'},
            {'name': 'phone_numbers', 'value': [
                {
                    'data': [
                        {'name': 'number', 'prompt': '555-555-5555', 'value': ''},
                        {'name': 'number_type', 'prompt': 'Type (e.g., Home, Work)', 'value': ''}
                    ]
                }
            ], 'prompt': 'Phone Numbers'},
            {'name': 'address_line_1', 'value': '', 'prompt': 'Address Line 1'},
            {'name': 'address_line_2', 'value': '', 'prompt': 'Address Line 2'},
            {'name': 'city', 'value': '', 'prompt': 'City'},
            {'name': 'state', 'value': '', 'prompt': 'State'},
            {'name': 'zip_code', 'value': '', 'prompt': 'Zip Code'},
            {'name': 'country', 'value': '', 'prompt': 'Country'}
        ]
        if as_dict:
            data_dict = {}
            for item in data:
                data_dict[item['name']] = {'value': item.get('value'), 'prompt': item.get('prompt')}
            return data
        else:
            return Template(data)


class Email(FlatDatabaseModel):

    __required__ = [
        'email',
        'email_type',
        'person'
    ]

    __indexed__ = [
        'email',
        'email_type'
    ]

    email = str
    email_type = str
    person = object

    def __init__(self, pk, data):
        super(Email, self).__init__(pk, data)

    def get_collection_item(self, as_dict=False):
        data = [
            {'name': 'email', 'prompt': 'name@example.com', 'value': self.email},
            {'name': 'email_type', 'prompt': 'Type (e.g., Home, Work)', 'value': self.email_type}
        ]
        if as_dict:
            data_dict = {}
            for item in data:
                data_dict[item['name']] = {'value': item.get('value'), 'prompt': item.get('prompt')}
            return data_dict
        else:
            return [Data(item['name'], value=item.get('value'), prompt=item.get('prompt')) for item in data]


class PhoneNumber(FlatDatabaseModel):

    __required__ = [
        'number',
        'number_type',
        'person'
    ]

    __indexed__ = [
        'number',
        'number_type'
    ]

    number = str
    number_type = str
    person = object

    def __init__(self, pk, data):
        super(PhoneNumber, self).__init__(pk, data)

    def get_collection_item(self, as_dict=False):
        data = [
            {'name': 'number', 'prompt': '1-555-555-5555', 'value': self.number},
            {'name': 'number_type', 'prompt': 'Type (e.g., Home, Work)', 'value': self.number_type}
        ]
        if as_dict:
            data_dict = {}
            for item in data:
                data_dict[item['name']] = {'value': item.get('value'), 'prompt': item.get('prompt')}
            return data_dict
        else:
            return [Data(item['name'], value=item.get('value'), prompt=item.get('prompt')) for item in data]

models = {
    'Person': Person,
    'Email': Email,
    'PhoneNumber': PhoneNumber
}