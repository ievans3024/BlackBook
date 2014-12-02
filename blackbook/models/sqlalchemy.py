__author__ = 'ievans3024'

from collection_json import Data, Item, Template
from flask_crudsdb import Model, ModelError
from flask_sqlalchemy import Model as SQLAModel


class SQLAlchemyModel(SQLAModel, Model):

    def get_collection_item(self, as_dict=False):
        return super(SQLAlchemyModel, self).get_collection_item(as_dict)

    @staticmethod
    def get_template(as_dict=False):
        return super(SQLAlchemyModel).get_template(as_dict)


class Person(SQLAlchemyModel):
    pass


class Email(SQLAlchemyModel):
    pass


class PhoneNumber(SQLAlchemyModel):
    pass

