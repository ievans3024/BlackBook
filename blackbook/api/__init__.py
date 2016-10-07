from flask.views import MethodView

__all__ = ['collectionplusjson', 'errors', 'html', 'json', 'xml']
__author__ = 'ievans3024'


class Api(MethodView):

    def __init__(self, db, mimetype):
        self.db = db
        self.mimetype = mimetype
        super(Api, self).__init__()

    def generate_document(self, *args, **kwargs):
        raise NotImplementedError()
