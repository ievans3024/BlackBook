__author__ = 'ievans3024'

'''
/user/
  public - some restricted behavior
  can be completely restricted in config
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

/contact/
  restricted - requires being logged in, will only display session user's contacts
  list of contacts
  pagination links
  contact creation template (creates for session user)

/contact/<cid>/
  restricted - must be logged in, must have permission if not session user's contact
  a specific contact
  link to owning user
  link to phone numbers
  link to emails
  link to addresses
  contact update template

/contact/<cid>/phone/
  list of phone numbers for a contact
  link to owning contact
  phone number template (POST to add, DELETE to remove)

/contact/<cid>/email/
  list of emails for a contact
  link to owning contact
  email template (POST to add, DELETE to remove)

/contact/<cid>/address/
  list of addresses for a contact
  link to owning contact
  address template (POST to add, DELETE to remove)

/user/<id>/permissions/
  list of user permissions
  link to owning user
  user permissions update template (POST to add perms, DELETE to remove)

/user/<id>/groups/
  list of user groups
  link to owning user
  user groups update template (POST to add groups, DELETE to remove)

/group/
  list of groups
  group creation template

/group/<id>/
'''

class ModelField(object):
    pass


class Model(object):
    pass


class Contact(Model):
    pass


class ContactAddress(Model):
    pass


class ContactPhoneNumber(Model):
    pass


class Permissible(Model):
    pass


class Group(Permissible):
    pass


class User(Permissible):
    pass


