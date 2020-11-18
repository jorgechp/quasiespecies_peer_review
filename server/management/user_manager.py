from dataclasses import dataclass

from server.db.database_manager import DatabaseManager
from server.security.security_manager import SecurityManager


@dataclass
class User:
    id: int
    nick: str
    mail: str


class UserManager(object):

    def __init__(self, database_manager: DatabaseManager, secret_key_path: str):
        self._security_manager = SecurityManager()
        self._security_manager.set_file_path(secret_key_path)

        if not self._security_manager.is_key_file_exists():
            self._security_manager.generate_fernet_key()
        self._security_manager.use_fernet_key()

        self._database_manager = database_manager
        self._num_articles = database_manager.get_number_of_articles()

    def add_user(self, nick: str, plain_mail: str, plain_password: str) -> User:
        encrypted_mail = self._security_manager.encrypt_mail(plain_mail).decode()
        hashed_password = self._security_manager.hash_password(plain_password)

        id_user = self._database_manager.add_user(nick, encrypted_mail, hashed_password)
        if id_user == -1:
            return id_user
        return User(id_user, nick, plain_mail)

    def get_user_id(self, nick: str) -> int:
        return self._database_manager.get_user_by_nick(nick)

    def check_user_password(self, user_id: int, plain_password: str) -> bool:
        hashed_password = self._database_manager.get_user_password(user_id)
        return self._security_manager.check_hashed_password(plain_password,hashed_password)
