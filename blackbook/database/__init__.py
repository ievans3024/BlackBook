__author__ = 'ievans3024'


class Database(object):
    """Database wrapper, base class"""

    def __init__(self, app):
        """Constructor for Database"""
        self.app = app
        self.database = {}
        self.models = {}

    def new(self):
        pass

    def edit(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def search(self):
        pass

    def generate_test_db(self):
        pass