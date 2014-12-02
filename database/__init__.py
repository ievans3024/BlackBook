__author__ = 'ievans3024'


class Database(object):
    """
    A base class for database abstraction for ReSTful APIs

    This class is a skeleton to model wrappers from. A database wrapper should abstract away database/ORM quirks in
    behind a simple interface modeled after CRUDS -- Create, Read, Update, Delete, Search -- systems.

    Subclass this class when creating a new wrapper class. Implement the same methods provided here, and the application
    code will be able to interact with the database regardless of what kind of database is being used.
    """

    class Model(object):
        """
        A base class for database models.

        This class is a skeleton to model information models from. A database wrapper may subclass this to provide
        some simple methods for different kinds of information.

        When an information model inherits from this and another class, this class should be to the right of all other
        inherited classes, e.g:
            class SomeMultiInheritModel(SomeOtherModel, Model):
                pass
        """

        class ModelError(BaseException):
            """
            Wrapper class for model-specific errors. Can be subclassed.
            Purely exists to allow for catching explicitly written model errors (e.g., for data validation) and to
            create custom exceptions to catch different types of errors (e.g., missing required fields, wrong data
            type, etc.)
            """
            def __init__(self, message, *args, **kwargs):
                super(BaseException, self).__init__(message)

        def __init__(self, *args, **kwargs):
            """
            Model Constructor
            All models should implement this method.
            This method should raise a Database.Model.ModelError or a subclass of it when data supplied is invalid.
            Models should have an 'endpoint' property that can be set on init
            """
            pass

        def get_collection_item(self, as_dict=False):
            """
            Get a collection_json.Item representation of this model
            :param as_dict: If true, return a dict-like object instead of a collection_json.Item instance.
            :return: A collection_json.Item instance by default, a dict-like object if as_dict is true.
            """
            raise NotImplementedError()

        @staticmethod
        def get_template(as_dict=False):
            """
            Get an empty collection_json.Template for this model
            :param as_dict: If true, return a dict-like object instead of a collection_json.Template instance.
            :return: A collection_json.Template instance by default, a dict-like object if as_dict is true
            """
            raise NotImplementedError()

        def update(self, data):
            """
            Update this model instance's data
            :param data: The information to update the model with.
            :type data: collection_json.Template
            :return:
            """
            raise NotImplementedError()

    def __init__(self, app, *args, **kwargs):
        """
        Database Constructor
        All Databases should implement this method.
        All Databases should create a property called "models" that is a dict-like object where keys are the model name
        and values are the Model Class, e.g.:
            self.models = {
                'ModelOne': SomeDatabaseClass.ModelOne,
                'ModelTwo': SomeDatabaseClass.ModelTwo
            }
        :param app: The flask application to tie this Database to.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def add_model(self, model_class):
        """
        Add a model class to the instance models.
        :param model_class: The model class to add
        :type model_class: database.Database.Model
        :raises TypeError: If model_class is not a subclass of ubookstore.database.Database.Model
        :return:
        """
        if issubclass(model_class, Database.Model):
            try:
                self.models[model_class.__name__] = model_class
            except (AttributeError, TypeError):
                raise NotImplementedError(
                    self.__class__.__name__ + ' does not have a "models" attribute or it is not subscriptable.'
                )
        else:
            raise TypeError('model_class must be a subclass of database.Database.Model')

    def create(self, model, data, *args, **kwargs):
        """
        Create a new model instance.
        Please note that server-side data validation should happen in the model's init method somewhere.
        This method should capture instances of Database.Model.ModelError and return a Collection containing the
        appropriate error information.
        :param model: The model to create a new instance of.
        :param data: The data to parse into the model.
        :return: A collection_json.Collection instance containing information about what happened (including errors.)
        """
        raise NotImplementedError()

    def read(self, model, *args, **kwargs):
        """
        Get information representing a model instance.
        :param model: The model to attempt to read from, using information in args/kwargs to specify what is requested.
        :return: A collection_json.Collection instance containing information about the requested resource or what
        happened (including errors.)
        """
        raise NotImplementedError()

    def update(self, model, data, *args, **kwargs):
        """
        Update information for an existing model instance.
        Please note that server-side data validation should happen in the model's init method somewhere.
        This method should capture instances of Database.Model.ModelError and return a Collection containing the
        appropriate error information.
        :param model: The model to update the information for.
        :param data: The data to parse into the model. Should accept partial data and overlay it on existing data.
        :return: A collection_json.Collection instance containing information about what happened (including errors.)
        """
        raise NotImplementedError()

    def delete(self, model, *args, **kwargs):
        """
        Delete an instance of a model.
        This method should determine from args/kwargs which instance of the model to delete.
        :param model: The model to delete an instance of.
        :return: A collection_json.Collection instance containing information about what happened (including errors.)
        """
        raise NotImplementedError()

    def search(self, model, data, *args, **kwargs):
        """
        Search a model for instances that might be relevant to a query.
        :param model: The model to search through instances of.
        :return: A collection_json.Collection instance containing information about the results from the query, or about
        what happened (including errors.)
        """
        raise NotImplementedError()

    def generate_test_db(self):
        """
        Generate test data to demonstrate or test the application.
        This method should create a separate, temporary database, instead of overwriting production data.
        :raises: RunTimeError if app config key 'TESTING' does not have a value of True.
        :return:
        """
        raise NotImplementedError()


test_first_names = [
    'Alex', 'Andrea', 'Bryce', 'Brianna', 'Cole', 'Cathy', 'Derek', 'Danielle', 'Eric', 'Edith', 'Fred', 'Felicia',
    'Garrett', 'Gianna', 'Harold', 'Helga', 'Ira', 'Ingrid', 'Jonathan', 'Jacquelyn', 'Kerry', 'Karen', 'Larry',
    'Laura', 'Melvin', 'Margaret', 'Noel', 'Natalie', 'Otis', 'Olga', 'Peter', 'Pia', 'Quentin', 'Quinn',
    'Reginald', 'Rachel', 'Steven', 'Samantha', 'Tyler', 'Tullia', 'Ulric', 'Uma', 'Vincent', 'Valerie', 'Wade',
    'Wendy', 'Xavier', 'Xandra', 'Yusef', 'Yolanda', 'Zach', 'Zoe'
]

test_last_names = [
    'Ashford', 'Aldred', 'Beckett', 'Blackford', 'Carey', 'Conaway', 'Delung', 'Doohan', 'Eagan', 'Eastman',
    'Farley', 'Flores', 'Gandy', 'Grimes', 'Harkness', 'Hughley', 'Inman', 'Isley', 'Jager', 'Johannsen',
    'Keatinge', 'Kaufman', 'Lachance', 'Lopez', 'Markley', 'Meeker', 'Norrell', 'Nunnelly', 'Oberman', 'Osmond',
    'Puterbough', 'Pinkman', 'Quigly', 'Quayle', 'Romero', 'Rosenkranz', 'Smith', 'Stillman', 'Titsworth',
    'Thomson', 'Umbrell', 'Underwood', 'Valentine', 'Voyer', 'Wheatley', 'Wetzel', 'Xerxes', 'Xin', 'Yancey',
    'York', 'Zeeley', 'Zorn'
]

test_phone_numbers = [
    '6310', '2686', '8370', '7294', '0480', '8213', '1676', '5981', '9820', '9213', '6547', '1629', '7464', '6742',
    '2307', '3152', '3245', '4283', '0144', '4995', '1271', '9220', '9827', '7032', '4855', '7975', '3912', '8340',
    '7934', '4647', '6552', '3079', '6161', '1307', '3158', '1034', '0295', '2317', '7179', '0743', '8588', '7068',
    '2450', '9826', '6458', '0554', '5614', '5106', '5020', '0577', '7277', '6371'
]

test_address_line_1s = [
    '907 23rd St.', '972 24th Ave.', '483 24th Ave.', '676 8th Ave.', '984 21st St.', '923 19th St.',
    '734 13th Ave.', '741 22nd Ave.', '45 20th Ave.', '597 16th St.', '259 15th Ave.', '361 3rd Ave.',
    '697 21st St.', '887 18th Ave.', '403 9th Ave.', '684 9th Ave.', '641 19th Ave.', '398 2nd Ave.',
    '752 11th St.', '237 14th St.', '393 8th Ave.', '603 18th Ave.', '601 15th St.', '54 2nd Ave.', '357 20th Ave.',
    '424 10th Ave.', '343 18th St.', '448 13th St.', '743 6th St.', '308 13th St.', '929 15th Ave.', '990 19th St.',
    '27 19th St.', '119 12th St.', '156 15th Ave.', '698 3rd St.', '177 24th Ave.', '663 1st St.', '808 5th Ave.',
    '88 10th St.', '776 15th St.', '927 9th St.', '834 7th Ave.', '786 6th Ave.', '598 22nd St.', '653 2nd St.',
    '162 4th St.', '552 4th Ave.', '118 8th St.', '900 3rd St.', '9 14th St.', '921 9th Ave.'
]

test_address_line_2s = [
    None, None, 'Apt. R', 'Apt. 786', 'Apt. K', 'Apt. V', None, 'Apt. X', 'Apt. N', None, None, 'Apt. 789',
    'Apt. O', 'Apt. S', 'Apt. J', 'Apt. 778', None, 'Apt. 662', None, 'Apt. P', 'Apt. 717', 'Apt. E', 'Apt. 402',
    'Apt. W', None, 'Apt. 545', None, None, 'Apt. X', None, None, 'Apt. T', 'Apt. 183', None, None, None,
    'Apt. 104', 'Apt. L', 'Apt. 675', 'Apt. C', 'Apt. D', None, 'Apt. V', None, 'Apt. 846', 'Apt. 804', 'Apt. 365',
    'Apt. 447', 'Apt. 330', None, 'Apt. 765', None
]

test_cities = [
    'Example City',
    'Nowhere',
    'Sigil',
    'Pleasantville'
]

test_states = [
    'XY',
    'XX',
    'ZY',
    'ZX'
]

test_zipcodes = [str(n).zfill(5) for n in range(100)]