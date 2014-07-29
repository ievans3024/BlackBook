__author__ = 'ievans3024'

from flask_sqlalchemy import SQLAlchemy
from blackbook2 import app
from blackbook2.collection import CollectionPlusJSONItem

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

    def get_collection_object(self):
        """
        Get object for json parsing
        Returns object ready for json
        """
        collection = CollectionPlusJSONItem('/api/entry/%d/' % self.id, **{
            'first_name': self.first_name,
            'last_name': self.last_name,
            'emails': [{email.email_type: email.email} for email in self.emails],
            'phone_numbers': [{phone.number_type: phone.number} for phone in self.phone_numbers],
            'address_line_1': self.address_line1,
            'address_line_2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country
        })

        return collection()


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


def generate_test_db():
    if not app.config.get('TESTING'):
        raise RuntimeError('App config must have TESTING option set to True.')

    from os.path import join
    from random import choice
    from tempfile import gettempdir

    # TODO: Populate these with bullshit data

    first_names = [
        'Alex', 'Andrea', 'Bryce', 'Brianna', 'Cole', 'Cathy', 'Derek', 'Danielle', 'Eric', 'Edith', 'Fred', 'Felicia',
        'Garrett', 'Gianna', 'Harold', 'Helga', 'Ira', 'Ingrid', 'Jonathan', 'Jacquelyn', 'Kerry', 'Karen', 'Larry',
        'Laura', 'Melvin', 'Margaret', 'Noel', 'Natalie', 'Otis', 'Olga', 'Peter', 'Pia', 'Quentin', 'Quinn',
        'Reginald', 'Rachel', 'Steven', 'Samantha', 'Tyler', 'Tullia', 'Ulric', 'Uma', 'Vincent', 'Valerie', 'Wade',
        'Wendy', 'Xavier', 'Xandra', 'Zach', 'Zoe'
    ]

    last_names = [
        'Ashford', 'Aldred', 'Beckett', 'Blackford', 'Carey', 'Conaway', 'Delung', 'Doohan', 'Eagan', 'Eastman',
        'Farley', 'Flores', 'Gandy', 'Grimes', 'Harkness', 'Hughley', 'Inman', 'Isley', 'Jager', 'Johannsen',
        'Keatinge', 'Kaufman', 'Lachance', 'Lopez', 'Markley', 'Meeker', 'Norrell', 'Nunnelly', 'Oberman', 'Osmond',
        'Puterbough', 'Pinkman', 'Quigly', 'Quayle', 'Romero', 'Rosenkranz', 'Smith', 'Stillman', 'Titsworth',
        'Thomson', 'Umbrell', 'Underwood', 'Valentine', 'Voyer', 'Wheatley', 'Wetzel', 'Xerxes', 'Xin', 'Yancey',
        'York', 'Zeeley', 'Zorn'
    ]

    phone_numbers = [
        '8208', '6768', '4514', '3589', '2611', '2300', '8704', '6427', '1970', '6449', '2902', '0689',
        '1695', '9713', '6905', '4483', '3876', '9844', '5312', '3451', '7077', '2009', '8568', '6801',
        '9060', '4410', '3072', '4123', '6190', '8853', '1415', '6155', '7584', '9710', '1069', '9864',
        '9944', '6118', '3151', '1504', '2391', '6684', '2697', '6541', '9924', '1167', '8599', '3120'
    ]

    address_line1s = [
        '240 2nd St.', '424 23rd St.', '148 18th St.', '888 23rd Ave.', '476 7th Ave.', '796 6th Ave.', '641 16th St.',
        '794 5th St.', '403 11th St.', '323 3rd Ave.', '310 7th St.', '83 14th Ave.', '576 10th Ave.', '700 19th St.',
        '826 12th Ave.', '301 11th Ave.', '14 22nd Ave.', '897 2nd Ave.', '455 17th Ave.', '55 9th St.', '821 5th Ave.',
        '858 10th Ave.', '25 6th St.', '576 9th Ave.', '352 16th St.', '301 8th St.', '85 6th St.', '163 6th Ave.',
        '340 4th St.', '660 14th St.', '888 1st Ave.', '564 10th St.', '170 5th St.', '640 17th Ave.', '469 5th St.',
        '41 18th Ave.', '39 11th Ave.', '712 20th St.', '848 22nd St.', '661 3rd St.', '296 8th St.', '147 11th St.',
        '289 5th St.', '299 22nd St.', '205 23rd St.', '699 2nd Ave.', '355 12th Ave.', '72 5th St.'
    ]

    address_line2s = [
        'Apt. B', 'Apt. 580', 'Apt. 350', None, None, 'Apt. 899', 'Apt. 149', None, None, 'Apt. N', 'Apt. 868',
        'Apt. Y', None, 'Apt. 277', 'Apt. M', None, 'Apt. 927', None, None, None, 'Apt. W', None, 'Apt. U', 'Apt. 739',
        'Apt. 113', None, 'Apt. O', 'Apt. 990', None, None, None, 'Apt. 245', 'Apt. 242', 'Apt. 569', None, None, None,
        'Apt. 144', 'Apt. G', None, 'Apt. 960', 'Apt. X', None, 'Apt. 582', 'Apt. 955', 'Apt. H', 'Apt. 879', None
    ]

    cities = [
        'Example City',
        'Nowhere',
        'Sigil',
        'Pleasantville'
    ]

    states = [
        'XY',
        'XX',
        'ZY',
        'ZX'
    ]

    zipcodes = [str(n).zfill(5) for n in range(100)]

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(
        join(gettempdir(), 'blackbook2', 'test.db').replace('\\', '\\')  # windows paths need two backslashes
    )

    db.create_all()

    while first_names and last_names:
        name = first_names.pop(first_names.index(choice(first_names)))
        surname = last_names.pop(last_names.index(choice(last_names)))

        db.session.add(Person(name, surname))

    db.session.commit()  # Must commit to create persons before modifying them.

    for person in Person.query.all():
        person.emails = [
            Email('primary', '{first}.{last}@example.com'.format(**{
                'first': person.first_name,
                'last': person.last_name
            }), person.id)
        ]
        person.phone_numbers = [
            PhoneNumber('primary', '1-555-555-{0}'.format(
                phone_numbers.pop(phone_numbers.index(choice(phone_numbers)))
            ), person.id)
        ]
        person.address_line1 = address_line1s.pop(address_line1s.index(choice(address_line1s)))
        person.address_line2 = address_line2s.pop(address_line2s.index(choice(address_line2s)))
        person.city = choice(cities)
        person.state = choice(states)
        person.zip_code = choice(zipcodes)

    db.session.commit()