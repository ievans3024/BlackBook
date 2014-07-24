__author__ = 'ievans3024'


from blackbook2 import app, db


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
        collection = {
            'href': '/api/entry/%d/' % self.id,
            'data': {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'emails': [],
                'phone_numbers': [],
                'address_line_1': self.address_line1,
                'address_line_2': self.address_line2,
                'city': self.city,
                'state': self.state,
                'zip_code': self.zip_code,
                'country': self.country
            }
        }

        return collection


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