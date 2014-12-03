__author__ = 'ievans3024'

import blackbook.models
from flask_crudsdb import Model, ModelError
from flask_sqlalchemy import Model as SQLAModel


class SQLAlchemyModel(SQLAModel, Model):

    def get_collection_item(self, as_dict=False):
        return super(SQLAlchemyModel, self).get_collection_item(as_dict)

    @staticmethod
    def get_template(as_dict=False):
        return super(SQLAlchemyModel).get_template(as_dict)


class Person(blackbook.models.Person, SQLAlchemyModel):
    pass


class Email(blackbook.models.Email, SQLAlchemyModel):
    pass


class PhoneNumber(blackbook.models.PhoneNumber, SQLAlchemyModel):
    pass

