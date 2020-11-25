from flask import (
    Blueprint, request, session, jsonify, abort
)
from flask_cors import cross_origin, CORS

from server.management.user_manager import UserManager


def construct_user_blueprint(user_manager: UserManager):
    bp = Blueprint('user', __name__, url_prefix='/user')

    CORS(bp, resources={r"/user/*": {"origins": "http://localhost"}},headers=['Content-Type', 'Authorization'],
     expose_headers='Authorization')

    @bp.route('/login', methods=['POST', 'DELETE'])
    @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
    def user_session():
        if request.method == 'POST':
            return perfom_login()
        elif request.method == 'DELETE':
            return perfom_logout()

    def perfom_login():
        if 'username' in session:
            response = jsonify({'message': 'There is another user session.'})
            response.headers['Access-Control-Allow-Credentials'] = "true"
            return response, 400

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
        else:
            response = jsonify({'message': 'Login incorrect'})
            response.headers['Access-Control-Allow-Credentials'] = "true"
            return response, 401


        response = jsonify(is_correct_login)
        response.headers['Access-Control-Allow-Credentials']="true"
        return response

    def perfom_logout():
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
