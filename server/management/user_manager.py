from dataclasses import dataclass

from server.db.database_manager import DatabaseManager

@dataclass
class User:
    id: int
    mail: str

class UserManager(object):

    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager
        self._num_articles = database_manager.get_number_of_articles()

    def add_user(self, mail: str) -> User:
        id_user = self._database_manager.add_user(mail)
        return User(id_user, mail)
