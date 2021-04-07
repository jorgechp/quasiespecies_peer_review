import types
import sqlite3
from typing import List


class DatabaseManager(object):

    def __init__(self, database_caller: types.FunctionType = None, database_connection: sqlite3.Connection = None):
        self._database_caller = database_caller
        self._db = database_connection

    def __get_cursor(self) -> sqlite3.Cursor:
        if self._database_caller is not None:
            db = self._database_caller()
        else:
            db = self._db
        return db, db.cursor()

    @staticmethod
    def close_connections(db: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        db.commit()
        cursor.close()
        db.cursor()

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
        query = "SELECT article.idarticle, article.title, article.abstract, " \
                "article.authors_keywords, article.keywords_plus, article.idjournal " \
                "FROM article JOIN journal ON article.idJournal = journal.idJournal " \
                "WHERE journal.idImpactType IN (SELECT idimpacttype FROM impact_type " \
                "ORDER BY random() LIMIT 1) ORDER BY random() LIMIT 1"

        cursor.execute(query)
        response = cursor.fetchone()
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_num_articles_per_impact(self,  impact: str) -> int:
        id_answer_impact = self.get_id_impact(impact)
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT COUNT(title) 
                            FROM article 
                            JOIN journal 
                            ON article.idJournal = journal.idJournal                  
                            WHERE journal.idImpactType = {}
                    """.format(id_answer_impact))
        response = cursor.fetchone()[0]
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_impact_type(self, id_article) -> int:
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT impact_type.description 
                            FROM impact_type 
                            JOIN journal 
                            ON impact_type.idImpactType = journal.idImpactType 
                            JOIN article
                            ON article.idJournal = journal.idJournal
                            WHERE article.idArticle = {}
                    """.format(id_article))
        response = cursor.fetchone()[0]
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

    def add_user_answer(self, id_user: int, id_article: int, impact: str, score: int, time:int) -> None or bool:
        db, cursor = self.__get_cursor()

        cursor.execute("""
                            SELECT idImpactType 
                            FROM journal JOIN article ON journal.idJournal = article.idJournal 
                            WHERE article.idArticle = {}
                        """.format(id_article)
                       )

        data = cursor.fetchone()
        if data is not None:
            id_real_impact = data[0]
        else:
            return False

        id_anwer_impact = self.get_id_impact(impact)

        cursor.execute("""
                            INSERT INTO user_answer_article(idUser,
                                                            idArticle,
                                                            userAnswerImpact,
                                                            realImpact,
                                                            score,
                                                            time) 
                            VALUES ({},{},{},{},{},{})
                        """.format(id_user, id_article, id_anwer_impact, id_real_impact, score, time)
                       )
        DatabaseManager.close_connections(db, cursor)

    def __change_role(self, is_editor: bool, is_reviewer: bool, cursor: sqlite3.Cursor, user_id: int) -> None:
        try:
            user_has_role_query = """
                            INSERT INTO user_has_role(idUser, idRole) 
                            VALUES ({},{})
                        """

            if is_editor:
                cursor.execute(user_has_role_query.format(user_id, 1))
            if is_reviewer:
                cursor.execute(user_has_role_query.format(user_id, 2))
        except sqlite3.IntegrityError as err:
            return -1

    def add_user(self, nick: str, mail: str, password: bytes, is_editor: bool, is_reviewer: bool) -> int:
        db, cursor = self.__get_cursor()

        try:
            cursor.execute("""
                                INSERT INTO user(nick, mail, password) 
                                VALUES ("{}","{}","{}")
                            """.format(nick, mail, password)
                           )

            response = cursor.lastrowid
            self.__change_role(is_editor, is_reviewer, cursor, response)

        except sqlite3.IntegrityError as err:
            return -1
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_users_nicknames(self) -> List[tuple]:
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT DISTINCT(nick) 
                            FROM user
                    """)
        data = cursor.fetchall()
        response = data if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def remove_user(self, user_id: str) -> bool:
        db, cursor = self.__get_cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("""DELETE FROM user WHERE idUser = '{}' """.format(user_id))
        except sqlite3.IntegrityError:
            return False
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return True

    def change_mail(self, user_id: str, new_mail: str) -> bool:
        db, cursor = self.__get_cursor()
        try:
            cursor.execute("""UPDATE user SET mail = '{}' WHERE idUser = '{}' """.format(new_mail, user_id))
        except sqlite3.Error:
            return False
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return True

    def change_password(self, user_id: str, new_password: str) -> bool:
        db, cursor = self.__get_cursor()

        try:
            cursor.execute("""UPDATE user SET password = '{}' WHERE idUser = '{}' """.format(new_password, user_id))
        except sqlite3.Error:
            return False
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return True

    def get_user_by_nick(self, user_id: str):
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT idUser 
                            FROM user                             
                            WHERE nick = '{}'
                    """.format(user_id))
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

    def get_score(self, user_id: int, partition: int, limit: int):
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT score 
                            FROM user_answer_article                             
                            WHERE idImpactType = {} AND idUser = {}
                            ORDER BY date DESC
                            LIMIT {}
                    """.format(partition, user_id, limit))
        data = cursor.fetchall()
        response = data if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_id_impact(self, impact_name:str) -> int:
        db, cursor = self.__get_cursor()
        cursor.execute("""
                            SELECT idImpactType 
                            FROM impact_type                             
                            WHERE description LIKE '{}'
                    """.format(impact_name))
        data = cursor.fetchone()
        response = data[0] if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def count_user_score_table(self, user_id: str) -> int:
        db, cursor = self.__get_cursor()

        cursor.execute("""SELECT COUNT(idAnswer) FROM user_answer_article WHERE idUser = {};""".format(user_id))
        data = cursor.fetchone()
        response = data[0] if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_user_score_table(self, user_id: str, first: int, target_impact: str, user_impact: str) -> int:
        db, cursor = self.__get_cursor()

        id_real_impact = self.get_id_impact(target_impact)
        id_user_impact = self.get_id_impact(user_impact)

        if first != -1:
            query = """
                            SELECT COUNT(userAnswerImpact)
                            FROM user_answer_article
                            WHERE  idUser = {} AND userAnswerImpact = {} AND realImpact = {} AND
                            idAnswer IN(
                                                SELECT idAnswer 
                                                  FROM user_answer_article
                                                  WHERE  idUser = {}
                                                  ORDER BY date ASC
                                                  LIMIT {});                    
                     """.format(user_id, id_user_impact, id_real_impact, user_id, first)
        else:
            query = """
                            SELECT COUNT(userAnswerImpact)
                            FROM user_answer_article
                            WHERE  idUser = {} AND userAnswerImpact = {} AND realImpact = {};                    
                     """.format(user_id, id_user_impact, id_real_impact)

        cursor.execute(query)
        data = cursor.fetchone()
        response = data[0] if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_user_mail(self, user_nick: str):
        db, cursor = self.__get_cursor()
        cursor.execute("""SELECT mail FROM user WHERE idUser = '{}';""".format(user_nick))
        data = cursor.fetchone()
        response = data[0] if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def get_user_language(self, user_nick: str):
        db, cursor = self.__get_cursor()
        cursor.execute("""SELECT language FROM user WHERE idUser = '{}';""".format(user_nick))
        data = cursor.fetchone()
        response = data[0] if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def set_user_language(self, user_nick: str, language: str) -> bool :
        db, cursor = self.__get_cursor()
        try:
            cursor.execute("""UPDATE user SET language = '{}' WHERE idUser = '{}';""".format(language, user_nick))
            DatabaseManager.close_connections(db, cursor)
            return True
        except sqlite3.Error:
            return False

    def remove_user_tokens(self, user_id: str):
        db, cursor = self.__get_cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("""
                                  DELETE FROM user_tokens WHERE idUser ='{}'
                              """.format(user_id)
                           )
        except sqlite3.IntegrityError as error:
            return -1
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return 0

    def get_role_name(self, id_role: int) -> str:
        db, cursor = self.__get_cursor()
        try:
            cursor.execute("""SELECT name FROM role WHERE idRole = '{}' """.format(id_role))
            data = cursor.fetchone()
            response = data[0] if data is not None else None
            DatabaseManager.close_connections(db, cursor)
            return response
        except sqlite3.Error:
            return ""

    def get_user_role(self, user_id: str):
        db, cursor = self.__get_cursor()

        try:
            cursor.execute("""SELECT idRole FROM user_has_role WHERE idUser = '{}' """.format(user_id))

        except sqlite3.Error:
            return False
        db.commit()
        data = cursor.fetchall()
        response = data if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def change_user_role(self, user_id: int, is_editor: bool, is_reviewer: bool) -> bool:
        db, cursor = self.__get_cursor()

        try:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("""DELETE FROM user_has_role WHERE idUser = '{}' """.format(user_id))
            self.__change_role(is_editor, is_reviewer, cursor, user_id)
        except sqlite3.Error:
            return False
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return True

    def add_user_token(self, user_id: str, client_token: str, cookie_token: str) -> int:
        db, cursor = self.__get_cursor()
        try:
            cursor.execute("""
                                INSERT INTO user_tokens(idUser,
                                                                client_token,
                                                                cookie_token)
                                VALUES ('{}', '{}','{}')
                            """.format(user_id, client_token, cookie_token)
                           )
        except sqlite3.IntegrityError as error:
            return -1
        db.commit()
        DatabaseManager.close_connections(db, cursor)
        return 0

    def getUserByTokens(self, client_token, cookie_token):
        db, cursor = self.__get_cursor()
        cursor.execute(
            """SELECT idUser FROM user_tokens WHERE client_token = '{}' AND cookie_token = '{}';""".format(client_token, cookie_token))
        data = cursor.fetchone()
        response = data[0] if data is not None else None
        DatabaseManager.close_connections(db, cursor)
        return response

    def change_user_password(self, id_user: str, hashed_password: str):
        db, cursor = self.__get_cursor()
        try:
            cursor.execute("""
                                UPDATE user SET password = '{}' WHERE idUser = {}
                            """.format(hashed_password, id_user)
                           )
        except sqlite3.IntegrityError as error:
            return -1
        DatabaseManager.close_connections(db, cursor)
        return 0
