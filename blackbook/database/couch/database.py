import blackbook.database
import blackbook.database.models as common_models
import blackbook.database.couch.models as couch_models
import couchdb
import json
import glob
import os.path

from flask import current_app

__author__ = 'ievans3024'


class CouchDatabase(blackbook.database.Database):
    
    model_map = {
        common_models.Contact: couch_models.Contact,
        common_models.ContactAddress: couch_models.ContactAddress,
        common_models.ContactEmail: couch_models.ContactEmail,
        common_models.ContactPhone: couch_models.ContactPhone,
        common_models.Group: couch_models.Group,
        common_models.User: couch_models.User
    }

    def __init__(self):
        self.dbname = current_app.config.get('COUCHDB_NAME') or 'blackbook'
        try:
            self.server = couchdb.Server(current_app.config.get('COUCHDB_URI') or 'http://localhost:5984')
        except ConnectionRefusedError as e:
            raise blackbook.database.DatabaseUnreachableError(
                'The connection to the database was refused. (Error: {error})\n' +
                'Please ensure option "COUCHDB_URI" is set and correct in config.py'.format(error=e.args[0])
            )
        except couchdb.Unauthorized as e:
            raise blackbook.database.DatabaseUnreachableError(
                'The connection to the database was refused. (Error: {error})\n' +
                'Please ensure options "COUCHDB_USER" and "COUCHDB_PASSWORD" are set and correct in config.py '.format(
                    error=e.args[0]
                )
            )
        except couchdb.HTTPError as e:
            raise blackbook.database.DatabaseUnreachableError(
                'There was an HTTP error when attempting to connect to the database. (Error: {error})'.format(
                    error=e.args[0]
                )
            )
        try:
            self.db = self.server[self.dbname]
        except couchdb.ResourceNotFound:
            self.setup()

    @staticmethod
    def __iterate_design_docs():

        design_doc_path = os.path.join(os.path.dirname(__file__), 'design_docs', '*.json')
        design_docs = glob.glob(design_doc_path)

        for design in design_docs:
            with open(design) as docfile:
                yield json.load(docfile)

    @property
    def is_setup(self):
        try:
            db = self.server[self.dbname]
        except couchdb.ResourceNotFound:
            return False

        for design in self.__iterate_design_docs():
            doc = self.db.get(design.get('_id'))
            if not doc:
                return False
            else:
                if design != doc:
                    return False

        return True

    def create(self, data):
        model = self.model_map.get(data.__class__)
        if model is None:
            raise blackbook.database.InvalidModelError()

        data_dict = data.serialize()
        del data_dict['id']
        data_dict['_id'] = data.id

        doc = model(**data_dict)
        saved = self.db.save(doc)

        if data.id is None:
            data.id = saved[0].id

        return data

    def delete(self, data):
        pass

    def read(self, model, _id=None):
        pass

    def replicate(self, database):
        pass

    def search(self, query, model=None):
        pass

    def setup(self):
        if not self.is_setup:
            try:
                # Try to create new db
                self.db = self.server.create(self.dbname)
            except couchdb.http.PreconditionFailed as e:
                if e.args[0][0] == 'file_exists':
                    # db exists, use it
                    self.db = self.server[self.dbname]
                else:
                    raise blackbook.database.DatabaseError(
                        'There was an error when trying to create database "{dbname}" (Error: {error})'.format(
                            dbname=self.dbname,
                            error=e.args[0]
                        )
                    )
            except couchdb.http.ServerError as e:
                raise blackbook.database.DatabaseError(
                    'There was an error when trying to create database "{dbname}" (Error: {error})\n' +
                    'Please ensure couchdb options are set and correct in config.py'.format(
                        dbname=self.dbname,
                        error=e.args[0]
                    )
                )

            for design in self.__iterate_design_docs():
                existing = self.db.get(design.get('_id'))
                if not existing:
                    # Create new
                    self.db.save(design)
                else:
                    # Update existing
                    for k, v in design.items():
                        if k in existing:
                            # Update existing from spec
                            if existing[k] != v:
                                existing[k] = v
                        else:
                            # Add new from spec
                            existing[k] = v
                    for k in existing:
                        # Delete items not in spec
                        if k not in design:
                            del existing[k]
                    self.db.save(existing)

    def update(self, data):
        pass
