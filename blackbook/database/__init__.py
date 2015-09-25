__author__ = 'ievans3024'


class Model(object):

    def get_collection_items(self):
        """
        Get a collection_plus_json.Array of collection_plus_json.Items
        representing one or more instances of the model.
        :return:
        """
        raise NotImplementedError()


class ModelError(BaseException):
    pass
