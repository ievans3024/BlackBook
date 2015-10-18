import blackbook.database
import couchdb.mapping
import datetime
import re
import uuid

from flask import current_app

__author__ = 'ievans3024'

# TODO: full-text search with couch-lucene (and pylucene?)
#   see: https://wiki.apache.org/couch/Full_text_search


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


class User(Permissible):

    email = couchdb.mapping.TextField()
    display_name = couchdb.mapping.TextField()
    password_hash = couchdb.mapping.TextField()
    contacts = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of Contact.id
    email_verified = couchdb.mapping.BooleanField()
    active = couchdb.mapping.BooleanField()
    last_active = couchdb.mapping.DateTimeField()


class Contact(BaseDocument):
    """A contact being stored in the "book"."""
    user = couchdb.mapping.TextField()  # references User.id
    name_first = couchdb.mapping.TextField()
    name_last = couchdb.mapping.TextField()
    date_created = couchdb.mapping.DateTimeField(default=datetime.datetime.now)
    date_modified = couchdb.mapping.DateTimeField(default=datetime.datetime.now)
    defaults = couchdb.mapping.DictField(
        couchdb.mapping.Mapping.build(
            address=couchdb.mapping.DictField(
                couchdb.mapping.Mapping.build(
                    label=couchdb.mapping.TextField(),
                    line_1=couchdb.mapping.TextField(),
                    line_2=couchdb.mapping.TextField(),
                    city=couchdb.mapping.TextField(),
                    state=couchdb.mapping.TextField(),
                    zip=couchdb.mapping.TextField(),
                    country=couchdb.mapping.TextField()
                )
            ),
            email=couchdb.mapping.DictField(
                couchdb.mapping.Mapping.build(
                    label=couchdb.mapping.TextField(),
                    email=couchdb.mapping.TextField()
                )
            ),
            phone_number=couchdb.mapping.DictField(
                couchdb.mapping.Mapping.build(
                    label=couchdb.mapping.TextField(),
                    number=couchdb.mapping.TextField()
                )
            )
        )
    )
    addresses = couchdb.mapping.ListField(
        couchdb.mapping.DictField(
            couchdb.mapping.Mapping.build(
                label=couchdb.mapping.TextField(),
                line_1=couchdb.mapping.TextField(),
                line_2=couchdb.mapping.TextField(),
                city=couchdb.mapping.TextField(),
                state=couchdb.mapping.TextField(),
                zip=couchdb.mapping.TextField(),
                country=couchdb.mapping.TextField()
            )
        )
    )
    emails = couchdb.mapping.ListField(
        couchdb.mapping.DictField(
            couchdb.mapping.Mapping.build(
                label=couchdb.mapping.TextField(),
                email=couchdb.mapping.TextField()
            )
        )
    )
    phone_numbers = couchdb.mapping.ListField(
        couchdb.mapping.DictField(
            couchdb.mapping.Mapping.build(
                label=couchdb.mapping.TextField(),
                number=couchdb.mapping.TextField()
            )
        )
    )

    @property
    def name(self):
        return " ".join([self.name_first, self.name_last])

    @property
    def rname(self):
        return ", ".join([self.name_last, self.name_first])

    def get_collection_items(self):
        pass


class Group(Permissible):
    """A group for users of the system."""

    name = couchdb.mapping.TextField()
    description = couchdb.mapping.TextField()
    by_name = couchdb.mapping.ViewField("group", "")

    def get_collection_items(self):
        pass


class Session(BaseDocument):
    """Session data for Users"""

    token = couchdb.mapping.TextField(default=uuid.uuid4())
    user = couchdb.mapping.TextField()  # references User.id
    expiry = couchdb.mapping.DateTimeField(
        default=lambda: datetime.datetime.now() + current_app.config.get("PERMANENT_SESSION_LIFETIME") or datetime.timedelta(days=14)
    )
    by_token = couchdb.mapping.ViewField("session", "")
    by_user = couchdb.mapping.ViewField("session", "")

    def get_collection_items(self):
        pass


class User(Permissible):
    """A user of the system."""

    password_hash = couchdb.mapping.TextField()
    name = couchdb.mapping.TextField()
    email = couchdb.mapping.TextField()
    contacts = couchdb.mapping.ListField(couchdb.mapping.TextField())
    by_name = couchdb.mapping.ViewField("user", "")
    by_email = couchdb.mapping.ViewField("user", "")
    by_salt = couchdb.mapping.ViewField("user", "")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_collection_items(self):
        pass

    def set_email(self, db, email):
        users = self.by_email(db, key=email)
        if not users.rows:
            self.email = email
        else:
            raise blackbook.database.ModelError('A user with that email already exists.')

    def set_password(self, db, password):
        hash_method = current_app.config.get('PASSWORD_HASH_METHOD') or 'pbkdf2:sha512'
        salt_length = current_app.config.get('PASSWORD_SALT_LENGTH') or 12
        while True:
            new_hash = generate_password_hash(password, method=hash_method, salt_length=salt_length)
            salt = new_hash.split("$")[1]
            users = self.by_salt(db, key=salt)
            if not users.rows:
                self.password_hash = new_hash
                break
