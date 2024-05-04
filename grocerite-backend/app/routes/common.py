from apiflask import APIBlueprint
from flask import request, jsonify
from ..db import db
from ..models import User, Member, Household
from ..api_utils import api_response

common_bp = APIBlueprint('common', __name__)


@common_bp.route('/dashboard/<string:user_id>', methods=['GET'])
def home_dashboard(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if user is None:
        return api_response(status='F', message='User not found', status_code=404)
    
    base_res_data = {
        'households': [],
        'active_lists': []
    }

    households = db.session.query(Household).\
        join(Member, Household.id == Member.household_idx).\
        join(User, Member.user_idx == User.id).\
        filter(User.user_id == user_id).\
        all()
    
    active_lists = [
        g.get_api_data() for h in households for g in h.grocery_lists if g.is_active
    ]

    if len(households) > 0:
        base_res_data['households'] = [h.get_api_data() for h in households]
        base_res_data['active_lists'] = active_lists
        
    return api_response(data=[base_res_data])