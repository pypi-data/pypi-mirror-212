"""

"""
# Python level imports
import sqlitedict
from sqlitedict import SqliteDict

class DB_Creation:
    def __init__(self, location):
        """
        :param location: path of database as a string
        """
        self.__location = location
        self._create_database(self.__location)

    def _create_database(self, location: str) -> SqliteDict:
        db = sqlitedict.SqliteDict(location)
        return db
