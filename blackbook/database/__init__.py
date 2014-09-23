__author__ = 'ievans3024'

from blackbook.collection import CollectionPlusJSON, CollectionPlusJSONItem


class Database(object):
    """Database wrapper, base class"""
     # TODO: Force usage of self.models['ModelName'] and make these private members?
    class Person(object):
        def __init__(self):
            raise NotImplementedError()

        def get_collection_object(self):
            raise NotImplementedError()

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

            collection = CollectionPlusJSONItem(uri='', **opts)

            return collection

    class Email(object):
        def __init__(self):
            raise NotImplementedError()

    class PhoneNumber(object):
        def __init__(self):
            raise NotImplementedError()

    def __init__(self, app):
        raise NotImplementedError()

    def create(self, data):
        raise NotImplementedError()

    def update(self, id, data):
        raise NotImplementedError()

    def read(self, id=None):
        raise NotImplementedError()

    def delete(self, id):
        raise NotImplementedError()

    def search(self, data):
        raise NotImplementedError()

    def generate_test_db(self):
        raise NotImplementedError()


class FlatDatabase(Database):
    """A Basic Database that operates in memory and stores as json in user-configurable directory"""
    class Person(Database.Person):

        def __init__(self, id, first_name, last_name, emails=[], phone_numbers=[],
                     address_line1=None, address_line2=None, city=None, state=None, zip_code=None, country=None):

            try:
                self.id = abs(int(id))
            except (TypeError, ValueError) as e:
                raise e
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
        self.database = {}
        self.models = {
            'Person': FlatDatabase.Person,
            'Email': FlatDatabase.Email,
            'PhoneNumber': FlatDatabase.PhoneNumber
        }

    def create(self, data):
        """Creates a person"""
        # TODO: Unpack data and supply correctly to Person.__init__()
        person = self.models['Person'](**data)
        if not self.database:
            self.database[0] = person
        response_object = CollectionPlusJSON(href=person.get_collection_object().get('href'))
        return response_object

    def update(self, id, data):
        raise NotImplementedError()

    def read(self, id=None):
        person = self.database.get(id)
        if person:
            response_object = CollectionPlusJSON(href=person.get_collection_object().get('href'))
        else:
            response_object = CollectionPlusJSON()  # TODO: common responses as constants?
            response_object['error'] = {
                'title': 'Not Found',
                'code': '404',
                'message': 'There is no Person with that id in the database.'
            }
        return response_object

    def delete(self, id):
        person = self.database.get(id)
        if person:
            del self.database[id]
        else:
            response_object = CollectionPlusJSON()
            response_object['error'] = {
                'title': 'Not Found',
                'code': '404',
                'message': 'There is no Person with that id in the database.'
            }
        return response_object


    def search(self, data):
        raise NotImplementedError()

    def generate_test_db(self):
        raise NotImplementedError()

test_first_names = [
    'Alex', 'Andrea', 'Bryce', 'Brianna', 'Cole', 'Cathy', 'Derek', 'Danielle', 'Eric', 'Edith', 'Fred', 'Felicia',
    'Garrett', 'Gianna', 'Harold', 'Helga', 'Ira', 'Ingrid', 'Jonathan', 'Jacquelyn', 'Kerry', 'Karen', 'Larry',
    'Laura', 'Melvin', 'Margaret', 'Noel', 'Natalie', 'Otis', 'Olga', 'Peter', 'Pia', 'Quentin', 'Quinn',
    'Reginald', 'Rachel', 'Steven', 'Samantha', 'Tyler', 'Tullia', 'Ulric', 'Uma', 'Vincent', 'Valerie', 'Wade',
    'Wendy', 'Xavier', 'Xandra', 'Yusef', 'Yolanda', 'Zach', 'Zoe'
]

test_last_names = [
    'Ashford', 'Aldred', 'Beckett', 'Blackford', 'Carey', 'Conaway', 'Delung', 'Doohan', 'Eagan', 'Eastman',
    'Farley', 'Flores', 'Gandy', 'Grimes', 'Harkness', 'Hughley', 'Inman', 'Isley', 'Jager', 'Johannsen',
    'Keatinge', 'Kaufman', 'Lachance', 'Lopez', 'Markley', 'Meeker', 'Norrell', 'Nunnelly', 'Oberman', 'Osmond',
    'Puterbough', 'Pinkman', 'Quigly', 'Quayle', 'Romero', 'Rosenkranz', 'Smith', 'Stillman', 'Titsworth',
    'Thomson', 'Umbrell', 'Underwood', 'Valentine', 'Voyer', 'Wheatley', 'Wetzel', 'Xerxes', 'Xin', 'Yancey',
    'York', 'Zeeley', 'Zorn'
]

test_phone_numbers = [
    '6310', '2686', '8370', '7294', '0480', '8213', '1676', '5981', '9820', '9213', '6547', '1629', '7464', '6742',
    '2307', '3152', '3245', '4283', '0144', '4995', '1271', '9220', '9827', '7032', '4855', '7975', '3912', '8340',
    '7934', '4647', '6552', '3079', '6161', '1307', '3158', '1034', '0295', '2317', '7179', '0743', '8588', '7068',
    '2450', '9826', '6458', '0554', '5614', '5106', '5020', '0577', '7277', '6371'
]

test_address_line1s = [
    '907 23rd St.', '972 24th Ave.', '483 24th Ave.', '676 8th Ave.', '984 21st St.', '923 19th St.',
    '734 13th Ave.', '741 22nd Ave.', '45 20th Ave.', '597 16th St.', '259 15th Ave.', '361 3rd Ave.',
    '697 21st St.', '887 18th Ave.', '403 9th Ave.', '684 9th Ave.', '641 19th Ave.', '398 2nd Ave.',
    '752 11th St.', '237 14th St.', '393 8th Ave.', '603 18th Ave.', '601 15th St.', '54 2nd Ave.', '357 20th Ave.',
    '424 10th Ave.', '343 18th St.', '448 13th St.', '743 6th St.', '308 13th St.', '929 15th Ave.', '990 19th St.',
    '27 19th St.', '119 12th St.', '156 15th Ave.', '698 3rd St.', '177 24th Ave.', '663 1st St.', '808 5th Ave.',
    '88 10th St.', '776 15th St.', '927 9th St.', '834 7th Ave.', '786 6th Ave.', '598 22nd St.', '653 2nd St.',
    '162 4th St.', '552 4th Ave.', '118 8th St.', '900 3rd St.', '9 14th St.', '921 9th Ave.'
]

test_address_line2s = [
    None, None, 'Apt. R', 'Apt. 786', 'Apt. K', 'Apt. V', None, 'Apt. X', 'Apt. N', None, None, 'Apt. 789',
    'Apt. O', 'Apt. S', 'Apt. J', 'Apt. 778', None, 'Apt. 662', None, 'Apt. P', 'Apt. 717', 'Apt. E', 'Apt. 402',
    'Apt. W', None, 'Apt. 545', None, None, 'Apt. X', None, None, 'Apt. T', 'Apt. 183', None, None, None,
    'Apt. 104', 'Apt. L', 'Apt. 675', 'Apt. C', 'Apt. D', None, 'Apt. V', None, 'Apt. 846', 'Apt. 804', 'Apt. 365',
    'Apt. 447', 'Apt. 330', None, 'Apt. 765', None
]

test_cities = [
    'Example City',
    'Nowhere',
    'Sigil',
    'Pleasantville'
]

test_states = [
    'XY',
    'XX',
    'ZY',
    'ZX'
]

test_zipcodes = [str(n).zfill(5) for n in range(100)]