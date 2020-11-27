from flask import jsonify


def process_response(response = None, authorization__required = True):
    response = jsonify(response)
    if authorization__required:
        response.headers['Access-Control-Allow-Credentials'] = "true"
    return response