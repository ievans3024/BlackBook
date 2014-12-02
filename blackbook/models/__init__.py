__author__ = 'ievans3024'

'''
class Person(object):
    def __init__(self, id, first_name, last_name, emails=[], phone_numbers=[],
                 address_line_1=None, address_line_2=None, city=None, state=None, zip_code=None, country=None):
        """
        Person constructor
        :param id: The id to assign this Person
        :param first_name: This Person's first name.
        :param last_name: This Person's last name.
        :param emails: A list of this Person's emails as Email instances (optional)
        :param phone_numbers: A list of this Person's phone numbers as PhoneNumber instances (optional)
        :param address_line_1: The first line of this Person's physical address (optional)
        :param address_line_2: The second line of this Person's physical address (optional)
        :param city: The city this Person is located in (optional)
        :param state: The state this Person is located in (optional)
        :param zip_code: The zip code this Person is located in (optional)
        :param country: The country this Person is located in (optional)
        :return:
        """
        raise NotImplementedError()

    def get_collection_object(self, short=False, as_dict=False):
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
    def get_collection_template(as_dict=False):
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


class Email(object):
    def __init__(self, email_type, email):
        """
        Email constructor
        :param email_type: The classification of this Email (e.g., "home", "work", etc.)
        :param email: The email address that this Email represents
        :return:
        """
        raise NotImplementedError()


class PhoneNumber(object):
    def __init__(self, number_type, number):
        """
        PhoneNumber constructor
        :param number_type: The classification of this PhoneNumber (e.g., "home", "work", etc.)
        :param number: The phone number that this PhoneNumber represents
        :return:
        """
        raise NotImplementedError()
'''