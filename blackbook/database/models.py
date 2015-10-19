import collections
import datetime
import re
import werkzeug.security

__author__ = 'ievans3024'

'''

contact
  id
  date_created
  date_modified
  user (<user>)
  name_first
  name_last
  addresses[<contact_address>]
  emails[<contact_email>]
  phone_numbers[<contact_phone>]

contact_address
  id
  date_created
  date_modified
  contact (<contact>)
  label
  line_1
  line_2
  city
  state
  zip
  country

contact_email
  id
  date_created
  date_modified
  contact (<contact>)
  label
  address

contact_phone
  id
  date_created
  date_modified
  contact (<contact>)
  label
  number

group
  id
  date_created
  date_modified
  name
  description
  permissions[<str:permission>]
  groups[<group>]

session
  id
  date_created
  date_modified
  user (<user>)
  token
  expiry

user
  id
  email
  display_name
  password_hash
  date_created
  date_modified
  contacts[<contact>]
  permissions[<str:permission>]
  groups[<group>]
  email_verified
  active
  last_active

/address/
  restricted - must be logged in, must have permission if not session user's contact
  list of addresses for a contact
  link to owning contact
  pagination links (if applicable)
  address creation template

/address/<aid>/
  restricted - must be logged in, must have permission if not session user's contact
  a specific address for a contact
  link to owning contact
  address update template

/contact/
  restricted - requires being logged in, will only display session user's contacts
  list of contacts
  pagination links (if applicable)
  contact creation template (creates for session user)

/contact/<cid>/
  restricted - must be logged in, must have permission if not session user's contact
  a specific contact
  link to owning user
  link to phone numbers
  link to emails
  link to addresses
  pagination links (if applicable)
  contact update template

/email/
  restricted - must be logged in, must have permission if not session user's contact
  list of emails for a contact
  link to owning contact
  pagination links (if applicable)
  email creation template

/email/<eid>/
  restricted - must be logged in, must have permission if not session user's contact
  a specific email for a contact
  link to owning contact
  email update template

/group/
  restricted - must have permission
  list of groups
  pagination links (if applicable)
  group creation template

/group/<id>/
  restricted - must have permission
  a specific group

/phone/
  restricted - must be logged in, must have permission if not session user's contact
  list of phone numbers for a contact
  link to owning contact
  pagination links (if applicable)
  phone number creation template

/phone/<pid>/
  restricted - must be logged in, must have permission if not session user's contact
  a specific phone number for a contact
  link to owning contact
  phone number update template

/session/
  public
  log into the system, check if you are logged in.
  all requests return minimal collection with template
  if session exists and is valid, link to get session user info (i.e., /user/id/)
  login credentials template
  DELETE:
    log out
    does not require any data in body or url args.
    200 OK              Session exists
  GET:
    check if logged in
    does not require any data in body or url args.
    200 OK              Session exists and is valid
    400 Bad Request     Session data not in cookies, malformed, or supplied but does not exist, try POST w/ form data
    419 Auth Timeout    Session exists, but has expired. Create new session with POST
  PUT:
    update logged in session expiry
    does not require any data in body or url args.
    200 OK              Session exists, was not expired, and has updated its expiry.
    400 Bad Request     Session data not in cookies, malformed, or supplied but does not exist, try POST w/ form data
    419 Auth Timeout    Session exists, but has expired. Create new sessoin with POST
  POST:
    log in
    requires login credentials template as x-www-form-urlencoded in POST body.
    201 Created         Login form supplied was valid, session has been created and session token is in cookies.
    400 Bad Request     Incomplete or malformed form data.
    401 Unauthorized    Form data was complete, but invalid credentials.
    429 Too Many        There have been too many attempts in too short of a time.

/user/
  public - some restricted behavior, can be completely restricted in config
  a list of users (requires permission, will only display session user if logged in and no permission)
  user creation template (if session user, requires permission)

/user/<id>/
  restricted - requires permission to view other users, can view self if logged in.
  information about a user
  link to user contacts
  link to user groups
  link to user permissions
  user update template

/user/<id>/contact/
  restricted - requires permission
  list of a specific user's contacts
  pagination links
  link to owning user
  contact creation template (creates for user in uri)

/user/<id>/permissions/
  restricted - must have permission
  list of user permissions
  link to owning user
  pagination links (if applicable)
  user permissions update template (POST to add perms, DELETE to remove)

/user/<id>/groups/
  restricted - must have permission
  list of user groups
  link to owning user
  pagination links (if applicable)
  user groups update template (POST to add groups, DELETE to remove)
'''


class ModelError(BaseException):
    pass


class ModelField(object):
    """Descriptor for Model fields that need to be of a certain type."""

    def __init__(self, cls, nullable=False):
        if isinstance(cls, type):
            self.cls = cls
            self.nullable = bool(nullable)
        else:
            raise TypeError('Parameter "cls" must be a class.')

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self._get_own_name(owner))

    def __set__(self, instance, value):
        if value is None and not self.nullable:
            raise TypeError('Value cannot be None.')
        elif not isinstance(value, self.cls) and not self.nullable:
            raise TypeError(
                'Value must be an instance of {cls}.'.format(
                    cls='.'.join([self.cls.__module__, self.cls.__name__])
                )
            )
        instance.__dict__[self._get_own_name(type(instance))] = value

    def __delete__(self, instance):
        if instance:
            del instance.__dict__[self._get_own_name(type(instance))]

    def _get_own_name(self, owner):
        for attr in dir(owner):
            if getattr(owner, attr) is self:
                return attr


class Array(collections.UserList):
    """A special kind of iterable that only wants to store instances of a certain type."""
    # TODO: Type enforcement
    pass


class ArrayField(ModelField):
    """Descriptor for Model fields that need to be an iterable containing instances of a type."""
    # TODO: deprecate and remove once Array code is in place.
    def __set__(self, instance, value):
        if isinstance(value, collections.Iterable):
            if not all([isinstance(i, self.cls) for i in value]):
                raise ValueError('Value must be an iterable containing {cls} instances.'.format(cls=self.cls.__name__))
            else:
                instance.__dict__[self._get_own_name(type(instance))] = value
        else:
            raise TypeError('Value must be iterable.')


class Model(object):
    """Abstract base class for generic Models"""

    id = ModelField(object, nullable=True)
    date_created = ModelField(datetime.datetime)
    date_modified = ModelField(datetime.datetime)

    def __init__(self, _id=None, ctime=datetime.datetime.now(), mtime=datetime.datetime.now()):
        self.id = _id
        self.date_created = ctime
        self.date_modified = mtime

    def __setattr__(self, key, value):
        # Retain ctime, change mtime to now otherwise
        if key == 'date_created' and self.date_created is not None:
            value = self.date_created
        elif key == 'date_modified':
            value = datetime.datetime.now()
        else:
            self.date_modified = datetime.datetime.now()
        super(Model, self).__setattr__(key, value)

    def serialize(self):
        data = dict(**self.__dict__)
        for k, v in data.items():
            try:
                k_descriptor = getattr(self.__class__, k)
            except AttributeError:
                del data[k]
            else:
                if isinstance(k_descriptor, ArrayField):
                    # ArrayField before ModelField because ArrayField is a subclass of ModelField
                    if isinstance(k_descriptor.cls, Model):
                        data[k] = [i.serialize() for i in v]
                    else:
                        data[k] = list(v)
                elif isinstance(k_descriptor, ModelField):
                    if isinstance(k_descriptor.cls, Model):
                        data[k] = v.serialize()
        return data


class ContactBase(Model):
    """
    Base class for Contact, intentionally empty.
    Only Contact should subclass this.

    Part of a set of empty classes to allow ModelField descriptors to be assigned a model
    whose class may not have been declared yet.
    """
    pass


class ContactAddressBase(Model):
    """
    Base class for ContactAddress, intentionally empty.
    Only ContactAddress should subclass this.

    Part of a set of empty classes to allow ModelField descriptors to be assigned a model
    whose class may not have been declared yet.
    """
    pass


class ContactEmailBase(Model):
    """
    Base class for ContactEmail, intentionally empty.
    Only ContactEmail should subclass this.

    Part of a set of empty classes to allow ModelField descriptors to be assigned a model
    whose class may not have been declared yet.
    """
    pass


class ContactPhoneBase(Model):
    """
    Base class for ContactPhone, intentionally empty.
    Only ContactPhone should subclass this.

    Part of a set of empty classes to allow ModelField descriptors to be assigned a model
    whose class may not have been declared yet.
    """
    pass


class GroupBase(Model):
    """
    Base class for Group, intentionally empty.
    Only Group should subclass this.

    Part of a set of empty classes to allow ModelField descriptors to be assigned a model
    whose class may not have been declared yet.
    """
    pass


class UserBase(Model):
    """
    Base class for User, intentionally empty.
    Only User should subclass this.

    Part of a set of empty classes to allow ModelField descriptors to be assigned a model
    whose class may not have been declared yet.
    """
    pass


class Contact(ContactBase):
    """User contacts"""

    user = ModelField(UserBase)
    name_first = ModelField(str)
    name_last = ModelField(str)
    addresses = ArrayField(ContactAddressBase)
    emails = ArrayField(ContactEmailBase)
    phone_numbers = ArrayField(ContactPhoneBase)

    def __init__(self, user, name_first, name_last, addresses=(), emails=(), phone_numbers=(), **kwargs):
        super(Contact, self).__init__(**kwargs)
        self.user = user
        self.name_first = name_first
        self.name_last = name_last
        self.addresses = addresses
        self.emails = emails
        self.phone_numbers = phone_numbers


class ContactInformation(Model):
    """Contact Information Base Class"""

    contact = ModelField(Contact)
    label = ModelField(str)

    def __init__(self, contact, label, **kwargs):
        super(ContactInformation, self).__init__(**kwargs)
        self.contact = contact
        self.label = label


class ContactAddress(ContactInformation, ContactAddressBase):
    """Contact Address"""

    line_1 = ModelField(str)
    line_2 = ModelField(str)
    city = ModelField(str)
    state = ModelField(str)
    zip = ModelField(str)
    country = ModelField(str)

    def __init__(self, line_1, line_2, city, state, zip_code, *args, country='', **kwargs):
        super(ContactAddress, self).__init__(*args, **kwargs)
        self.line_1 = line_1
        self.line_2 = line_2
        self.city = city
        self.state = state
        self.zip = zip_code
        self.country = country


class ContactEmail(ContactInformation, ContactEmailBase):
    """Contact Email Address"""

    address = ModelField(str)

    def __init__(self, address, *args, **kwargs):
        super(ContactEmail, self).__init__(*args, **kwargs)
        self.address = address


class ContactPhone(ContactInformation, ContactPhoneBase):
    """Contact Phone Number"""

    number = ModelField(str)

    def __init__(self, number, *args, **kwargs):
        super(ContactPhone, self).__init__(*args, **kwargs)
        self.number = number


class Permissible(Model):
    """A model that is part of a permissions hierarchy"""

    permissions = ArrayField(str)
    groups = ArrayField(GroupBase)

    def __init__(self, permissions=(), groups=(), **kwargs):
        super(Permissible, self).__init__(**kwargs)
        self.permissions = permissions
        self.groups = groups

    def compile_permissions(self, permissions=None, groups_checked=None):
        if not permissions:
            permissions = self.permissions
        else:
            permissions = [p for p in permissions if p not in self.permissions]

        if not groups_checked:
            groups_checked = []

        if len(self.groups):
            for group in self.groups:
                if group.id not in groups_checked:
                    groups_checked.append(group.id)
                    permissions, groups_checked = group.compile_permissions(
                        permissions=permissions,
                        groups_checked=groups_checked
                    )
        return permissions, groups_checked

    def has_permission(self, *perms, operator='and'):
        ops = {'and', 'or'}
        if operator not in ops:
            raise ValueError('Parameter "operator" must be one of {ops}'.format(ops=str(ops)))
        else:
            if not len(perms):
                # If no perms are provided, assume nobody has permission
                return False
            permissions = self.compile_permissions()
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

            if operator == 'or':
                return any([permission_matches.get(perm) for perm in perms])
            if operator == 'and':
                return all([permission_matches.get(perm) for perm in perms])


class Group(Permissible, GroupBase):
    """A User group containing permissions"""

    name = ModelField(str)
    description = ModelField(str)

    def __init__(self, name, description, **kwargs):
        super(Group, self).__init__(**kwargs)
        self.name = name
        self.description = description


class User(Permissible, UserBase):
    """A User"""

    email = ModelField(str)
    display_name = ModelField(str)
    password_hash = ModelField(str)
    contacts = ArrayField(ContactBase)
    email_verified = ModelField(bool)
    active = ModelField(bool)
    last_active = ModelField(datetime.datetime, nullable=True)

    def __init__(self, email, display_name, password_hash='',
                 contacts=(), email_verified=False, active=False, last_active=None, **kwargs):
        super(User, self).__init__(**kwargs)
        self.email = email
        self.display_name = display_name
        self.password_hash = password_hash
        self.contacts = contacts
        self.email_verified = email_verified
        self.active = active
        self.last_active = last_active

    def set_password(self, password, method='pbkdf2:sha512', salt_length=12):
        self.password_hash = werkzeug.security.generate_password_hash(password, method=method, salt_length=salt_length)

    def check_password(self, password):
        return werkzeug.security.check_password_hash(self.password_hash, password)
