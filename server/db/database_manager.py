import sqlite3

class DatabaseManager(object):

    def __init__(self, database_connection: sqlite3.Connection):
        self._database_connection = database_connection

    def get_number_of_articles(self) -> int:
        """
        Returns the name of articles stored in the database.
        :return: The number of articles in the database.
        :rtype: int
        """

        cursor = self._database_connection.cursor()
        cursor.execute("SELECT seq FROM 'sqlite_sequence' WHERE name = 'article' ")
        return cursor.fetchone()[0]
