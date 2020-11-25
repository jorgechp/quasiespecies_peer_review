class User:
    def __init__(self, id_user: int):
        self._is_authenticated = False
        self._is_active = True
        self._id = 0

    def set_authenticated(self, is_authenticated):
        self._is_authenticated = is_authenticated

    def is_authenticated(self):
        return self._is_authenticated

    def is_active(self):
        return self._is_authenticated

    def is_anoynmouse(self):
        return not self._is_authenticated

    def get_id(self):
        return chr(self._id)
