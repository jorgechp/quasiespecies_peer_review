import configparser
from dataclasses import dataclass

from db.database_manager import DatabaseManager
from management.mail_management import MailManagement
from security.security_manager import SecurityManager


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

    def add_user(self, nick: str, plain_mail: str, plain_password: str, is_editor: bool, is_reviewer: bool) -> User:
        encrypted_mail = self._security_manager.encrypt_mail(plain_mail).decode()
        hashed_password = self._security_manager.hash_password(plain_password)

        id_user = self._database_manager.add_user(nick, encrypted_mail, hashed_password, is_editor, is_reviewer)
        if id_user == -1:
            return id_user
        return User(id_user, nick, plain_mail)

    def remove_user(self, user_id: int) -> bool:
        return self._database_manager.remove_user(user_id)

    def get_user_id(self, nick: str) -> int:
        return self._database_manager.get_user_by_nick(nick)

    def check_user_password(self, user_id: int, plain_password: str) -> bool:
        hashed_password = self._database_manager.get_user_password(user_id)
        return self._security_manager.check_hashed_password(plain_password,hashed_password)

    def change_mail(self, user_id: str, new_mail: str) -> bool:
        encrypted_mail = self._security_manager.encrypt_mail(new_mail).decode()
        return self._database_manager.change_mail(user_id, encrypted_mail)

    def change_password(self, user_id: str, plain_password: str) -> bool:
        hashed_password = self._security_manager.hash_password(plain_password)
        return self._database_manager.change_password(user_id, hashed_password)

    def remove_user(self, user_id: int) -> bool:
        return self._database_manager.remove_user(user_id)

    def get_user_mail(self, user_id: str, mail: str):
        user_mail_encrypted = self._database_manager.get_user_mail(user_id)
        if user_mail_encrypted == -1:
            return user_mail_encrypted
        decrypted_mail = self._security_manager.decrypt_mail(user_mail_encrypted)
        if mail != decrypted_mail:
            return -1
        return decrypted_mail

    def get_recovery_token(self, user_nick: str):
        client_token, session_token = self._security_manager.get_recovery_token()
        user_id = self._database_manager.get_user_by_nick(user_nick)
        self._database_manager.remove_user_tokens(user_id)
        self._database_manager.add_user_token(user_id, client_token, session_token)
        return client_token, session_token

    def send_recovery_mail(self, user_mail: str, client_token: str):
        config = configparser.ConfigParser()
        config.read('security/config.ini')
        default_config = config['MAIL']

        mail_client = MailManagement(default_config['server_port']
                                     , str(default_config['mail_password'])
                                     , default_config['server_smtp']
                                     , default_config['mail_account'])
        mail_client.send_recovery_mail(user_mail, client_token)

    def check_user_token(self, token_mail, session_token):
        return self._database_manager.getUserByTokens(token_mail, session_token)

    def change_user_password(self, id_user: str, plain_password: str):
        hashed_password = self._security_manager.hash_password(plain_password)
        response = self._database_manager.change_user_password(id_user, hashed_password)
        return response == 0

    def remove_user_token(self, id_user_token: str) -> None:
        self._database_manager.remove_user_tokens(id_user_token)
