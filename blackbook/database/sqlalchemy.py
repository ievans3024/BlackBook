__author__ = 'ievans3024'

from flask_sqlalchemy import SQLAlchemy
from blackbook.collection import CollectionPlusJSONItem
from blackbook.database import Database


class SQLDatabase(Database):
    """SQL database wrapper"""

    def __init__(self, app):

        db = SQLAlchemy(app)

        class Person(db.Model):
            __searchable__ = [
                'first_name',
                'last_name',
                'address_line1',
                'address_line2',
                'city',
                'state',
                'zip_code',
                'country'
            ]

            id = db.Column(db.Integer, primary_key=True)
            first_name = db.Column(db.String(100))
            last_name = db.Column(db.String(100))
            emails = db.relationship('Email', backref='person', lazy='dynamic')  # TODO: make these m2m relationships
            phone_numbers = db.relationship('PhoneNumber', backref='person', lazy='dynamic')  # TODO
            address_line1 = db.Column(db.String(50), nullable=True)
            address_line2 = db.Column(db.String(50), nullable=True)
            city = db.Column(db.String(50), nullable=True)
            state = db.Column(db.String(2), nullable=True)
            zip_code = db.Column(db.String(11), nullable=True)
            country = db.Column(db.String(50), nullable=True)

            def __init__(self, first_name, last_name, emails=[], phone_numbers=[],
                         address_line1=None, address_line2=None, city=None, state=None, zip_code=None, country=None):
                self.first_name = first_name
                self.last_name = last_name
                self.emails = emails
                self.phone_numbers = phone_numbers
                self.address_line1 = address_line1
                self.address_line2 = address_line2
                self.city = city
                self.state = state
                self.zip_code = zip_code
                self.country = country

            @staticmethod
            def get_collection_template():
                """
                Get object for template
                Returns object ready for json
                """
                opts = {
                    'first_name': '',
                    'last_name': '',
                    'emails': [{'email_type': '', 'email': ''}],
                    'phone_numbers': [{'number_type': '', 'number': ''}],
                    'address_line_1': '',
                    'address_line_2': '',
                    'city': '',
                    'state': '',
                    'zip_code': '',
                    'country': ''
                }

                collection = CollectionPlusJSONItem('', **opts)

                return collection.get_dict()

            def get_collection_object(self, short=False):
                """
                Get object for json parsing
                Returns object ready for json
                """
                phone_numbers = {}
                emails = {}

                for number in self.phone_numbers:
                    phone_numbers[number.number_type] = number.number

                for email in self.emails:
                    emails[email.email_type] = email.email

                if not short:
                    opts = {
                        'first_name': self.first_name,
                        'last_name': self.last_name,
                        'emails': emails,
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

                collection = CollectionPlusJSONItem('/api/entry/%d/' % self.id, **opts)

                return collection.get_dict()

        class Email(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            email_type = db.Column(db.String(20))
            email = db.Column(db.String(100))
            person_id = db.Column(db.Integer, db.ForeignKey('person.id'))  # TODO: make this an m2m relationship

            def __init__(self, email_type, email, person_id):
                self.email_type = email_type
                self.email = email
                self.person_id = person_id

        class PhoneNumber(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            number_type = db.Column(db.String(20))
            number = db.Column(db.String(100))
            person_id = db.Column(db.Integer, db.ForeignKey('person.id'))  # TODO: make this an m2m relationship

            def __init__(self, number_type, number, person_id):
                self.number_type = number_type
                self.number = number
                self.person_id = person_id

        self.app = app
        self.database = db
        self.models = {
            'Person': Person,
            'Email': Email,
            'PhoneNumber': PhoneNumber
        }

    def new(self):
        pass

    def edit(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def search(self):
        pass

    def generate_test_db(self):
        if not self.app.config.get('TESTING'):
            raise RuntimeError('App config must have TESTING option set to True.')

        from os import mkdir
        from os.path import join, isdir
        from random import choice
        from tempfile import gettempdir
        from blackbook.database import test_address_line1s, test_address_line2s, test_cities, test_first_names, \
            test_last_names, test_phone_numbers, test_states, test_zipcodes

        tempdir = join(gettempdir(), 'blackbook')

        if not isdir(tempdir):
            mkdir(tempdir)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(
            join(tempdir, 'test.db').replace('\\', '\\')  # windows paths need two backslashes
        )

        self.database.create_all()

        while test_first_names and test_last_names:
            name = test_first_names.pop(test_first_names.index(choice(test_first_names)))
            surname = test_last_names.pop(test_last_names.index(choice(test_last_names)))

            self.database.session.add(self.models['Person'](name, surname))

        self.database.session.commit()  # Must commit to create persons before modifying them.

        for person in self.models['Person'].query.all():
            person.emails = [
                self.models['Email']('primary', '{first}.{last}@example.com'.format(
                    first=person.first_name.lower(),
                    last=person.last_name.lower()
                ), person.id)
            ]
            person.phone_numbers = [
                self.models['PhoneNumber']('primary', '1-555-555-{0}'.format(
                    test_phone_numbers.pop(test_phone_numbers.index(choice(test_phone_numbers)))
                ), person.id)
            ]
            person.address_line1 = test_address_line1s.pop(test_address_line1s.index(choice(test_address_line1s)))
            person.address_line2 = test_address_line2s.pop(test_address_line2s.index(choice(test_address_line2s)))
            person.city = choice(test_cities)
            person.state = choice(test_states)
            person.zip_code = choice(test_zipcodes)

        self.database.session.commit()