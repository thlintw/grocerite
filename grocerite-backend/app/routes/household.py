from flask import Blueprint, request, jsonify
from ..db import db
from ..models import User, Member, Household, Container, ContainerType
from ..api_utils import api_response

household = Blueprint('household', __name__)

# household CRUD routes

# list
@household.route('/household/<string:user_id>', methods=['GET'])
def list_households(user_id):
    households = db.session.query(Household).\
        join(Member, Household.id == Member.household_idx).\
        join(User, Member.user_idx == User.id).\
        filter(User.user_id == user_id).\
        all()
    
    if len(households) == 0:
        return api_response(data=[])
    else:
        data = [
            h.get_api_data() for h in households
        ]
        
        return api_response(data=data)
    
    
# get
@household.route('/household/get/<string:household_id>', methods=['GET'])
def get_household(household_id):
    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    return api_response(data=[household.get_api_data()])

    

# create
@household.route('/household/create/<string:user_id>', methods=['POST'])
def create_household(user_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'name',
        'containers',
        'iconIdx',
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if user is None:
        return api_response(status='F', message='User not found', status_code=404)
    
    name = data.get('name', '')
    raw_containers = data.get('containers', [])
    icon_idx = data.get('iconIdx', None)

    if not name:
        return api_response(status='F', message='Missing name field', status_code=400)
    if len(raw_containers) == 0:
        return api_response(status='F', message='Should have at least 1 container', status_code=400)
    if icon_idx is None:
        return api_response(status='F', message='Missing iconIdx field', status_code=400)
    
    household = Household(
        name=name,
        icon_idx=icon_idx,
    )

    try:
        for raw_container in raw_containers:
            type = db.session.query(ContainerType).filter(ContainerType.name == raw_container['type']).first()
            if type is None:
                return api_response(status='F', message='Container type not found', status_code=404)
            container = Container(
                name=raw_container['name'],
                type=type,
                household=household,                
            )
            db.session.add(container)
            household.containers.append(container)

    except Exception as e:
        return api_response(status='F', message='Container creation error', status_code=400)

    try:
        db.session.add(household)
        db.session.commit()
    except Exception as e:
        return api_response(status='F', message='Household creation error', status_code=400)
    
    return api_response(data=[household.get_api_data()])



# update
@household.route('/household/update/<string:household_id>', methods=['PUT'])
def update_household(household_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)

    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    data = request.json

    key_list = [
        'name',
        'containers',
        'iconIdx',
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    name = data.get('name', '')
    raw_containers = data.get('containers', [])
    icon_idx = data.get('iconIdx', None)

    if not name:
        return api_response(status='F', message='Missing name field', status_code=400)
    if len(raw_containers) == 0:
        return api_response(status='F', message='Should have at least 1 container', status_code=400)
    if icon_idx is None:
        return api_response(status='F', message='Missing iconIdx field', status_code=400)
    
    household.name = name
    household.icon_idx = icon_idx
    try:
        for old_container in household.containers:
            db.session.delete(old_container)
        for raw_container in raw_containers:
            type = db.session.query(ContainerType).filter(ContainerType.name == raw_container['type']).first()
            if type is None:
                return api_response(status='F', message='Container type not found', status_code=404)
            container = Container(
                name=raw_container['name'],
                type=type,
                household=household,                
            )
            db.session.add(container)
            household.containers.append(container)
    except Exception as e:
        return api_response(status='F', message='Container modification error', status_code=400)
    
    try:
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        return api_response(status='F', message='Household modification error', status_code=400)



# delete
@household.route('/household/delete/<string:household_id>', methods=['DELETE'])
def delete_household(household_id):
    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    try:
        db.session.delete(household)
        db.session.commit()
        return api_response()
    except Exception as e:
        return api_response(status='F', message='Household deletion error', status_code=400)