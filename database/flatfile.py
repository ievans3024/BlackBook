__author__ = 'ievans3024'

import json

from collection_json import Collection

from database import Database


class FlatDatabase(Database):
    """A Basic Database that operates in memory and stores as json in user-configurable directory"""

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

    def __init__(self, app):
        self.app = app
        self.models = {
            'Person': FlatDatabase.Person,
            'Email': FlatDatabase.Email,
            'PhoneNumber': FlatDatabase.PhoneNumber
        }
        try:
            FileNotFoundError
        except NameError:
            FileNotFoundError = IOError  # python2/3 compatibility hack -- for open() errors -- better way to do this?
        try:
            self.__reload_db_file()
        except TypeError:
            raise RuntimeError('Database file not specified in config option FLAT_DATABASE_FILE')
        except (IOError, FileNotFoundError):
            # TODO: Make subclass of dict with auto-incrementing keys option
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
        self.__write_db_file()
        return Collection(href='/api/', items=[person.get_collection_object()])

    def update(self, id, data):
        person = self.database.get(id)
        if person:
            updated = dict(person.get_collection_object(as_dict=True), **data)
            fname = updated.get('first_name')
            lname = updated.get('last_name')

            del updated['first_name']
            del updated['last_name']

            person = self.models['Person'](id, fname, lname, **updated)
            self.database[id] = person
            self.__write_db_file()
            return Collection(href='/api/', items=[person.get_collection_object()])
        else:
            return Collection(href='/api/', error=Database.HTTP_ERRORS[404])

    def read(self, id=None, page=1, per_page=5):
        response = Collection(href='/api/')
        if id is None:
            for k, v in self.database.items():
                response.items.append(v.get_collection_object(short=True))
            response = self.paginate(response, endpoint="/api/entry/", page=page, per_page=per_page)[0]
        else:
            person = self.database.get(id)
            if person:
                response.items.append(person.get_collection_object())
            else:
                response = Collection(href='/api/', error=Database.HTTP_ERRORS[404])
        return response

    def delete(self, id):
        person = self.database.get(id)
        if person:
            del self.database[id]
            self.__write_db_file()
        else:
            return Database.HTTP_ERRORS[404]

    def search(self, data):
        pass

    def generate_test_db(self):
        """Generates a test/sample database in a temp directory"""
        if not self.app.config.get('TESTING'):
            raise RuntimeError('App config must have TESTING option set to True.')

        from os import mkdir
        from os.path import join, isdir
        from random import choice
        from tempfile import gettempdir
        from database import test_address_line_1s, test_address_line_2s, test_cities, test_first_names, \
            test_last_names, test_phone_numbers, test_states, test_zipcodes

        tempdir = join(gettempdir(), 'blackbook')

        if not isdir(tempdir):
            mkdir(tempdir)

        self.app.config['FLAT_DATABASE_FILE'] = '{0}'.format(
            join(tempdir, 'test.json').replace('\\', '\\')  # windows paths need two backslashes
        )

        id = 0

        while test_first_names and test_last_names:
            name = test_first_names.pop(test_first_names.index(choice(test_first_names)))
            surname = test_last_names.pop(test_last_names.index(choice(test_last_names)))
            person = self.models['Person'](
                id, name, surname,
                emails=[
                    self.models['Email']('primary', '{first}.{last}@example.com'.format(
                        first=name.lower(), last=surname.lower()
                    ))
                ],
                phone_numbers=[
                    self.models['PhoneNumber']('primary', '1-555-555-{0}'.format(
                        test_phone_numbers.pop(
                            test_phone_numbers.index(choice(test_phone_numbers))
                        )
                    ))
                ],
                address_line1=test_address_line_1s.pop(
                    test_address_line_1s.index(choice(test_address_line_1s))
                ),
                address_line2=test_address_line_2s.pop(
                    test_address_line_2s.index(choice(test_address_line_2s))
                ),
                city=choice(test_cities),
                state=choice(test_states),
                zip_code=choice(test_zipcodes)
            )
            self.database[id] = person
            id += 1