import os
import string
import random

import bcrypt as bcrypt
from cryptography.fernet import Fernet


class SecurityManager(object):
    """
    This class handles security parameter like Fernet password.

    It's implemented as a singleton, the singleton code is extracted from Tutorials Point:
    https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
    """

    __instance = None
    __key = None
    __path = None

    @staticmethod
    def get_instance():
        if SecurityManager.__instance is None:
            SecurityManager()
        return SecurityManager.__instance

    def __init__(self):
        if SecurityManager.__instance is None:
            SecurityManager.__instance = self

    def set_file_path(self, path:str) -> None:
        """
        Sets the path to the secret key file.

        :param path: The path to the file.
        """

        self.__path = path

    def use_fernet_key(self):
        """
        Loads the Fernet key.
        """

        file = open(self.__path, "rb")
        self.__key = file.read()
        file.close()

    def is_key_file_exists(self) -> bool:
        """
        Checks if the key file exists.

        :return: True if the key file exists, False otherwise.
        :rtype: bool
        """

        return os.path.exists(self.__path)

    def generate_fernet_key(self) -> None:
        """
        Generates a Fernet keys in the specified path.
        """

        file = open(self.__path, "wb")
        file.write(Fernet.generate_key())
        file.close()

    def encrypt_mail(self, mail: str) -> bytes:
        """
        Encode the user mail into a bytes chain, and then, encrypt the bytes with the Fernet standard.
        
        :param mail: The plain text password to be ciphered.
        :return: The bytes chain of the mail.
        :rtype: bytes
        """

        return Fernet(self.__key).encrypt(mail.encode())

    def decrypt_mail(self, mail: str) -> str:
        """
        Decrypt a password, to obtain a bytes chain, and decodes the byte chain to get the plain user mail.
        
        :param mail: The encypted mail.
        :return: The plain mail.
        :rtype: str
        """
        return Fernet(self.__key).decrypt(mail.encode()).decode()

    def hash_password(self, password: str) -> str:
        """
        Hash a password, using the bcrypt library.

        :param password: The password to be hashed.
        :type password: str
        :return: The password, hashed.
        :rtype: str
        """

        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_hashed_password(self, password: str, hashed_password: str) -> bool:
        """
        Check if a plain password coincides with a hashed one.

        :param password: The plain password to be checked.
        :type password: str
        :param hashed_password: The hashed password.
        :type hashed_password: str

        :return: True if the plain password coincides with the hashed one, False otherwise.
        :rtype: bool
        """

        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_recovery_token(self) -> tuple:
        """
        Generates two random strings, to be used as recovery password token.

        :return: A tuple with the two random tokens
        """
        client_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
        session_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(500))
        return client_token, session_token


