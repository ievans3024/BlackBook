import couchdb
import json
import glob
import os.path

from flask import current_app

__author__ = 'ievans3024'

server = couchdb.Server(current_app.config.get('COUCHDB_URI') or 'http://localhost:5984')
dbname = current_app.config.get('DB_NAME') or 'blackbook'

# Attempt to connect to the database, create it if it doesn't exist
try:
    db = server[dbname]
except couchdb.ResourceNotFound:
    try:
        db = server.create(dbname)
    except couchdb.http.ServerError as e:
        raise ValueError(
            'CouchDB returned an error when trying to create database "{dbname}" (Error {error}.)\n' +
            'Please ensure options "COUCHDB_URI" and "DB_NAME" are set and correct in config.py'.format(
                dbname=dbname,
                error=e.args[0]
            )
        )


def setup(db=db):
    """
    Place the database schema in the database
    :param db: The Database to place the schema into, defaults to current app configuration.
    :return:
    """
    design_doc_path = os.path.join(os.path.dirname(__file__), 'design_docs', '*.json')
    design_docs = glob.glob(design_doc_path)

    for design in design_docs:
        with open(design) as docfile:
            doc = json.load(docfile)
            existing = db.get(doc.get('_id'))
            # Check for and update existing schema.
            # Create new schema docs otherwise.
            if not existing:
                db.save(doc)
            else:
                for k, v in doc.items():
                    if k in existing:
                        if existing[k] != v:
                            existing[k] = v
                    else:
                        existing[k] = v
                db.save(existing)

    return db
