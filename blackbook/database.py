import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

group_permissions = db.Table('group_permissions',
                             db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                             db.Column('permission', db.String, db.ForeignKey('permission.permission'))
                             )

user_groups = db.Table('user_groups',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
                       )

user_permissions = db.Table('user_permissions',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('permission', db.String, db.ForeignKey('permission.permission'))
                            )

contacts = db.Table('contacts',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
                    )


class JSONObjectEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, JSONObject):
            return o.serializable
        else:
            return super(JSONObjectEncoder, self).default(o)


class JSONObject(object):

    @property
    def mimetype(self):
        return 'application/json'

    @property
    def serializable(self):
        return self.__dict__

    def __init__(self, from_json=None, **props):
        if from_json and isinstance(from_json, (str, bytes, bytearray)):
            props = dict(props, **json.loads(from_json))  # allows props to be supplied defaults

        for k, v in props.items():
            if isinstance(v, dict):
                v = JSONObject(**v)
            self.__setattr__(k, v)

    def __str__(self):
        return json.dumps(self.__dict__, cls=JSONObjectEncoder)

    def __setattr__(self, k, v):
        if isinstance(v, dict):
            v = JSONObject(**v)
        return super(JSONObject, self).__setattr__(k, v)


class JSONSerializable(object):

    @property
    def serializable(self):
        return JSONObject(**self.__dict__)

    @property
    def serialized(self):
        return str(self.serializable)


class Permissible(object):

    def has_permission(self, *permissions, operator='or'):

        ops = {'and', 'or'}

        if operator not in ops:
            operator = 'or'

        permission_check = [p.permission in permissions for p in self.permissions]

        if operator == 'and':
            return all(permission_check)
        else:
            return any(permission_check)


class Resource(JSONSerializable):

    @property
    def public_document(self):
        raise NotImplementedError()


class ResourcePartial(JSONSerializable):

    @property
    def public_document(self):
        raise NotImplementedError()


class User(db.Model, Permissible, Resource):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    display_name = db.Column(db.String)
    contact_info = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=True)
    sessions = db.relationship('Session', backref='user', lazy='dynamic')
    contacts = db.relationship('Contact', secondary=contacts, backref='user', lazy='dynamic')
    permissions = db.relationship('Permission', secondary=user_permissions, backref='user', lazy='dynamic')
    groups = db.relationship('Group', secondary=user_groups, backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def has_permission(self, *permissions, operator='or'):
        has_permission = super(self, User).has_permission(*permissions, operator=operator)
        if not has_permission:
            return any(
                [g.has_permission(*permissions, operator=operator) for g in self.groups]
            )

    @property
    def public_document(self):
        opts = {
            'contact_info': self.contact_info.serializable,
            'contacts': [c.serializable for c in self.contacts]
        }
        return JSONObject(**opts)


class Group(db.Model, Permissible):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    permissions = db.relationship('Permission', secondary=group_permissions, backref='permissible', lazy='dynamic')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Permission(db.Model):
    permission = db.Column(db.String, primary_key=True)

    def __init__(self, permission):
        self.permission = permission


class Contact(db.Model, Resource):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    name_prefix = db.Column(db.String)
    name_first = db.Column(db.String)
    name_middle = db.Column(db.String)
    name_last = db.Column(db.String)
    name_suffix = db.Column(db.String)
    addresses = db.relationship('Address', backref='contact', lazy='dynamic')
    emails = db.relationship('Email', backref='contact', lazy='dynamic')
    phone_numbers = db.relationship('PhoneNumber', backref='contact', lazy='dynamic')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def public_document(self):
        opts = {
            'name': {
                'prefix': self.name_prefix,
                'first': self.name_first,
                'middle': self.name_middle,
                'last': self.name_last,
                'suffix': self.name_suffix
            },
            'emails': [e.public_document for e in self.emails],
            'addresses': [a.public_document for a in self.addresses],
            'phone_numbers': [ph.public_document for ph in self.phone_numbers]
        }
        return JSONObject(**opts)


class Address(db.Model, ResourcePartial):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    label = db.Column(db.String)
    company = db.Column(db.String)
    name = db.Column(db.String)
    street = db.Column(db.String)
    unit = db.Column(db.String)
    city = db.Column(db.String)
    locality = db.Column(db.String)
    postal_code = db.Column(db.String)
    country = db.Column(db.String)
    address_contact = db.Column(db.Integer, db.ForeignKey('contact.id'))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def public_document(self):
        opts = {
            'label': self.label,
            'company': self.company,
            'name': self.name,
            'street': self.street,
            'unit': self.unit,
            'city': self.city,
            'locality': self.locality,
            'postal_code': self.postal_code,
            'country': self.country
        }
        return JSONObject(**opts)


class Email(db.Model, ResourcePartial):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    label = db.Column(db.String)
    address = db.Column(db.String)
    email_contact = db.Column(db.Integer, db.ForeignKey('contact.id'))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def public_document(self):
        return JSONObject(label=self.label, address=self.address)


class PhoneNumber(db.Model, JSONSerializable):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    label = db.Column(db.String)
    number = db.Column(db.String)
    phone_contact = db.Column(db.Integer, db.ForeignKey('contact.id'))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def public_document(self):
        return JSONObject(label=self.label, number=self.number)


class Session(db.Model, Resource):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)
    token = db.Column(db.String)
    session_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def public_document(self):
        return JSONObject(id=self.id, expiry=self.expiry, token=self.token)
