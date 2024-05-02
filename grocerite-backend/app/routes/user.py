from flask import Blueprint, request, jsonify
from ..db import db
from ..models import User
from ..api_utils import api_response
import time

user_bp = Blueprint('user', __name__)


# get self profile
@user_bp.route('/profile/<string:user_id>', methods=['GET'])
def get_profile(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if user is None:
        return api_response(404, 'User not found')
    return api_response(200, 'Success', user.to_dict())


# create user profile
@user_bp.route('/profile/create', methods=['POST'])
def create_profile():
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json    
    email = data.get('email')

    existing_user = db.session.query(User).filter(User.email == email).first()
    if existing_user:
        return api_response(status='F', message='User already exists', status_code=400)
    
    username = data.get('username', '')
    email = data.get('password', '')
    fb_uid = data.get('fb_uid', '')

    if not all([username, email, fb_uid]):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    user = User(
        username=username,
        email=email,
        fb_uid=fb_uid
    )

    try:
        db.session.add(user)
        db.session.commit()
        return api_response(data=[user.get_api_data()])
    except Exception as e:
        db.session.rollback()
        return api_response(status='F', message='Failed to create user', status_code=500)
    

# update user profile
# to be implemented



