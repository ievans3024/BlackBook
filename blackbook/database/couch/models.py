import blackbook.database
import couchdb.mapping
import datetime
import uuid

from flask import current_app

__author__ = 'ievans3024'

# TODO: full-text search with couch-lucene (and pylucene?)
#   see: https://wiki.apache.org/couch/Full_text_search

LOGIN_TIMEOUT = current_app.config.get('LOGIN_TIMEOUT') or {'days': 14}


class CouchModel(couchdb.mapping.Document):

    id = couchdb.mapping.TextField(default=uuid.uuid4)
    date_created = couchdb.mapping.DateTimeField(default=datetime.datetime.now)
    date_modified = couchdb.mapping.DateTimeField(default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        super(CouchModel, self).__init__(*args, **kwargs)
        self.type = self.__class__.__name__.lower()

    def __setattr__(self, key, value):
        if key == 'date_created' and self.date_created is not None:
            value = self.date_created
        elif key == 'date_modified':
            value = datetime.datetime.now()
        else:
            self.date_modified = datetime.datetime.now()
        super(CouchModel, self).__setattr__(key, value)


class Contact(CouchModel):

    user = couchdb.mapping.TextField()  # User.id
    name_first = couchdb.mapping.TextField()
    name_last = couchdb.mapping.TextField()
    addresses = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of ContactAddress.id
    emails = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of ContactEmail.id
    phone_numbers = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of ContactPhone.id

    # Views
    all = couchdb.mapping.ViewField("contact", "")
    by_name = couchdb.mapping.ViewField("contact", "")
    by_surname = couchdb.mapping.ViewField("contact", "")
    by_user = couchdb.mapping.ViewField("contact", "")


class ContactInformation(CouchModel):

    contact = couchdb.mapping.TextField()  # Contact.id
    label = couchdb.mapping.TextField()


class ContactAddress(ContactInformation):

    line_1 = couchdb.mapping.TextField()
    line_2 = couchdb.mapping.TextField()
    city = couchdb.mapping.TextField()
    state = couchdb.mapping.TextField()
    zip = couchdb.mapping.TextField()
    country = couchdb.mapping.TextField()


class ContactEmail(ContactInformation):

    address = couchdb.mapping.TextField()


class ContactPhone(ContactInformation):

    number = couchdb.mapping.TextField()


class Permissible(CouchModel):

    permissions = couchdb.mapping.ListField(couchdb.mapping.TextField())
    groups = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of Group.id


class Group(Permissible):

    name = couchdb.mapping.TextField()
    description = couchdb.mapping.TextField()


class Session(CouchModel):
    user = couchdb.mapping.TextField()
    token = couchdb.mapping.TextField()
    expiry = couchdb.mapping.DateTimeField(
        default=lambda: datetime.datetime.now() + datetime.datetime.timedelta(**LOGIN_TIMEOUT)
    )


class User(Permissible):

    email = couchdb.mapping.TextField()
    display_name = couchdb.mapping.TextField()
    password_hash = couchdb.mapping.TextField()
    contacts = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of Contact.id
    email_verified = couchdb.mapping.BooleanField()
    active = couchdb.mapping.BooleanField()
    last_active = couchdb.mapping.DateTimeField()