__author__ = 'ievans3024'

import blackbook.models
from flask_crudsdb import Model, ModelError
from flask_crudsdb.sqlalchemy import Column, Integer, String, SQLAlchemyModel


class Person(blackbook.models.Person, SQLAlchemyModel):

    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    emails = []
    phone_numbers = []
    address_line_1 = Column(String(50), nullable=True)
    address_line_2 = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(2), nullable=True)
    zip_code = Column(String(11), nullable=True)
    country = Column(String(50), nullable=True)

    def __init__(self, data, *args, **kwargs):
        super(Person, self).__init__(data, *args, **kwargs)


class Email(blackbook.models.Email, SQLAlchemyModel):

    __tablename__ = 'emails'


class PhoneNumber(blackbook.models.PhoneNumber, SQLAlchemyModel):

    __tablename__ = 'phonenumbers'

