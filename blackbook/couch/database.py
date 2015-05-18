__author__ = 'ian'

from couchdb import ResourceNotFound, Server
from couchdb.mapping import Document
from json import load
from os.path import abspath, dirname, join


def init_db(app):
    dbname = app.config.get("DB_NAME") or "blackbook"
    server = Server(app.config.get("COUCHDB_URI") or "http://localhost:5984")  # default to couch default uri

    # Create database if it doesn't exist
    try:
        db = server[dbname]
    except ResourceNotFound:
        db = server.create(dbname)

    # Load in schema file
    with open(join(join(dirname(abspath(__file__)), "js"), "{db}.json".format(db=dbname))) as schema_file:
        schema = load(schema_file)

    # Update design docs and api specs according to schema file
    for doc in schema:
        d = Document.load(db, doc.get("_id"))
        if d:
            for k, v in doc.items():
                if k in d:
                    if d[k] != v:
                        d[k] = v
                else:
                    d[k] = v
            d.store(db)

    return db