import flask
from flask import (
    Blueprint, request, session, jsonify, abort
)
from flask_login import login_user, logout_user, current_user

from model.User import User
from server.management.user_manager import UserManager


def construct_user_blueprint(user_manager: UserManager):
    bp = Blueprint('user', __name__, url_prefix='/user')

    @bp.route('/login', methods=['POST', 'DELETE'])
    def user_session():
        if request.method == 'POST':
            return perfom_login()
        elif request.method == 'DELETE':
            return perfom_logout()

    def perfom_login():
        a = current_user
        if 'username' in session:
            abort(400, {'message': 'There is another user session.'})

        json_request = request.get_json(force=True)
        plain_nick = json_request['nick']
        plain_password = json_request['password']
        user_id = user_manager.get_user_id(plain_nick)

        if user_id is not None:
            is_correct_login = user_manager.check_user_password(user_id, plain_password)
        else:
            abort(401)

        if is_correct_login:
            session['username'] = user_id
            logged_user = User(user_id)
            login_user(logged_user)
        else:
            abort(401)


        response = jsonify(is_correct_login)
        response.headers.add('Access-Control-Allow-Headers',
                             "Origin, X-Requested-With, Content-Type, Accept, x-auth")
        response.set_cookie('token', 'aaaa')
        return response

    def perfom_logout():
        logout_user()
        session.clear()
        return jsonify(True)

    @bp.route('/', methods=['POST'])
    def add_user_answer():
        json_request = request.get_json(force=True)

        if 'mail' not in json_request or 'nick' not in json_request or 'password' not in json_request:
            abort(400, 'User data not provided.')

        plain_mail = json_request['mail']
        nick = json_request['nick']
        plain_password = json_request['password']

        new_user = user_manager.add_user(nick, plain_mail, plain_password)
        if new_user == -1:
            response = jsonify({'message': 'Duplicated user'})
            response.status_code = 400
            return response
        return jsonify(new_user)
    return bp
