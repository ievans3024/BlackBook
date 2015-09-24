import couchdb.mapping
import datetime
import re
import uuid

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

__author__ = 'ievans3024'

# TODO: full-text search with couch-lucene (and pylucene?)
#   see: https://wiki.apache.org/couch/Full_text_search


class BaseDocument(couchdb.mapping.Document):

    creation_time = couchdb.mapping.DateTimeField(default=datetime.datetime.now)
    modification_time = couchdb.mapping.DateTimeField(default=datetime.datetime.now)
    types = couchdb.mapping.ListField(couchdb.mapping.TextField())

    # Set the document id here to prevent generating duplicate docs
    # see https://pythonhosted.org/CouchDB/client.html#couchdb.client.Database.save
    def __init__(self, id=uuid.uuid4(), **kwargs):
        super(BaseDocument, self).__init__(id=id, **kwargs)
        self.types = [c.__name__ for c in self.__class__.__mro__ if issubclass(c, BaseDocument)]

    def __setattr__(self, key, value):
        if key == 'creation_time' and self.creation_time is not None:
            # Prevent overwriting existing creation time
            value = self.creation_time
        elif key == 'modification_time':
            # Prevent setting modification time to anything other than now
            value = datetime.datetime.now()
        super(BaseDocument, self).__setattr__(key, value)


class Permissible(BaseDocument):
    """A document that is part of a permissions hierarchy."""

    permissions = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of permission node strings
    groups = couchdb.mapping.ListField(couchdb.mapping.TextField())  # list of Group ids

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

        # if no permissions are supplied,
        # we assume nobody can have permission
        if not perms:
            return False

        # compile a collection of all permissions and groups provided in the hierarchy
        # need to do this for situations where multiple required permissions span the hierarchy
        permissions, groups = self.get_permissions(db)

        if str(operation).lower() in operations:
            permission_matches = {}
            for perm in perms:
                permission_matches[perm] = False  # assume no permission until permission is found
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
                        permission_matches[perm] = True
                        break  # only need to look for the first matching permission

            if operation == "or":
                return any([permission_matches.get(perm) for perm in perms])
            if operation == "and":
                return all([permission_matches.get(perm) for perm in perms])

        else:
            raise ValueError("Parameter 'operator' must be one of {ops}".format(ops=operations))


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
    all = couchdb.mapping.ViewField("contact", "")
    by_address = couchdb.mapping.ViewField("contact", "")
    by_email = couchdb.mapping.ViewField("contact", "")
    by_name = couchdb.mapping.ViewField("contact", "")
    by_phone_number = couchdb.mapping.ViewField("contact", "")
    by_surname = couchdb.mapping.ViewField("contact", "")
    by_user = couchdb.mapping.ViewField("contact", "")

    @property
    def name(self):
        return " ".join([self.name_first, self.name_last])

    @property
    def rname(self):
        return ", ".join([self.name_last, self.name_first])


class Group(Permissible):
    """A group for users of the system."""

    name = couchdb.mapping.TextField()
    description = couchdb.mapping.TextField()
    by_name = couchdb.mapping.ViewField("group", "")


class Session(BaseDocument):
    """Session data for Users"""

    token = couchdb.mapping.TextField(default=uuid.uuid4())
    user = couchdb.mapping.TextField()  # references User.id
    expiry = couchdb.mapping.DateTimeField(
        default=lambda: datetime.datetime.now() + current_app.config.get("PERMANENT_SESSION_LIFETIME") or datetime.timedelta(days=14)
    )
    by_token = couchdb.mapping.ViewField("session", "")
    by_user = couchdb.mapping.ViewField("session", "")


class User(Permissible):
    """A user of the system."""

    password_hash = couchdb.mapping.TextField()
    name = couchdb.mapping.TextField()
    email = couchdb.mapping.TextField()
    contacts = couchdb.mapping.ListField(couchdb.mapping.TextField())
    by_name = couchdb.mapping.ViewField("user", "")
    by_email = couchdb.mapping.ViewField("user", "")
    by_salt = couchdb.mapping.ViewField("user", "")

    def set_email(self, db, email):
        while True:
            users = self.by_email(db, key=email)
            if not users.rows:
                self.email = email
                break

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

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
