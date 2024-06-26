from apiflask import APIBlueprint
from flask import request
from ..db import db
from ..models import User, Member, Household, Container, ContainerType, ContainerItem, GroceryList, GroceryListItem
from ..api_utils import api_response
import traceback
from ..utils import get_id

household_bp = APIBlueprint('household', __name__)

# household CRUD routes

# list
@household_bp.route('/household/<string:user_id>', methods=['GET'])
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
@household_bp.route('/household/get/<string:household_id>', methods=['GET'])
def get_household(household_id):
    household = db.session.query(Household).filter(Household.household_id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    return api_response(data=[household.get_api_data()])

    

# create
@household_bp.route('/household/create/<string:user_id>', methods=['POST'])
def create_household(user_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'name',
        'containers',
        'iconIdx',
        'creator'
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

    types = db.session.query(ContainerType).all()

    try:
        creatorName = data['creator']['name']
        creatorPfpIdx = data['creator']['pfpIdx']
        creatorPfpBgColor = data['creator']['pfpBgColor']
        creatorPfpPresenting = data['creator']['pfpPresenting']

        creator = Member(
            user=user,
            household=household,
            name=creatorName,
            pfp_idx=creatorPfpIdx,
            pfp_bg_color=creatorPfpBgColor,
            pfp_presenting=creatorPfpPresenting,
            is_creator=True
        )

        db.session.add(creator)

    except Exception as e:
        print(traceback.format_exc())
        return api_response(status='F', message='Creator creation error', status_code=400)

    try:
        for raw_container in raw_containers:
            type = list(filter(lambda t: t.name == raw_container['type'], types))
            if len(type) == 0:
                return api_response(status='F', message='Container type not found', status_code=404)
            container = Container(
                name=raw_container['name'],
                type=type[0],
                household=household,
                container_id=f'C-{get_id(l=10)}'
            )
            db.session.add(container)

    except Exception as e:
        print(traceback.format_exc())
        return api_response(status='F', message='Container creation error', status_code=400)

    try:
        db.session.add(household)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(traceback.format_exc())
        return api_response(status='F', message='Household creation error', status_code=400)
    
    return api_response(data=[household.get_api_data()])



# update
@household_bp.route('/household/update/<string:household_id>', methods=['PUT'])
def update_household(household_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)

    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    data = request.json

    key_list = [
        'name',
        # 'containers',
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

    # try:
    #     for old_container in household.containers:
    #         db.session.delete(old_container)
    #     for raw_container in raw_containers:
    #         type = db.session.query(ContainerType).filter(ContainerType.name == raw_container['type']).first()
    #         if type is None:
    #             return api_response(status='F', message='Container type not found', status_code=404)
    #         container = Container(
    #             name=raw_container['name'],
    #             type=type,
    #             household=household,                
    #         )
    #         db.session.add(container)
    #         household.containers.append(container)
    # except Exception as e:
    #     return api_response(status='F', message='Container modification error', status_code=400)
    
    try:
        db.session.merge(household)
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Household modification error', status_code=400)
    


# update name only
@household_bp.route('/household/update_name/<string:household_id>', methods=['PUT'])
def update_household_name(household_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)

    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    data = request.json

    key_list = [
        'name',
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    name = data.get('name', '')

    if not name:
        return api_response(status='F', message='Missing name field', status_code=400)
    
    household.name = name

    try:
        db.session.merge(household)
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Household modification error', status_code=400)
    




# update icon only
@household_bp.route('/household/update_icon/<string:household_id>', methods=['PUT'])
def update_household_icon(household_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)

    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    data = request.json

    key_list = [
        'iconIdx',
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    icon_idx = data.get('iconIdx', None)

    if icon_idx is None:
        return api_response(status='F', message='Missing iconIdx field', status_code=400)
    
    household.icon_idx = icon_idx

    try:
        db.session.merge(household)
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Household modification error', status_code=400)



# delete
@household_bp.route('/household/delete/<string:household_id>', methods=['DELETE'])
def delete_household(household_id):
    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    try:
        db.session.delete(household)
        db.session.commit()
        return api_response()
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Household deletion error', status_code=400)
    



# add member
@household_bp.route('/household/add_member/<string:household_id>', methods=['POST'])
def add_household_member(household_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'userId',
        'pfpIdx',
        'pfpBgColor',
        'pfpPresenting',
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    user = db.session.query(User).filter(User.user_id == data['user_id']).first()
    if user is None:
        return api_response(status='F', message='User not found', status_code=404)
    
    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    name = data.get('name', '')
    pfp_idx = data.get('pfpIdx', None)
    pfp_bg_color = data.get('pfpBgColor', None)
    pfp_presenting = data.get('pfpPresenting', None)
    
    member = Member(
        user=user,
        household=household,
        name=name,
        pfp_idx=pfp_idx,
        pfp_bg_color=pfp_bg_color,
        pfp_presenting=pfp_presenting,
        is_creator=False
    )

    household.members.append(member)
    user.households.append(household)

    try:
        db.session.merge(household)
        db.session.add(member)
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Member creation error', status_code=400)
    


# delete member
@household_bp.route('/household/delete_member/<string:household_id>/<int:member_idx>', methods=['DELETE'])
def delete_household_member(household_id, member_idx):
    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    member = db.session.query(Member).filter(Member.id == member_idx).first()
    if member is None:
        return api_response(status='F', message='Member not found', status_code=404)
    
    if member in household.members:
        household.members.remove(member)
    
    try:
        db.session.delete(member)
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Member deletion error', status_code=400)
    



# update container (single)
@household_bp.route('/household/update_container/<string:household_id>/<int:container_idx>', methods=['PUT'])
def update_household_container(household_id, container_idx):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    container = db.session.query(Container).filter(Container.id == container_idx).first()
    if container is None:
        return api_response(status='F', message='Container not found', status_code=404)
    
    data = request.json

    key_list = [
        'name',
        'type',
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    name = data.get('name', '')
    type = db.session.query(ContainerType).filter(ContainerType.name == data['type']).first()
    if type is None:
        return api_response(status='F', message='Container type not found', status_code=404)
    
    container.name = name
    container.type = type

    try:
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Container modification error', status_code=400)
    




# manage container item
@household_bp.route('/household/manage_item/<string:household_id>/<int:container_idx>/<string:container_item_idx>', methods=['PUT'])
def manage_household_container_item(household_id, container_idx, container_item_idx):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    keylist = [
        'name',
        'quantity',
    ]

    data = request.json

    if not all(k in data for k in keylist):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    container_item = db.session.query(ContainerItem).\
        filter(
            ContainerItem.container.household.household_id == household_id,
            ContainerItem.container.id == container_idx,
            ContainerItem.id == container_item_idx
        ).first()
    
    if container_item is None:
        return api_response(status='F', message='Container item not found', status_code=404)
    
    name = data['name']

    if name != container_item.item.name:
        item = container_item.item
        item.name = name
        db.session.merge(item)

    container_item.quantity = data['quantity']

    db.session.merge(container_item)

    try:
        db.session.commit()
        return api_response(data=[container_item.container.household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Container item modification error', status_code=400)









# delete container
@household_bp.route('/household/delete_container/<string:household_id>/<int:container_idx>', methods=['DELETE'])
def delete_household_container(household_id, container_idx):
    container = db.session.query(Container).\
        filter(
            Container.household.household_id == household_id,
            Container.id == container_idx
        ).first()
    
    if container is None:
        return api_response(status='F', message='Container not found', status_code=404)
    
    for item in container.items:
        db.session.delete(item)

    db.session.delete(container)
    
    try:
        db.session.commit()
        return api_response(data=[container.household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Container deletion error', status_code=400)
    




# bulk add item to grocery list
@household_bp.route('/household/bulk_add_item_to_list/<string:household_id>/<int:container_idx>', methods=['POST'])
def bulk_add_item_to_list(household_id, container_idx):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'items',
        'target_list_idx'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)

    target_list = db.session.query(GroceryList).\
        filter(
            GroceryList.household.household_id == household_id,
            GroceryList.id == data['target_list_idx']
        ).first()
    
    if target_list is None:
        return api_response(status='F', message='Target list not found', status_code=404)
    
    items = db.session.query(ContainerItem).\
        filter(
            ContainerItem.container.id == container_idx,
            ContainerItem.id.in_([int(c_item['idx']) for c_item in data['items']])
        ).all()
    
    if len(items) == 0:
        return api_response(status='F', message='No items found', status_code=404)
    
    for c_item in data['items']:
        idx = int(c_item['idx'])
        quantity = int(c_item['quantity'])

        new_grocery_item = GroceryListItem(
            item_idx=idx,
            quantity=quantity,
            grocery_list=target_list,
            target_container_idx=container_idx
        )

        db.session.add(new_grocery_item)

    try:
        db.session.commit()
        return api_response(data=[target_list.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Grocery list item addition error', status_code=400)





# create container
@household_bp.route('/household/create_container/<string:household_id>', methods=['POST'])
def create_container(household_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    household = db.session.query(Household).filter(Household.household_id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    data = request.json

    key_list = [
        'name',
        'type',
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    name = data.get('name', '')
    type = db.session.query(ContainerType).filter(ContainerType.name == data['type']).first()
    if type is None:
        return api_response(status='F', message='Container type not found', status_code=404)
    
    container = Container(
        name=name,
        type=type,
        household=household
    )

    try:
        db.session.add(container)
        db.session.commit()
        return api_response(data=[household.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Container creation error', status_code=400)