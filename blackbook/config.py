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
COUCHDB_URI = "http://localhost:5984"
API_ROOT = '/api/'