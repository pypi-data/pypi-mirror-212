""" Base connection classes """
from abc import ABC, abstractmethod


class DBOpenException(Exception):
    """ Specific exception for when connection could not be established
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBExceptionNotOpen(Exception):
    """ Specific exception for when connection could not be used because it was not initialized
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBGetLockException(Exception):
    """ Specific exception for when Lock could not be obtained
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBReleaseLockException(Exception):
    """ Specific exception for when Lock could not be released
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBConn(ABC):
    """ Base connection class
    """
    def __init__(self):
        self.conn = None

    @abstractmethod
    def open_conn(self, params, autocommit=True):
        """ Opens a influxdb connection
        Args:
            params (_type_): Connection params
            autocommit (bool, optional): If commit will be done automatically aftger each writting operation
        """

    def close_conn(self):
        """ Close db connection
        """

    @abstractmethod
    def insert(self, table: str, rows: list):
        """ Insert some rows in a table
        Args:
            table (str): Table to insert the rows into
            rows (list): List of rows to be added
        """

    def get_lock(self, lockname: str):
        """ Gets a unique lock
        Args:
            lockname (str): Name of the lock
        Raises:
            DBGetLockException: Exception because this MUST be overloaded
        """
        raise DBGetLockException('getLock functionality must be overloaded.')

    def release_lock(self, lockname: str):
        """ Release a lock
        Args:
            lockname (str): Name of the lock
        Raises:
            DBReleaseLockException:  Exception because this MUST be overloaded
        """
        raise DBReleaseLockException('releaseLock functionality must be overloaded.')

def influxdb_factory(db_type: str = 'influx') -> DBConn:
    """ Factory for influxdb connection
    Args:
        db_type (str, optional): Defaults to 'influx'... can be 'mock'

    Returns:
        DBConn: _description_
    """
    if db_type == 'influx':
        from .influxdb_conn import InfluxDBConn # pylint: disable=import-outside-toplevel
        return InfluxDBConn()
    elif db_type == 'mock':
        from .mockdb_conn import InfluxMockDBConn # pylint: disable=import-outside-toplevel
        return InfluxMockDBConn()
