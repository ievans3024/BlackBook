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


def init_db(database, app):
    database.init_app(app)
    database.create_all(app=app)
    # create default user


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


class User(db.Model, Permissible):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    display_name = db.Column(db.String)
    contact_info = db.Column(db.Integer, db.ForeignKey('contact.id'))
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


class Contact(db.Model):
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


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    label = db.Column(db.String)
    company = db.Column(db.String)
    street = db.Column(db.String)
    apt = db.Column(db.String)
    city = db.Column(db.String)
    locality = db.Column(db.String)
    postal_code = db.Column(db.String)
    country = db.Column(db.String)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    label = db.Column(db.String)
    address = db.Column(db.String)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    label = db.Column(db.String)
    number = db.Column(db.String)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)
    token = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
