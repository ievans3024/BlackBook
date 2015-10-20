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
    type = couchdb.mapping.TextField()

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

    @property
    def owner(self):
        """
        Retrieve the ID(s) of owner documents

        Implementations should always return a list, even if
        there is no owner.

        :return:
        """
        raise NotImplementedError()

    @property
    def owns(self):
        """
        Retrief the ID(s) of owned documents

        Implementations should always return a list, even if
        this document doesn't own any others.

        :return:
        """
        raise NotImplementedError()
    
    def dereference(self, key):
        """
        Remove a reference to another document.
        
        Implementations should know where references to other documents are stored
        and iterate over the possibilities appropriately to remove the provided reference.
        
        :return:
        """
        raise NotImplementedError()


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

    @property
    def owner(self):
        return [self.user]

    @property
    def owns(self):
        return self.addresses + self.emails + self.phone_numbers

    def dereference(self, key):
        for l in (self.addresses, self.emails, self.phone_numbers):
            if key in l:
                l.pop(l.index(key))


class ContactInformation(CouchModel):

    contact = couchdb.mapping.TextField()  # Contact.id
    label = couchdb.mapping.TextField()

    @property
    def owner(self):
        return [self.contact]

    @property
    def owns(self):
        return []


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

    @property
    def owner(self):
        return []

    @property
    def owns(self):
        return []

    def dereference(self, key):
        if key in self.groups:
            self.groups.pop(self.groups.index(key))


class Group(Permissible):

    name = couchdb.mapping.TextField()
    description = couchdb.mapping.TextField()

    all = couchdb.mapping.ViewField('group', '')

    @property
    def owner(self):
        return []

    @property
    def owns(self):
        return []


class Session(CouchModel):
    user = couchdb.mapping.TextField()
    token = couchdb.mapping.TextField()
    expiry = couchdb.mapping.DateTimeField(
        default=lambda: datetime.datetime.now() + datetime.datetime.timedelta(**LOGIN_TIMEOUT)
    )

    @property
    def owner(self):
        return [self.user]

    @property
    def owns(self):
        return []


class User(Permissible):

    email = couchdb.mapping.TextField()
    display_name = couchdb.mapping.TextField()
    password_hash = couchdb.mapping.TextField()
    contacts = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of Contact.id
    email_verified = couchdb.mapping.BooleanField()
    active = couchdb.mapping.BooleanField()
    last_active = couchdb.mapping.DateTimeField()

    all = couchdb.mapping.ViewField('user', '')

    @property
    def owner(self):
        return []

    @property
    def owns(self):
        owns = super(User, self).owns
        owns = owns + self.contacts
        return owns

    def dereference(self, key):
        if key in self.contacts:
            self.contacts.pop(self.contacts.index(key))
