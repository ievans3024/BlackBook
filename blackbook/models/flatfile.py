__author__ = 'ievans3024'

"""
FlatfileDatabase data models
"""

import blackbook.models
from flask_crudsdb import Model, TypeEnforcer


class FlatDatabaseModel(Model):

    def __init__(self, data, *args, pk=None, **kwargs):
        super(FlatDatabaseModel, self).__init__(data)
        self.id = abs(int(pk))
        self.update(data)

    def get_collection_item(self, as_dict=False):
        return super(FlatDatabaseModel, self).get_collection_item(as_dict)

    @staticmethod
    def get_template(as_dict=False):
        return super(FlatDatabaseModel).get_template(as_dict)


class Person(blackbook.models.Person, FlatDatabaseModel):

    first_name = TypeEnforcer(str)
    last_name = TypeEnforcer(str)
    emails = TypeEnforcer(list)
    phone_numbers = TypeEnforcer(list)
    address_line_1 = TypeEnforcer(str)
    address_line_2 = TypeEnforcer(str)
    city = TypeEnforcer(str)
    state = TypeEnforcer(str)
    zip_code = TypeEnforcer(str)
    country = TypeEnforcer(str)

    def __init__(self, data, *args, **kwargs):
        super(Person, self).__init__(data, *args, **kwargs)


class Email(blackbook.models.Email, FlatDatabaseModel):

    email = TypeEnforcer(str)
    email_type = TypeEnforcer(str)
    person = TypeEnforcer(object)

    def __init__(self, data, *args, **kwargs):
        super(Email, self).__init__(data, *args, **kwargs)


class PhoneNumber(FlatDatabaseModel):

    number = TypeEnforcer(str)
    number_type = TypeEnforcer(str)
    person = TypeEnforcer(object)

    def __init__(self, data, *args, **kwargs):
        super(PhoneNumber, self).__init__(data, *args, **kwargs)

models = {
    'Person': Person,
    'Email': Email,
    'PhoneNumber': PhoneNumber
}