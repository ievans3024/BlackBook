import blackbook.database
import couchdb.mapping as mapping
import datetime
import uuid

from flask import current_app

__author__ = 'ievans3024'

# TODO: full-text search with couch-lucene (and pylucene?)
#   see: https://wiki.apache.org/couch/Full_text_search

LOGIN_TIMEOUT = current_app.config.get('LOGIN_TIMEOUT') or {'days': 14}


class CouchModel(mapping.Document):

    id = mapping.TextField(default=uuid.uuid4)
    date_created = mapping.DateTimeField(default=datetime.datetime.now)
    date_modified = mapping.DateTimeField(default=datetime.datetime.now)
    type = mapping.TextField()

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
    

class Permissible(CouchModel):

    permissions = mapping.ListField(mapping.TextField())
    groups = mapping.ListField(mapping.TextField())  # list of Group.id


class Group(Permissible):

    name = mapping.TextField()
    description = mapping.TextField()

    all = mapping.ViewField('group', '')


class User(Permissible):

    # Properties
    email = mapping.TextField()
    display_name = mapping.TextField()
    password_hash = mapping.TextField()
    email_verified = mapping.BooleanField()
    active = mapping.BooleanField()
    last_active = mapping.DateTimeField(),
    addresses = mapping.ListField(
        mapping.DictField(
            mapping.Mapping.build(
                label=mapping.TextField(),
                street=mapping.TextField(),
                apt=mapping.TextField(),
                city=mapping.TextField(),
                locality=mapping.TextField(),
                postal_code=mapping.TextField(),
                country=mapping.TextField()
            )
        )
    )
    emails = mapping.ListField(
        mapping.DictField(
            mapping.Mapping.build(
                label=mapping.TextField(),
                address=mapping.TextField(),
            )
        )
    )
    phone_numbers = mapping.ListField(
        mapping.DictField(
            mapping.Mapping.build(
                label=mapping.TextField(),
                number=mapping.TextField(),
            )
        )
    )
    contacts = mapping.ListField(
        mapping.DictField(
            mapping.Mapping.build(
                name_first=mapping.TextField(),
                name_last=mapping.TextField(),
                addresses=mapping.ListField(
                    mapping.DictField(
                        mapping.Mapping.build(
                            label=mapping.TextField(),
                            street=mapping.TextField(),
                            apt=mapping.TextField(),
                            city=mapping.TextField(),
                            locality=mapping.TextField(),
                            postal_code=mapping.TextField(),
                            country=mapping.TextField()
                        )
                    )
                ),
                emails=mapping.ListField(
                    mapping.DictField(
                        mapping.Mapping.build(
                            label=mapping.TextField(),
                            address=mapping.TextField(),
                        )
                    )
                ),
                phone_numbers=mapping.ListField(
                    mapping.DictField(
                        mapping.Mapping.build(
                            label=mapping.TextField(),
                            number=mapping.TextField(),
                        )
                    )
                )
            )
        )
    )
    sessions = mapping.ListField(
        mapping.DictField(
            mapping.Mapping.build(
                token=mapping.TextField(),
                expiry=mapping.DateTimeField(
                    default=lambda: datetime.datetime.now() + datetime.timedelta(**LOGIN_TIMEOUT)
                )
            )
        )
    )

    # Views
    all = mapping.ViewField('user', '')
