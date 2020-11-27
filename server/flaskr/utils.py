from flask import jsonify


def process_response(response = None, authorization__required = True, cors_header = None):
    response = jsonify(response)
    if authorization__required:
        response.headers['Access-Control-Allow-Credentials'] = "true"
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    if cors_header != None:
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers['Access-Control-Allow-Origin'] = cors_header
    return response