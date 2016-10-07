from flask.views import MethodView

__all__ = ['collectionplusjson', 'errors', 'html', 'json', 'xml']
__author__ = 'ievans3024'

"""

routes

/api/<type>/
    GET - retrieve some basic data about the api
/api/<type>/user/
    GET - retrieve some basic data about the user endpoint
    POST - create a new user
/api/<type>/user/<id>/
    self sessions may do all below to own account
    must have permission to perform these actions on other accounts
    GET - retrieve info about a user, including all contact data
    PUT - update all user data (all fields must be filled)
    PATCH - update partial user data (only fields to be updated should be filled)
    DELETE - delete user account
/api/<type>/session/
    GET - retrieve current session auth based on cookies/session data
    POST - create new session with credentials in body
    PUT/PATCH - update current session expiry
    DELETE - delete session

"""


class Api(MethodView):

    def __init__(self, db, mimetype):
        self.db = db
        self.mimetype = mimetype
        super(Api, self).__init__()

    def generate_document(self, *args, **kwargs):
        raise NotImplementedError()
