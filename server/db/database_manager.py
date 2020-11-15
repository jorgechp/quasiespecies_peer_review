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

    def get_random_article(self):
        """
        Returns a random article from the database.

        :return: A row with the article information.
        """

        cursor = self._database_connection.cursor()
        cursor.execute("SELECT * FROM article ORDER BY RANDOM() LIMIT 1;")
        return cursor.fetchone()

    def get_quartile_from_article(self, id_article: int) -> int:
        """
        Returns information about the quartile associated to the journal of an article.

        :param id_article: The id of the article.
        :type id_article: int
        :return: The quartile of the journal.
        :rtype: int
        """
        cursor = self._database_connection.cursor()
        cursor.execute("""
                            SELECT quartile 
                            FROM journal 
                            JOIN article 
                            ON journal.idJournal = article.idJournal 
                            WHERE article.idArticle = {}
                    """.format(id_article))
        return cursor.fetchone()[0]

    def get_quartile_from_journal(self, id_journal: int) -> int:
        cursor = self._database_connection.cursor()
        cursor.execute("""
                            SELECT quartile 
                            FROM journal                             
                            WHERE idJournal = {}
                    """.format(id_journal))
        return cursor.fetchone()[0]

    def add_user_answer(self, id_user: int, id_article: int, id_journal: int, score: int) -> None:
        cursor = self._database_connection.cursor()
        cursor.execute("""
                            INSERT INTO user_answer_article(idUser, idArticle, idJournal, score) 
                            VALUES ({},{},{},{})
                        """.format(id_user, id_article, id_journal, score)
                       )

    def add_user(self, mail: str) -> int:
        cursor = self._database_connection.cursor()
        cursor.execute("""
                            INSERT INTO user(mail) 
                            VALUES ({})
                        """.format(mail)
                       )
        return cursor.lastrowid
