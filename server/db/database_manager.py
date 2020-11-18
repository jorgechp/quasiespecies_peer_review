import types
import sqlite3


class DatabaseManager(object):

    def __init__(self, database_caller: types.FunctionType):
        self._database_caller = database_caller

    def __get_cursor(self) -> sqlite3.Cursor:
        db = self._database_caller()
        return db, db.cursor()

    @staticmethod
    def close_connections(db: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        db.commit()
        cursor.close()
        db.cursor()

    @staticmethod
    def convert_quartile_to_impact(quartile: int) -> str:
        if quartile <= 2:
            return "HIGH IMPACT"
        elif quartile == 3:
            return "MEDIUM IMPACT"
        else:
            return "LOW IMPACT"

    def get_number_of_articles(self) -> int:
        """
        Returns the name of articles stored in the database.
        :return: The number of articles in the database.
        :rtype: int
        """

        db, cursor = self.__get_cursor()
        cursor.execute("SELECT COUNT(idArticle) FROM 'article' ")
        response = cursor.fetchone()[0]
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_article(self, id_article: int):
        """
        Returns an article from the database. Identified by its id

        :return: A row with the article information.
        """

        db, cursor = self.__get_cursor()
        cursor.execute("SELECT * FROM article WHERE idArticle = {};".format(id_article))
        response = cursor.fetchone()
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_random_article(self):
        """
        Returns a random article from the database.

        :return: A row with the article information.
        """

        db, cursor = self.__get_cursor()
        cursor.execute("SELECT * FROM article ORDER BY RANDOM() LIMIT 1;")
        response = cursor.fetchone()
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_quartile_from_article(self, id_article: int) -> int:
        """
        Returns information about the quartile associated to the journal of an article.

        :param id_article: The idUser of the article.
        :type id_article: int
        :return: The quartile of the journal.
        :rtype: int
        """

        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT quartile 
                            FROM journal 
                            JOIN article 
                            ON journal.idJournal = article.idJournal 
                            WHERE article.idArticle = {}
                    """.format(id_article))
        response = cursor.fetchone()[0]
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_quartile_from_journal(self, id_journal: int) -> int:
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT quartile 
                            FROM journal                             
                            WHERE idJournal = {}
                    """.format(id_journal))

        response = cursor.fetchone()[0]
        DatabaseManager.close_connections(db, cursor)
        return response

    def add_user_answer(self, id_user: int, id_article: int, quartile: int, score: int) -> None or bool:
        impact_type_description = DatabaseManager.convert_quartile_to_impact(quartile)

        db, cursor = self.__get_cursor()

        cursor.execute("""
                            SELECT idImpactType FROM impact_type WHERE description LIKE '{}'
                        """.format(impact_type_description)
                       )

        data = cursor.fetchone()
        if data is not None:
            impact_id = data[0]
        else:
            return False

        cursor.execute("""
                            INSERT INTO user_answer_article(idUser,
                                                            idArticle,
                                                            user_answer_quartile,
                                                            idImpactType,
                                                            score) 
                            VALUES ({},{},{},{},{})
                        """.format(id_user, id_article, quartile, impact_id, score)
                       )
        DatabaseManager.close_connections(db, cursor)

    def add_user(self, nick: str, mail: str, password: bytes) -> int:
        db, cursor = self.__get_cursor()

        try:
            cursor.execute("""
                                INSERT INTO user(nick, mail, password) 
                                VALUES ("{}","{}","{}")
                            """.format(nick, mail, password)
                           )
        except sqlite3.IntegrityError:
            return -1
        response = cursor.lastrowid
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_user_by_nick(self, encrypted_mail: str):
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT idUser 
                            FROM user                             
                            WHERE nick = '{}'
                    """.format(encrypted_mail))
        data = cursor.fetchone()
        response = data[0] if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_user_password(self, id_user: int) -> bytes:
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT password 
                            FROM user                             
                            WHERE idUser = '{}'
                    """.format(id_user))
        response = cursor.fetchone()[0]
        DatabaseManager.close_connections(db, cursor)
        return response
