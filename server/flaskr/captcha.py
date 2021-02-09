import requests as req

from flask import (
    Blueprint, request, session,  abort
)
from flask_cors import CORS, cross_origin

from flaskr.utils import process_response



def construct_captcha_blueprint(secret_key: str, cors_exception: str):
    bp = Blueprint('captcha', __name__, url_prefix='/captcha')
    CORS(bp, resources={r"/captcha*": {"origins": "https://localhost/*"}},headers=['Content-Type', 'Authorization'],
     expose_headers='Authorization')

    @bp.route('/token_validate', methods=['POST'])
    @cross_origin(origin=cors_exception, headers=['Content- Type', 'Authorization'])
    def validate_captcha():
        json_request = request.get_json(force=True)
        if 'recaptcha' not in json_request:
            response = process_response({'success': False, 'message': 'Captcha data not provided'})
            return response, 400

        token = json_request['recaptcha']

        url = "https://www.google.com/recaptcha/api/siteverify?secret={}&response={}&remoteip={}"\
                    .format(secret_key, token, request.remote_addr)

        response = req.get(url)
        if response.ok:
            response = process_response({'success': True, 'message': 'recaptcha passed'})
            return response, 200
        else:
            response = process_response({'success': False, 'message': 'recaptcha failed'})
            return response, 400

    return bp