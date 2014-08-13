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

        return collection()

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

    from os import mkdir
    from os.path import join, isdir
    from random import choice
    from tempfile import gettempdir

    first_names = [
        'Alex', 'Andrea', 'Bryce', 'Brianna', 'Cole', 'Cathy', 'Derek', 'Danielle', 'Eric', 'Edith', 'Fred', 'Felicia',
        'Garrett', 'Gianna', 'Harold', 'Helga', 'Ira', 'Ingrid', 'Jonathan', 'Jacquelyn', 'Kerry', 'Karen', 'Larry',
        'Laura', 'Melvin', 'Margaret', 'Noel', 'Natalie', 'Otis', 'Olga', 'Peter', 'Pia', 'Quentin', 'Quinn',
        'Reginald', 'Rachel', 'Steven', 'Samantha', 'Tyler', 'Tullia', 'Ulric', 'Uma', 'Vincent', 'Valerie', 'Wade',
        'Wendy', 'Xavier', 'Xandra', 'Yusef', 'Yolanda', 'Zach', 'Zoe'
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
        '6310', '2686', '8370', '7294', '0480', '8213', '1676', '5981', '9820', '9213', '6547', '1629', '7464', '6742',
        '2307', '3152', '3245', '4283', '0144', '4995', '1271', '9220', '9827', '7032', '4855', '7975', '3912', '8340',
        '7934', '4647', '6552', '3079', '6161', '1307', '3158', '1034', '0295', '2317', '7179', '0743', '8588', '7068',
        '2450', '9826', '6458', '0554', '5614', '5106', '5020', '0577', '7277', '6371'
    ]

    address_line1s = [
        '907 23rd St.', '972 24th Ave.', '483 24th Ave.', '676 8th Ave.', '984 21st St.', '923 19th St.',
        '734 13th Ave.', '741 22nd Ave.', '45 20th Ave.', '597 16th St.', '259 15th Ave.', '361 3rd Ave.',
        '697 21st St.', '887 18th Ave.', '403 9th Ave.', '684 9th Ave.', '641 19th Ave.', '398 2nd Ave.',
        '752 11th St.', '237 14th St.', '393 8th Ave.', '603 18th Ave.', '601 15th St.', '54 2nd Ave.', '357 20th Ave.',
        '424 10th Ave.', '343 18th St.', '448 13th St.', '743 6th St.', '308 13th St.', '929 15th Ave.', '990 19th St.',
        '27 19th St.', '119 12th St.', '156 15th Ave.', '698 3rd St.', '177 24th Ave.', '663 1st St.', '808 5th Ave.',
        '88 10th St.', '776 15th St.', '927 9th St.', '834 7th Ave.', '786 6th Ave.', '598 22nd St.', '653 2nd St.',
        '162 4th St.', '552 4th Ave.', '118 8th St.', '900 3rd St.', '9 14th St.', '921 9th Ave.'
    ]

    address_line2s = [
        None, None, 'Apt. R', 'Apt. 786', 'Apt. K', 'Apt. V', None, 'Apt. X', 'Apt. N', None, None, 'Apt. 789',
        'Apt. O', 'Apt. S', 'Apt. J', 'Apt. 778', None, 'Apt. 662', None, 'Apt. P', 'Apt. 717', 'Apt. E', 'Apt. 402',
        'Apt. W', None, 'Apt. 545', None, None, 'Apt. X', None, None, 'Apt. T', 'Apt. 183', None, None, None,
        'Apt. 104', 'Apt. L', 'Apt. 675', 'Apt. C', 'Apt. D', None, 'Apt. V', None, 'Apt. 846', 'Apt. 804', 'Apt. 365',
        'Apt. 447', 'Apt. 330', None, 'Apt. 765', None
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

    tempdir = join(gettempdir(), 'blackbook2')

    if not isdir(tempdir):
        mkdir(tempdir)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(
        join(tempdir, 'test.db').replace('\\', '\\')  # windows paths need two backslashes
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
                'first': person.first_name.lower(),
                'last': person.last_name.lower()
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