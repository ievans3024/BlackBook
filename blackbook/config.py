from datetime import timedelta

# Flask Builtin Options
DEBUG = True
TESTING = False
PERMANENT_SESSION_LIFETIME = timedelta(days=14)
SECRET_KEY = """Make this really super secret and random!"""
SERVER_NAME = None  # address and port, default is 127.0.0.1:5000
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # True in https production

# Custom Options
PASSWORD_HASH_METHOD = 'pbkdf2:sha512'  # only methods supported by functions in werkzueg.security
PASSWORD_SALT_LENGTH = 12
PUBLIC_REGISTRATION = False  # Set to True to allow anyone to make an account
DATABASE_PLUGIN = "blackbook.couch"
COUCHDB_URI = "http://localhost:5984"
API_ROOT = '/api/'
API_PAGINATION_PER_PAGE = 10