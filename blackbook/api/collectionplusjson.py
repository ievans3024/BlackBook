import blackbook.lib.collection_plus_json as collection_json

from blackbook.api import Api


class CollectionJsonApi(Api):

    def __init__(self, db):
        super(CollectionJsonApi, self).__init__(db, 'application/vnd.collection+json')

    def generate_document(self, *args, **kwargs):
        pass
