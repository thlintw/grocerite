
from functools import wraps
from flask import make_response, jsonify, request
import firebase_admin
from firebase_admin import auth

def api_response(status='S', message='', data=None, status_code=200):
    response = {
        'status': status,
        'message': message,
        'data': data if data is not None else []
    }
    return make_response(jsonify(response), status_code)


def needs_firebase_auth(f):
    @wraps(f)

    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return api_response(status='F', message='Authorization header is missing', status_code=403)

        id_token = auth_header.split(' ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            kwargs['decoded_token'] = decoded_token
        except firebase_admin.auth.InvalidIdTokenError:
            return api_response(status='F', message='Authorization header is invalid', status_code=403)
        except Exception as e:
            return api_response(status='F', message='Error decoding token', status_code=403)

        return f(*args, **kwargs)
    
    return decorated_function