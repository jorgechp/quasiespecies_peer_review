from flask import (
    Blueprint, request, session
)
from flask_cors import cross_origin, CORS

from flaskr.utils import process_response
from management.user_manager import UserManager


def construct_user_blueprint(user_manager: UserManager, cors_exception: str, default_language= 'en'):
    bp = Blueprint('user', __name__, url_prefix='/user')

    CORS(bp, resources={r"/user*": {"origins": cors_exception}}, headers=['Content-Type', 'Authorization'],
     expose_headers='Authorization')


    @bp.route('/login', methods=['GET', 'POST', 'OPTIONS'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def user_session():
        if request.method == 'GET':
            return check_login()
        elif request.method == 'POST':
            return perfom_login()
        elif request.method == 'OPTIONS':
            response = process_response()
            return response, 200

    def check_login():
        is_current_login = 'username' in session
        response = process_response(is_current_login)
        return response

    def perfom_login():
        if 'username' in session:
            response = process_response({'message': 'There is another user session.'})
            return response, 400

        json_request = request.get_json(force=True)
        plain_nick = json_request['nick']
        plain_password = json_request['password']
        user_id = user_manager.get_user_id(plain_nick)

        if user_id is not None:
            is_correct_login = user_manager.check_user_password(user_id, plain_password)
        else:
            response = process_response({'message': 'Login incorrect'})
            return response, 401

        if is_correct_login:
            session['username'] = user_id
        else:
            response = process_response({'message': 'Login incorrect'})
            return response, 401

        response = process_response(is_correct_login)
        return response

    @bp.route('/login/recovery', methods=['POST', 'OPTIONS'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def user_recovery():
        if request.method == 'POST':
            return recovery_login()
        elif request.method == 'OPTIONS':
            response = process_response()
            return response, 200

    def recovery_login():
        json_request = request.get_json(force=True)
        if 'nick' not in json_request or 'mail' not in json_request:
            response = process_response({'message': 'User data not provided'})
            return response, 400
        user_nick = json_request['nick']
        mail = json_request['mail']
        user_id = user_manager.get_user_id(user_nick)
        user_data = user_manager.check_user_mail(user_id, mail)
        if user_data == -1:
            response = process_response({'message': 'Wrong user data'})
            return response, 400
        client_token, session_token = user_manager.get_recovery_token(user_nick)
        session['session_token'] = session_token
        user_manager.send_recovery_mail(mail, client_token)
        response = process_response(True)
        return response, 200

    @bp.route('/login/recovery/token', methods=['POST', 'OPTIONS'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def user_recovery_second_step():
        if request.method == 'POST':
            return recovery_change_password()
        elif request.method == 'OPTIONS':
            response = process_response()
            return response, 200

    def recovery_change_password():
        json_request = request.get_json(force=True)

        if 'token' not in json_request or 'password' not in json_request:
            response = process_response({'message': 'Token or data not provided'})
            return response, 400

        token_mail = json_request['token']
        if 'session_token' not in session:
            response = process_response({'message': 'Session token not found'})
            return response, 400

        session_token = session['session_token']
        plain_password = json_request['password']

        id_user_token = user_manager.check_user_token(token_mail, session_token)
        if id_user_token is not None:
            response = user_manager.change_user_password(id_user_token, plain_password)
            if response:
                user_manager.remove_user_token(id_user_token)
                del session['session_token']
            response = process_response(True, authorization__required=True)
            return response, 200
        else:
            response = process_response({'message': 'Wrong token data'})
            return response, 400

    @bp.route('/logout', methods=['POST', 'OPTIONS'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def perfom_logout():
        session.clear()
        response = process_response(True, authorization__required=True)
        return response

    @bp.route('/', methods=['POST'])
    def add_user():
        json_request = request.get_json(force=True)

        if 'mail' not in json_request or 'nick' not in json_request or 'password' not in json_request:
            response = process_response({'message': 'User data not provided'})
            return response, 400

        plain_mail = json_request['mail']
        nick = json_request['nick']
        plain_password = json_request['password']
        is_editor = json_request['editor']
        is_reviewer = json_request['reviewer']

        new_user = user_manager.add_user(nick, plain_mail, plain_password, is_editor, is_reviewer)
        if new_user == -1:
            response = process_response({'message': 'Duplicated user'})
            return response, 400
        return process_response(new_user, authorization__required=False, cors_header="*"), 200

    @bp.route('/mail', methods=['GET'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def get_mail():
        if 'username' not in session:
            response = process_response({'message': 'Not authorized'})
            return response, 401

        user_mail = user_manager.get_user_mail(session['username'])

        if len(user_mail) > 0:
            return process_response(user_mail), 200
        else:
            response = process_response({'message': 'Server error'})
            return response, 500

    @bp.route('/mail', methods=['POST'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def change_mail():
        json_request = request.get_json(force=True)

        if 'current_password' not in json_request or 'new_mail' not in json_request:
            response = process_response({'message': 'User data not provided'})
            return response, 400

        if 'username' not in session:
            response = process_response({'message': 'Not authorized'})
            return response, 401

        plain_password = json_request['current_password']
        plain_mail = json_request['new_mail']

        is_correct_login = user_manager.check_user_password(session['username'], plain_password)
        if is_correct_login:
            response = user_manager.change_mail(session['username'], plain_mail)
        else:
            response = process_response({'message': 'Incorrect login'})
            return response, 401

        return process_response(response), 200

    @bp.route('/role', methods=['GET'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def get_user_role():
        if 'username' not in session:
            response = process_response({'message': 'Not authorized'})
            return response, 401

        response = process_response(user_manager.get_user_role(session['username']))
        return response, 200

    @bp.route('/role', methods=['POST'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def change_user_role():
        json_request = request.get_json(force=True)

        if 'username' not in session:
            response = process_response({'message': 'Not authorized'})
            return response, 401

        if 'current_password' not in json_request:
            response = process_response({'message': 'User data not provided'})
            return response, 400

        plain_password = json_request['current_password']
        is_editor = json_request['editor']
        is_reviewer = json_request['reviewer']
        is_correct_login = user_manager.check_user_password(session['username'], plain_password)

        if is_correct_login:
            response = process_response(user_manager.change_user_role(session['username'], is_editor, is_reviewer))
        else:
            response = process_response({'message': 'Incorrect login'})
            return response, 401
        return response, 200

    @bp.route('/password', methods=['POST'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def change_password():
        json_request = request.get_json(force=True)

        if 'current_password' not in json_request:
            response = process_response({'message': 'User data not provided'})
            return response, 400

        if 'username' not in session:
            response = process_response({'message': 'Not authorized'})
            return response, 401

        plain_password = json_request['current_password']
        plain_new_password = json_request['new_password']

        is_correct_login = user_manager.check_user_password(session['username'], plain_password)
        if is_correct_login:
            response = user_manager.change_password(session['username'], plain_new_password)
        else:
            response = process_response({'message': 'Incorrect login'})
            return response, 401

        return process_response(response), 200

    @bp.route('/delete', methods=['POST'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def remove_user():
        json_request = request.get_json(force=True)

        if 'current_password' not in json_request:
            response = process_response({'message': 'User data not provided'})
            return response, 400

        if 'username' not in session:
            response = process_response({'message': 'Not authorized'})
            return response, 401

        plain_password = json_request['current_password']

        is_correct_login = user_manager.check_user_password(session['username'], plain_password)

        if is_correct_login:
            response = user_manager.remove_user(session['username'])
            session.clear()
        else:
            response = process_response({'message': 'Incorrect login'})
            return response, 401

        return process_response(response), 200

    @bp.route('/language', methods=['GET'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def get_user_language():
        if 'username' not in session:
            response = default_language
        else:
            response = user_manager.get_user_language(session['username'])

        return process_response(response), 200

    @bp.route('/language', methods=['PUT'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def set_user_language():
        json_request = request.get_json(force=True)
        if 'username' not in session:
            response = process_response({'message': 'Not authorized'})
            return response, 401

        language_code = json_request['language']
        response = user_manager.set_user_language(session['username'], language_code)

        return process_response(response), 200

    return bp
