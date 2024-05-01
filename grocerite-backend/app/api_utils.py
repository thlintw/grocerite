from flask import make_response, jsonify

def api_response(status='S', message='', data=None, status_code=200):
    response = {
        'status': status,
        'message': message,
        'data': data
    }
    return make_response(jsonify(response), status_code)