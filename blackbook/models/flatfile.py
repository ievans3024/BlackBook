__author__ = 'ievans3024'

"""
FlatfileDatabase data models
"""

from blackbook.collection import parse_template
from collection_json import Item, Template
from flask_crudsdb import Model, ModelError


class FlatDatabaseModel(Model):

    __required__ = []

    def __init__(self, id, data):
        super(FlatDatabaseModel, self).__init__(data)
        self.id = abs(int(id))
        self.update(data)

    def get_collection_item(self, as_dict=False):
        return super(FlatDatabaseModel, self).get_collection_item(as_dict)

    @staticmethod
    def get_template(as_dict=False):
        return super(FlatDatabaseModel).get_template(as_dict)

    def update(self, data):
        data = parse_template(data)
        default = self.get_template(True)
        for required in self.__required__:
            if required not in data:
                raise ModelError('%s not found in provided data but is a required attribute.')
        for k, v in data.iteritems():
            if default.get(k) is not None:
                setattr(self, k, v)
            else:
                print('key %s not found in template' % k)


class Person(FlatDatabaseModel):

    # required data properties for this model
    __required__ = [
        'first_name',
        'last_name'
    ]
    first_name = ''
    last_name = ''
    emails = []
    phone_numbers = []
    address_line_1 = ''
    address_line_2 = ''
    city = ''
    state = ''
    zip = 0
    country = ''

    def __init__(self, id, data):
        super(Person, self).__init__(id, data)

    def get_collection_item(self, short=False, as_dict=False):
        uri = '/api/entry/%d/' % self.id
        phone_numbers = [
            {
                'number_type': phone_number.number_type,
                'number': phone_number.number
            }
            for phone_number in self.phone_numbers
        ]

        if not short:
            data = {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'emails': [{'email_type': email.email_type, 'email': email.email} for email in self.emails],
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
        'email_type'
    ]

    email = ''
    email_type = ''

    def __init__(self, id, data):
        super(Email, self).__init__(id, data)


class PhoneNumber(FlatDatabaseModel):
    def __init__(self, data):
        self.number_type = number_type
        self.number = number


'''
class Person(Database.Model):

        def __init__(self, id, first_name, last_name, emails=[], phone_numbers=[],
                     address_line1=None, address_line2=None, city=None, state=None, zip_code=None, country=None):

            self.id = abs(int(id))

            if type(emails) != list:
                raise TypeError('emails must be a list')
            if type(phone_numbers) != list:
                raise TypeError('phone_numbers must be a list')

            for email in emails:
                if not isinstance(email, FlatDatabase.Email):
                    raise TypeError(
                        'phone_numbers must contain instances of %s' % FlatDatabase.Email.__class__.__name__
                    )

            for phone_number in phone_numbers:
                if not isinstance(phone_number, FlatDatabase.PhoneNumber):
                    raise TypeError(
                        'phone_numbers must contain instances of %s' % FlatDatabase.PhoneNumber.__class__.__name__
                    )

            self.first_name = str(first_name)
            self.last_name = str(last_name)
            self.emails = emails
            self.phone_numbers = phone_numbers
            self.address_line1 = str(address_line1)
            self.address_line2 = str(address_line2)
            self.city = str(city)
            self.state = str(state)
            self.zip_code = str(zip_code)
            self.country = str(country)

    class Email(Database.Email):
        def __init__(self, email_type, email):
            self.email_type = email_type
            self.email = email

    class PhoneNumber(Database.PhoneNumber):
        def __init__(self, number_type, number):
            self.number_type = number_type
            self.number = number
'''