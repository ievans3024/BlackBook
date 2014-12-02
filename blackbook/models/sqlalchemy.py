__author__ = 'ievans3024'

from blackbook.models import GenericModel
from collection_json import Data, Item, Template
from flask_crudsdb import Model, ModelError
from flask_sqlalchemy import Model as SQLAModel


class SQLAlchemyModel(SQLAModel, GenericModel, Model):

    def __init__(self, data, *args, **kwargs):
        super(SQLAlchemyModel, self).__init__(data, *args, **kwargs)

    def get_collection_item(self, as_dict=False):
        return super(SQLAlchemyModel, self).get_collection_item(as_dict)

    @staticmethod
    def get_template(as_dict=False):
        return super(SQLAlchemyModel).get_template(as_dict)