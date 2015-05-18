__author__ = 'ievans3024'

from flask import Blueprint

import blackbook.couch.api
import blackbook.couch.database

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

contact_view = api.Contact(database.db).as_view('contact_api')
api_blueprint.add_url_rule('/contact/', defaults={'user_id': None}, view_func=contact_view, methods=["GET", "POST"])
api_blueprint.add_url_rule('/contact/<contact_id>/', defaults={'user_id': None, 'contact_id': None},
                           view_func=contact_view, methods=["GET", "PATCH", "PUT", "DELETE"])
api_blueprint.add_url_rule('/user/<user_id>/contacts/', defaults={'user_id': None},
                           view_func=contact_view, methods=["GET", "POST"])