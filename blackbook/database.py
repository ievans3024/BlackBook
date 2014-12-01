__author__ = 'ievans3024'

from blackbook import app

if (not app.config.get('DATABASE_HANDLER')) or (app.config.get('DATABASE_HANDLER') == 'flatfile'):
    from database.flatfile import FlatDatabase
    from blackbook.models import flatfile
    db = FlatDatabase(app)
    db.models = flatfile.models
elif app.config.get('DATABASE_HANDLER') in ('sqlite', 'mysql', 'postgresql'):
    from database.sqlalchemy import SQLAlchemyDatabase
    from blackbook.models import sqlalchemy
    db = SQLAlchemyDatabase(app)
    db.models = sqlalchemy.models