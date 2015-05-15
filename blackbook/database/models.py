__author__ = 'ievans3024'

# TODO: full-text search with couchdb-lucene (and pylucene?)
#   see: https://wiki.apache.org/couchdb/Full_text_search

import re

from couchdb.mapping import DateTimeField, DictField, Document, ListField, Mapping, TextField, ViewField
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash


class Permissible(Document):
    """A document that is part of a permissions hierarchy."""

    permissions = ListField(TextField())  # list of permission node strings
    groups = ListField(TextField())  # list of Group ids

    def get_permissions(self, db, permissions=None, groups_checked=None):
        """
        Get a compiled list of permissions provided in this document's permission hierarchy.
        :param db: The Database to get permission information from.
        :param permissions: A list of permission string(s) discovered so far.
            Used internally by this method during recursion to compile a complete, non-duplicate list.
        :param groups_checked: A list of Group ids checked so far.
            Used internally by this method during recursion to prevent duplicate group checking and ancestry loops.
        :return permissions, groups: A list of permissions discovered and a list of groups checked.
        """
        if not permissions:
            permissions = self.permissions
        else:
            permissions = [p for p in self.permissions if p not in permissions]

        # need to do this outside the next if block because
        # it's possible to check perms on a groupless item
        # from the start and we need to consistently return
        # groups_checked with or without checking any groups.
        if not groups_checked:
            groups_checked = []

        if self.groups:
            for group in self.groups:
                if group not in groups_checked:
                    groups_checked.append(group)
                    g = Permissible.load(db, group)
                    permissions, groups_checked = g.get_permissions(
                        db,
                        permissions=permissions,
                        groups_checked=groups_checked
                    )

        return permissions, groups_checked

    def has_permission(self, db, *perms, operation="or"):
        """
        See if this document has permission somewhere in its hierarchy
        :param db: The Database to get permission information from.
        :param perms: Permission string(s) to check against.
        :param operation: A logical operator to apply to permission checking.
            "or" = any of the supplied permission nodes
            "and" = all of the supplied permission nodes
        :return: True if document has necessary permissions, False if document does not.
        """
        operations = {"or", "and"}

        # compile a collection of all permissions and groups provided in the hierarchy
        # need to do this for situations where multiple required permissions span the hierarchy
        permissions, groups = self.get_permissions(db)

        if str(operation).lower() in operations:
            permission_matches = {}
            for perm in perms:
                for permission in permissions:
                    # match will be truthy:
                    # permission = "one"
                    # perm is "one.two", "one.three", "one.two.three", "one.two.four", etc.

                    # match will not be truthy:
                    # permission = "one.two"
                    # perm is "one", "one.three", "four.one.two", "four.five.six", etc.

                    # need to escape separator to avoid false positives
                    regex = re.compile("^" + permission.replace(".", "\."))
                    match = regex.match(perm)
                    if match:
                        permission_matches[perm] = bool(match)
                        break  # only need to look for the first matching permission

            if operation == "or":
                return any([permission_matches.get(perm) for perm in perms])
            if operation == "and":
                return all([permission_matches.get(perm) for perm in perms])

        else:
            raise ValueError("Parameter 'operator' must be in {ops}".format(ops=operations))


class TypedDocument(Document):
    """A document that has a type and subtype."""

    type = TextField()
    subtype = TextField()

    def __init__(self, *args, _type=None, subtype=None, **kwargs):
        super(TypedDocument, self).__init__(*args, **kwargs)
        self.type = _type or self.__class__.__name__.lower()
        self.subtype = subtype or self.__class__.__name__.lower()


class Contact(TypedDocument):
    """A contact being stored in the "book"."""
    user = TextField()  # references User.id
    name_first = TextField()
    name_last = TextField()
    date_created = DateTimeField(default=datetime.now)
    date_modified = DateTimeField(default=datetime.now)
    defaults = DictField(
        Mapping.build(
            address=DictField(
                Mapping.build(
                    label=TextField(),
                    line_1=TextField(),
                    line_2=TextField(),
                    city=TextField(),
                    state=TextField(),
                    zip=TextField(),
                    country=TextField()
                )
            ),
            email=DictField(
                Mapping.build(
                    label=TextField(),
                    email=TextField()
                )
            ),
            phone_number=DictField(
                Mapping.build(
                    label=TextField(),
                    number=TextField()
                )
            )
        )
    )
    addresses = ListField(
        DictField(
            Mapping.build(
                label=TextField(),
                line_1=TextField(),
                line_2=TextField(),
                city=TextField(),
                state=TextField(),
                zip=TextField(),
                country=TextField()
            )
        )
    )
    emails = ListField(
        DictField(
            Mapping.build(
                label=TextField(),
                email=TextField()
            )
        )
    )
    phone_numbers = ListField(
        DictField(
            Mapping.build(
                label=TextField(),
                number=TextField()
            )
        )
    )
    by_address = ViewField("contact", "")
    by_email = ViewField("contact", "")
    by_name = ViewField("contact", "")
    by_phone_number = ViewField("contact", "")
    by_surname = ViewField("contact", "")
    by_user = ViewField("contact", "")

    @property
    def name(self):
        return " ".join([self.name_first, self.name_last])

    @property
    def rname(self):
        return ", ".join([self.name_last, self.name_first])


class Group(Permissible, TypedDocument):
    """A group for users of the system."""

    name = TextField()
    description = TextField()
    by_name = ViewField("group", "")


class Session(TypedDocument):
    """Session data for Users"""

    token = TextField()
    user = TextField()  # references User.id
    expiry = DateTimeField(
        default=lambda: datetime.now() + current_app.config.get("PERMANENT_SESSION_LIFETIME") or timedelta(days=14)
    )
    by_token = ViewField("session", "")
    by_user = ViewField("session", "")


class User(Permissible, TypedDocument):
    """A user of the system."""

    password_hash = TextField()
    name = TextField()
    email = TextField()
    contacts = ListField(TextField())
    by_name = ViewField("user", "")
    by_email = ViewField("user", "")
    by_salt = ViewField("user", "")

    def set_password(self, db, password):
        while True:
            new_hash = generate_password_hash(password, method="pbkdf2:sha512", salt_length=12)
            salt = new_hash.split("$")[1]
            users = self.by_salt(db, key=salt)
            if not users.rows:
                self.password_hash = new_hash
                break

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
