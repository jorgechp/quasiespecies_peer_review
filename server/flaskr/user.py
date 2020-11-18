from flask import (
    Blueprint, request, session, jsonify
)

from server.management.user_manager import UserManager


def construct_user_blueprint(user_manager: UserManager):
    bp = Blueprint('user', __name__, url_prefix='/user')

    @bp.route('/login', methods=['POST'])
    def login_user():
        if request.method == 'POST':
            json_request = request.get_json()
            plain_nick = json_request['nick']
            plain_password = json_request['password']

            user_id = user_manager.get_user_id(plain_nick)
            is_correct_login = user_manager.check_user_password(user_id, plain_password)

            if is_correct_login:
                session['username'] = user_id

            return jsonify(is_correct_login)

    @bp.route('/login', methods=['DELETE'])
    def login_user():
        session.clear()
        return jsonify(True)

    @bp.route('/', methods=['POST'])
    def add_user_answer():
        if request.method == 'POST':
            json_request = request.get_json()
            plain_mail = json_request['mail']
            nick = json_request['nick']
            plain_password = json_request['password']

            new_user = user_manager.add_user(nick, plain_mail, plain_password)

            return jsonify(new_user)
    return bp
