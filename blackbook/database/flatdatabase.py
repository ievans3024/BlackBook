__author__ = 'ievans3024'

from blackbook.database import Database
from blackbook.collection import json, CollectionPlusJSON, CollectionPlusJSONItem


class FlatDatabase(Database):
    """A Basic Database that operates in memory and stores as json in user-configurable directory"""
    class Person(Database.Person):

        def __init__(self, id, first_name, last_name, emails=[], phone_numbers=[],
                     address_line1=None, address_line2=None, city=None, state=None, zip_code=None, country=None):

            self.id = abs(int(id))

            if type(emails) != list:
                raise TypeError('emails must be a list')
            if type(phone_numbers) != list:
                raise TypeError('phone_numbers must be a list')

            for email in emails:
                if not isinstance(email, FlatDatabase.Email):
                    raise TypeError('emails must contain instances of Database().models["Email"]')

            for phone_number in phone_numbers:
                if not isinstance(phone_number, FlatDatabase.PhoneNumber):
                    raise TypeError('phone_numbers must contain instances of Database().models["PhoneNumber"]')

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

        def get_collection_object(self, short=False):
            """
            Get object for json parsing
            Returns object ready for json
            """
            phone_numbers = [
                {
                    'number_type': phone_number.number_type,
                    'number': phone_number.number
                }
                for phone_number in self.phone_numbers
            ]

            if not short:
                opts = {
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'emails': [{'email_type': email.email_type, 'email': email.email} for email in self.emails],
                    'phone_numbers': phone_numbers,
                    'address_line_1': self.address_line1,
                    'address_line_2': self.address_line2,
                    'city': self.city,
                    'state': self.state,
                    'zip_code': self.zip_code,
                    'country': self.country
                }
            else:
                opts = {
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'phone_numbers': phone_numbers
                }

            collection = CollectionPlusJSONItem(uri='/api/entry/%d/' % self.id, **opts)

            return collection

    class Email(Database.Email):
        def __init__(self, email_type, email):
            self.email_type = email_type
            self.email = email

    class PhoneNumber(Database.PhoneNumber):
        def __init__(self, number_type, number):
            self.number_type = number_type
            self.number = number

    def __init__(self, app):
        self.app = app
        self.models = {
            'Person': FlatDatabase.Person,
            'Email': FlatDatabase.Email,
            'PhoneNumber': FlatDatabase.PhoneNumber
        }
        try:
            self.__reload_db_file()
        except TypeError:
            raise RuntimeError('Database file not specified in config option FLAT_DATABASE_FILE')
        except (IOError, FileNotFoundError):
            self.database = {}
            self.__write_db_file()

    def __reload_db_file(self):
        with open(self.app.config['FLAT_DATABASE_FILE']) as db_file:
            self.database = json.load(db_file)

    def __write_db_file(self):
        with open(self.app.config['FLAT_DATABASE_FILE'], 'w') as db_file:
            json.dump(self.database, db_file)

    def create(self, data):
        """Creates a person"""
        try:
            id = sorted(self.database)[-1] + 1
        except IndexError:
            id = 0
        fname = data.get('first_name')
        lname = data.get('last_name')
        del data['first_name']
        del data['last_name']
        person = self.models['Person'](id, fname, lname, **data)
        if not self.database:
            self.database[0] = person
        response_object = CollectionPlusJSON()
        response_object.append_item(person.get_collection_object())
        self.__write_db_file()
        return response_object

    def update(self, id, data):
        person = self.database.get(id)
        if person:
            updated = dict(person.get_collection_object().__dict__, **data)
            fname = updated.get('first_name')
            lname = updated.get('last_name')

            del updated['first_name']
            del updated['last_name']

            person = self.models['Person'](id, fname, lname, **updated)
            self.database[id] = person

            response_object = CollectionPlusJSON()
            response_object.append_item(person.get_collection_object())
        else:
            response_object = Database.HTTP_ERRORS[404]
        self.__write_db_file()
        return response_object

    def read(self, id=None, page=1, per_page=5):
        response_object = CollectionPlusJSON()
        if id is None:
            for k, v in self.database.items():
                response_object.append_item(v.get_collection_object(short=True))
            response_object.paginate(page=page, per_page=per_page)
        else:
            person = self.database.get(id)
            if person:
                response_object.append_item(person.get_collection_object())
            else:
                response_object = Database.HTTP_ERRORS[404]
        return response_object

    def delete(self, id):
        person = self.database.get(id)
        if person:
            del self.database[id]
        else:
            response_object = Database.HTTP_404
        self.__write_db_file()
        return response_object

    def search(self, data):
        raise NotImplementedError()

    def generate_test_db(self):
        raise NotImplementedError()