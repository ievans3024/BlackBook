__author__ = 'ievans3024'

from collection_json import Collection, Item, Template, Error, Link
from math import ceil as _ceil


class Database(object):
    """
A base class for database wrappers.

    Consider this class to be a skeleton to model database wrappers from. Docstrings in this class provide helpful
    information for writing subclasses that will behave in a consistent way for the flask app to interface with.

    This system allows developers to abstract away quirks for their particular database interface without having to
    heavily modify the application logic directly. This also allows the application to be easily extended to support
    more database types as it is developed.
    """

    HTTP_ERRORS = {
        404: Error(code="404", message="There is no Person with that id.", title="Not Found")
    }

    # TODO: Force usage of self.models['ModelName'] and make these private members?
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

    def __init__(self, app):
        """
        Database wrapper constructor
        Implementations should create self.app (containing "app" param,) self.database, and self.models
        :param app: An instance of Flask
        :return:
        """
        raise NotImplementedError()

    def create(self, data):
        """
        Create a new Person entry
        :param data: A dict containing data for the new Person entry. See Database.Person.get_collection_template
        :return: The Person entry created, represented as a CollectionPlusJSON instance.
        """
        raise NotImplementedError()

    def update(self, id, data):
        """
        Update an existing Person entry
        Implementations should return Database.HTTP_ERRORS[404] if Person with id does not exist.
        :param id: The id of the existing person entry to update.
        :param data: A dict containing data to update the Person entry with. See Database.Person.get_collection_template
        :return: The Person entry updated, represented as a CollectionPlusJSON instance.
        """
        raise NotImplementedError()

    def read(self, id=None, page=1, per_page=5):
        """
        Read an existing Person entry, or read paginated list of all Person entries
        Implementations should use CollectionPlusJSON.paginate to paginate the list of Person entries
        :param id: The id of the existing person entry to read. (optional, default is None)
        :param page: The page of the paginated listing to get. (optional, default is 1, ignored if id is provided)
        :param per_page: The number of entries to list per page. (optional, default is 5, ignored if id is provided)
        :return: CollectionPlusJSON instance representing the Person or list of Person entries.
        """
        raise NotImplementedError()

    def delete(self, id):
        """
        Delete an existing Person entry
        :param id: The id of the existing Person entry to delete
        :return: The Person that was deleted, represented as a CollectionPlusJSON instance
        """
        raise NotImplementedError()

    def search(self, data):
        """
        Search the database records for certain criteria
        :param data: A dict containing query data. This should match the format of CollectionPlusJSON "queries" section.
        :return: The matching entries represented as a CollectionPlusJSON instance.
        """
        raise NotImplementedError()

    def generate_test_db(self):
        """
        Generate test data to demonstrate or test the application.
        This method should create a separate, temporary database, instead of overwriting production data.
        :raises: RunTimeError if app config key 'TESTING' does not have a value of True.
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def paginate(collection, endpoint='', uri_template='{endpoint_uri}?page={page}&per_page={per_page}',
                 page=None, per_page=5, leading=2, trailing=2):
        """
        Paginate this collection into a list of collections representing "pages" of this collection.
        :type collection: collection_json.Collection
        :type endpoint: str
        :type uri_template: str
        :type page: int
        :type per_page: int
        :type leading: int
        :type trailing: int
        :param endpoint: The URI for this resource.
        :param uri_template: A string providing a template for paginated URI structure. May include the following keys:
            "{endpoint_uri}" - This will evaluate to the value of the 'endpoint' param.
            "{page}" - The page number will be inserted here.
            "{per_page}" - The number of items to display per page will be inserted here.
        :param page: The page number to get.
        :param per_page: The number of items per page for this representation.
        :param leading: The number of leading pages before a page to add to its "links".
        :param trailing: The number of trailing pages after a page to add to its "links".
        :return tuple: A tuple of Collections representing ordered subsets of this collection. If the
            page parameter is supplied, the tuple will contain a single Collection representing one
            particular subset ("page") from this collection.

        """

        def sanitize_int(o, default=None):
            if type(o) is not int:
                try:
                    number = abs(int(o))
                except (ValueError, TypeError) as e:
                    if default is not None:
                        number = default
                    else:
                        raise e
            else:
                number = o
            return number

        per_page = sanitize_int(per_page, default=5)
        if page is not None:
            page = sanitize_int(page, default=1)
        pages = []
        number_of_pages = int(_ceil(len(collection.items) / per_page))

        def assemble_page():
            page_index_begin = ((page * per_page) - per_page)
            page_index_end = (page * per_page)
            new_page = Collection(href=collection.href, items=collection.items[page_index_begin:page_index_end])
            if collection.error:
                new_page.error = collection.error
            if collection.links:
                new_page.links = collection.links
            if collection.queries:
                new_page.queries = collection.qeuries
            if collection.template:
                new_page.template = collection.template
            if page > 1:
                new_page.links.append(Link(
                    uri_template.format(endpoint_uri=endpoint, page=1, per_page=per_page),
                    'first',
                    prompt='First'
                ))

                new_page.links.append(Link(
                    uri_template.format(endpoint_uri=endpoint, page=(page - 1), per_page=per_page),
                    'prev',
                    prompt='Previous'
                ))

                if page - trailing > 0:
                    new_page.links.append(Link(
                        '',
                        'skip',
                        prompt='…'
                    ))

                for lead_page in range(trailing, 0, -1):
                    page_num = page - lead_page
                    if page_num > 0 and page_num != page:
                        new_page.links.append(Link(
                            uri_template.format(endpoint_uri=endpoint, page=page_num, per_page=per_page),
                            'more',
                            prompt=str(page_num)
                        ))

            new_page.links.append(Link(
                uri_template.format(endpoint_uri=endpoint, page=page, per_page=per_page),
                'self',
                prompt=str(page)
            ))

            if page <= number_of_pages:
                for trail_page in range(1, leading + 1):
                    page_num = page + trail_page
                    if page_num <= number_of_pages:
                        new_page.links.append(Link(
                            uri_template.format(endpoint_uri=endpoint, page=page_num, per_page=per_page),
                            'more',
                            prompt=str(page_num)
                        ))

                if page + trailing < number_of_pages:
                    new_page.links.append(Link(
                        '',
                        'skip',
                        prompt='…'
                    ))

                if page <= number_of_pages:
                    new_page.links.append(Link(
                        uri_template.format(endpoint_uri=endpoint, page=page + 1, per_page=per_page),
                        'next',
                        prompt='Next'
                    ))

                    new_page.links.append(Link(
                        uri_template.format(endpoint_uri=endpoint, page=number_of_pages, per_page=per_page),
                        'last',
                        prompt='Last'
                    ))
            return new_page

        if page:
            pages.append(assemble_page())
        else:
            page = 1
            while page <= number_of_pages:
                pages.append(assemble_page())
                page += 1
        return tuple(pages)


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

test_address_line_1s = [
    '907 23rd St.', '972 24th Ave.', '483 24th Ave.', '676 8th Ave.', '984 21st St.', '923 19th St.',
    '734 13th Ave.', '741 22nd Ave.', '45 20th Ave.', '597 16th St.', '259 15th Ave.', '361 3rd Ave.',
    '697 21st St.', '887 18th Ave.', '403 9th Ave.', '684 9th Ave.', '641 19th Ave.', '398 2nd Ave.',
    '752 11th St.', '237 14th St.', '393 8th Ave.', '603 18th Ave.', '601 15th St.', '54 2nd Ave.', '357 20th Ave.',
    '424 10th Ave.', '343 18th St.', '448 13th St.', '743 6th St.', '308 13th St.', '929 15th Ave.', '990 19th St.',
    '27 19th St.', '119 12th St.', '156 15th Ave.', '698 3rd St.', '177 24th Ave.', '663 1st St.', '808 5th Ave.',
    '88 10th St.', '776 15th St.', '927 9th St.', '834 7th Ave.', '786 6th Ave.', '598 22nd St.', '653 2nd St.',
    '162 4th St.', '552 4th Ave.', '118 8th St.', '900 3rd St.', '9 14th St.', '921 9th Ave.'
]

test_address_line_2s = [
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