import couchdb
import couchdb.mapping
import json
import os.path

__author__ = 'ievans3024'


def init_db(app):
    dbname = app.config.get("DB_NAME") or "blackbook"
    server = couchdb.Server(app.config.get("COUCHDB_URI") or "http://localhost:5984")  # default to couch default uri

    # Create database if it doesn't exist
    try:
        db = server[dbname]
    except couchdb.ResourceNotFound:
        db = server.create(dbname)

    # Load in schema file
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "{0}.json".format(dbname))
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)

    # Update design docs and api specs according to schema file,
    # create new docs if they don't exist
    for doc in schema:
        d = couchdb.mapping.Document.load(db, doc.get("_id"))
        if not d:
            d = couchdb.mapping.Document(id=doc.get("_id"))
        for k, v in doc.items():
            if k in d:
                if d[k] != v:
                    d[k] = v
            else:
                d[k] = v
        d.store(db)

    return db