__author__ = 'ievans3024'


class DatabaseError(BaseException):
    """Base class for database errors."""
    pass


class DatabaseNotReadyError(DatabaseError):
    """Error class for databases that need to run Database.setup()"""
    pass


class DatabaseUnreachableError(DatabaseError):
    """Error class for databases that cannot be reached."""
    pass


class EntryExistsError(DatabaseError):
    """Error class for when an entry by that id/primary key already exists."""
    pass


class Database(object):
    """Abstract base class for databases"""

    @property
    def is_setup(self):
        """
        Check if Database.setup() needs to be run.

        Implementations should perform any and all functionality
        to ensure that:

           1. The database server is reachable
           2. All databases, tables and schema exist

        Implementations should return True if the database has
        everything it needs in place, False if not.

        Implementations should raise DatabaseUnreachableError if
        the database is not reachable.

        :return: bool
        """
        raise NotImplementedError()

    def create(self, data):
        """
        Create a new entry in the database.

        For the "data" parameter, implementations should accept
        instances of blackbook.database.models.Model and be able
        to extract information from them, or raise the appropriate
        DatabaseError accordingly.

        How the data contained in the instance is dissected and
        stored is left to the discretion of implementation.

        :param data: The Model instance to extract new data from.
        :return: An iterable of one blackbook.database.models.Model instance.
        """
        raise NotImplementedError()

    def delete(self, data):
        """
        Delete an existing entry from the database.

        For the "data" parameter, implementations should accept
        instances of blackbook.database.models.Model and be able
        to extract information from them, or raise the appropriate
        DatabaseError accordingly.

        How the data is used to find and delete the existing entry
        is left to the discretion of the implementation.

        Implementations should not return anything and should raise
        informative errors should any problems occur.

        :param data: The Model instance to find and delete the entry for.
        :return:
        """
        raise NotImplementedError()

    def read(self, model, _id=None):
        """
        Read one or more entries from the database.

        For the "model" parameter, implementations should accept
        subclasses of blackbook.database.models.Model and be able
        to find relevant data for and instantiate that model, or
        raise the appropriate DatabaseError accordingly.

        The optional "_id" parameter may be supplied to fetch a
        specific entry and return that data in an instance of the
        supplied model, or raise the appropriate DatabaseError
        accordingly.

        However the data is stored in the database, implementations
        should return one or more instances of the supplied model
        contained in an iterable.

        If _id is None, all entries that the implementation determines
        are suited for the model supplied should be returned. Otherwise,
        only one entry, if it exists, that matches _id should be returned.

        :param model: The Model subclass to instantiate
        :param _id: Optional. The id of a specific entry to get.
        :return: An iterable of one or more blackbook.database.models.Model instances.
        """
        raise NotImplementedError()

    def replicate(self, database):
        """
        Replicate the data contained in another Database instance.

        For the "database" parameter, implementations should accept
        an instance of Database, and call its read() method for each
        model type the implementation is meant to store.

        It is left up to the discretion of the implementation how
        it dissects and stores the information supplied by the read()
        method of the other database.

        Implementations should not return anything and should raise
        informative errors should any problems occur.

        :param database: An instance of blackbook.database.Database
        :return:
        """
        raise NotImplementedError()

    def search(self, query, model=None):
        """
        Find entries in the database matching a query.

        The optional "model" parameter should be a subclass of
        blackbook.database.models.Model and should be used by
        implementations to narrow results to a specific set of data.

        :param query: The search terms to try to find matching data for.
        :param model: Optional. The model to contstrain the search to.
        :return: An iterable of one or more blackbook.database.models.Model instances.
        """
        raise NotImplementedError()

    def setup(self):
        """
        Initialize the database for the first time.

        This method should be used to create tables, schema, stored
        procedures, etc. in the database.

        Implementations should not return anything, and should raise
        informative errors should any problems occur.

        :return:
        """
        raise NotImplementedError()

    def update(self, data):
        """
        Update an existing entry in the database.

        For the "data" parameter, implementations should accept
        instances of blackbook.database.models.Model and be able
        to extract information from them, or raise the appropriate
        DatabaseError accordingly.

        How the data contained in the instance is dissected and
        stored is left to the discretion of implementation.

        If the model instance does not contain an identifier that points
        to an existing entry in the database, the implementation should
        raise the appropriate DatabaseError

        :param data:
        :return: An iterable of one or more blackbook.database.models.Model instances.
        """
        raise NotImplementedError()
