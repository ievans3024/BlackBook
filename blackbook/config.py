# Flask Builtin Options
# see http://flask.pocoo.org/docs/config/#builtin-configuration-values
DEBUG = True
TESTING = False
SECRET_KEY = """Make this really super secret and random!"""
SERVER_NAME = None  # address and port, default is 127.0.0.1:5000
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # True in https production

# Flask-SQLAlchemy Options
# see http://flask-sqlalchemy.pocoo.org/config/
SQLALCHEMY_DATABASE_URI = ''

# Custom Options
# PASSWORD_HASH_METHOD
#   A string that will be passed to werkzueg.security functions
#   to specify which hashing algorithm to use
# PASSWORD_SALT_LENGTH
#   An integer indicating length of generated password salts
# PUBLIC_REGISTRATION
#   A boolean indicating whether to allow open public registration
#   or admin-created accounts only
# API_ROOT
#   A string indicating the api root. Must end in a forward slash ('/')
# API_PAGINATION_PER_PAGE
#   An integer indicating maximum results per "page" in a response
#   from API routes.

PASSWORD_HASH_METHOD = 'pbkdf2:sha512'
PASSWORD_SALT_LENGTH = 12
PUBLIC_REGISTRATION = False
API_ROOT = '/api/'
API_PAGINATION_PER_PAGE = 10