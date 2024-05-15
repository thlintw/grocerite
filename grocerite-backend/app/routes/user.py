from apiflask import APIBlueprint
from flask import request, jsonify
from ..db import db
from ..models import User, UserPreference, user_pref_keys
from ..api_utils import api_response
import time

user_bp = APIBlueprint('user', __name__)


# get profile
@user_bp.route('/profile_from_fb/<string:fb_uid>', methods=['GET'])
def get_user_profile_from_fb_uid(fb_uid):
    user = db.session.query(User).filter(User.fb_uid == fb_uid).first()
    if user is None:
        return api_response(data=[])
    return api_response(data=[user.get_api_data()])


# get self profile
@user_bp.route('/profile/get/<string:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if user is None:
        return api_response(status='F', message='User not found', status_code=404)
    return api_response(data=[user.get_api_data()])




# create user profile
@user_bp.route('/profile/create', methods=['POST'])
def create_user_profile():
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json    
    email = data.get('email', '')

    existing_user = db.session.query(User).filter(User.email == email).first()
    if existing_user:
        return api_response(status='F', message='User already exists', status_code=400)
    
    username = data.get('username', '')
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



# get user preferences
@user_bp.route('/profile/preferences/<string:user_id>', methods=['GET'])
def get_user_preferences(user_id):

    prefs = {
        key: '' for key in user_pref_keys
    }

    try:
        user_prefs = db.session.query(UserPreference).\
            filter(UserPreference.user.user_id == user_id).all()
        for p in user_prefs:
            prefs[p.pref_key] = p.pref_value
    except Exception as e:
        return api_response(status='F', message='Failed to get preferences', status_code=500)
    
    return api_response(data=[prefs])



# set user preferences
@user_bp.route('/profile/preferences/set/<string:user_id>', methods=['POST'])
def set_user_preferences(user_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json
    prefs = data.get('preferences', {})

    current_prefs = db.session.query(UserPreference).\
        filter(UserPreference.user.user_id == user_id).all()
    
    user = db.session.query(User).filter(User.user_id == user_id).first()

    try:
        for key, value in prefs.items():
            user_pref_row = filter(lambda p: p.key == key, current_prefs)
            if user_pref_row:
                user_pref_row.value = value
                db.session.merge(user_pref_row)
            else:
                user_pref_row = UserPreference(
                    user=user,
                    key=key,
                    value=value
                )
                db.session.add(user_pref_row)
            prefs[key] = user_pref_row.value
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return api_response(status='F', message='Failed to set preferences', status_code=500)
    
    return api_response(data=[prefs])