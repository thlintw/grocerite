from apiflask import APIBlueprint
from flask import request, Response
import app
from ..db import db
from ..models import Member, Household, Container, GroceryList, Item, GroceryListItem, ItemCategory, GroceryListChangeLog, GroceryListChangeType, ContainerItem
from ..api_utils import api_response, needs_firebase_auth
import time, traceback

grocery_list_bp = APIBlueprint('grocery_list', __name__)



# list 
@grocery_list_bp.route('/grocery_list/<string:household_id>', methods=['GET'])
def list_grocery_lists(household_id):
    grocery_lists = db.session.query(Household).\
        filter(Household.id == household_id).\
        first().grocery_lists
    
    if len(grocery_lists) == 0:
        return api_response(data=[])
    else:
        data = [
            g.get_api_data() for g in grocery_lists
        ]
        
        return api_response(data=data)
    


# get
@grocery_list_bp.route('/grocery_list/get/<string:grocery_list_id>', methods=['GET'])
def get_grocery_list(grocery_list_id):
    grocery_list = db.session.query(GroceryList).filter(GroceryList.grocery_list_id == grocery_list_id).first()
    if grocery_list is None:
        return api_response(status='F', message='Grocery list not found', status_code=404)
    
    return api_response(data=[grocery_list.get_api_data()])



# create
@grocery_list_bp.route('/grocery_list/create/<string:household_id>', methods=['POST'])
def create_grocery_list(household_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'name',
        'iconIdx',
        'description',
        'asigneeMemberIdx',
        'items',
        'deadline'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    household = db.session.query(Household).filter(Household.id == household_id).first()
    if household is None:
        return api_response(status='F', message='Household not found', status_code=404)
    
    name = data.get('name', '')
    icon_idx = data.get('iconIdx', 0)
    description = data.get('description', '')
    asignee_member_idx = data.get('asigneeMemberIdx', None)
    grocery_items_raw = data.get('items', [])
    deadline = data.get('deadline', None)
    deadline_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(deadline / 1000))

    if any([
        not name,
        not icon_idx,
        not grocery_items_raw,
    ]):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    grocery_list = GroceryList(
        name=name,
        icon_idx=icon_idx,
        description=description,
        asignee_member_idx=asignee_member_idx,
        deadline=deadline,
        deadline_dt=deadline_dt,
        household=household
    )

    try:
        available_containers = db.session.query(Container).filter(Container.household_idx == household.id).all()

        for g_item in grocery_items_raw:
            itemIdx = g_item.get('itemIdx', None)
            name = g_item.get('name', '')
            category = g_item.get('category', '')
            target_container_idx = g_item.get('containerIdx', None)

            item = None
            container = None

            if itemIdx:
                item = db.session.query(Item).filter(Item.id == itemIdx).first()
            else:
                cate = db.session.query(ItemCategory).filter(ItemCategory.name == category).first()
                item = Item(
                    name=name,
                    category=cate,
                    household=household
                )
                db.session.add(item)

            if target_container_idx:
                container = filter(lambda x: x.id == target_container_idx, available_containers)[0]
            
            grocery_item = GroceryListItem(
                quantity=g_item.get('quantity', 1),
                target_container=container,
                item=item
            )

            db.session.add(grocery_item)
            grocery_list.items.append(grocery_item)
    
    except Exception as e:
        return api_response(status='F', message='Error creating grocery items', status_code=400)


    try:
        db.session.add(grocery_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error creating grocery list', status_code=400)
        
    return api_response(data=[grocery_list.get_api_data()])




# update
@grocery_list_bp.route('/grocery_list/update/<string:grocery_list_id>', methods=['PUT'])
def update_grocery_list(grocery_list_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    grocery_list = db.session.query(GroceryList).filter(GroceryList.grocery_list_id == grocery_list_id).first()
    if grocery_list is None:
        return api_response(status='F', message='Grocery list not found', status_code=404)
    
    data = request.json

    key_list = [
        'name',
        'iconIdx',
        'description',
        'asigneeMemberIdx',
        'items',
        'deadline'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    name = data.get('name', '')
    icon_idx = data.get('iconIdx', 0)
    description = data.get('description', '')
    asignee_member_idx = data.get('asigneeMemberIdx', None)
    grocery_items_raw = data.get('items', [])
    deadline = data.get('deadline', -1)
    deadline_dt = None
    if deadline:
        deadline_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(deadline / 1000))

    if any([
        not name,
        not icon_idx,
        not grocery_items_raw,
    ]):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    grocery_list.name = name
    grocery_list.icon_idx = icon_idx
    grocery_list.description = description
    grocery_list.asignee_member_idx = asignee_member_idx
    grocery_list.deadline = deadline
    grocery_list.deadline_dt = deadline_dt

    try:
        old_item_idxs = set([i.id for i in grocery_list.items])
        new_item_idxs = set([g_item.get('idx', None) for g_item in grocery_items_raw])

        items_to_delete = old_item_idxs - new_item_idxs

        available_containers = db.session.query(Container).filter(Container.household_idx == grocery_list.household_idx).all()

        for g_item in grocery_items_raw:
            idx = g_item.get('idx', None)
            if idx in items_to_delete:
                db.session.delete(g_item)

            item_idx = g_item.get('itemIdx', None)
            name = g_item.get('name', '')
            quantity = g_item.get('quantity', 1)
            category = g_item.get('category', '')
            target_container_idx = g_item.get('containerIdx', None)

            if not idx:
                item = None
                container = None

                if item_idx:
                    item = db.session.query(Item).filter(Item.id == item_idx).first()
                else:
                    cate = db.session.query(ItemCategory).filter(ItemCategory.name == category).first()
                    item = Item(
                        name=name,
                        category=cate,
                        household=grocery_list.household
                    )
                    db.session.add(item)

                if target_container_idx:
                    container = filter(lambda x: x.id == target_container_idx, available_containers)[0]

                grocery_item = GroceryListItem(
                    quantity=g_item.get('quantity', 1),
                    target_container=container,
                    item=item
                )

                db.session.add(grocery_item)
                grocery_list.items.append(grocery_item)
            else:
                grocery_item = filter(lambda x: x.id == idx, grocery_list.items)[0]
                grocery_item.quantity = quantity
                
                if target_container_idx != grocery_item.target_container.id:
                    container = filter(lambda x: x.id == target_container_idx, available_containers)[0]
                    grocery_item.target_container = container
                
                db.session.merge(grocery_item)


    except Exception as e:
        return api_response(status='F', message='Error updating grocery items', status_code=400)
    
    try:
        db.session.merge(grocery_list)
        db.session.commit()
        return api_response(data=[grocery_list.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error updating grocery list', status_code=400)
    


# delete
@grocery_list_bp.route('/grocery_list/delete/<string:grocery_list_id>', methods=['DELETE'])
def delete_grocery_list(grocery_list_id):
    grocery_list = db.session.query(GroceryList).filter(GroceryList.grocery_list_id == grocery_list_id).first()
    if grocery_list is None:
        return api_response(status='F', message='Grocery list not found', status_code=404)
    
    try:
        db.session.delete(grocery_list)
        db.session.commit()
        return api_response()
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error deleting grocery list', status_code=400)
    

connected_clients = []

# @grocery_list_bp.route('/grocery_list/tick_notif/<string:grocery_list_id>')
# def tick_grocery_list_notif(grocery_list_id):
#     def event_stream():
#         connected_clients.append(request.sid)

#     return Response(event_stream(), content_type='text/event-stream')

# def send_sse_update():
#     for client in connected_clients:
#         app.extensions['socketio'].emit('update', {'message': 'Grocery list updated'}, room=client)

# tick list item
@grocery_list_bp.route('/grocery_list/tick_item/<string:grocery_list_id>/<string:grocery_item_idx>', methods=['PUT'])
def tick_grocery_list_item(grocery_list_id, grocery_item_idx):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'member_idx'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)

    grocery_list = db.session.query(GroceryList).filter(GroceryList.grocery_list_id == grocery_list_id).first()
    if grocery_list is None:
        return api_response(status='F', message='Grocery list not found', status_code=404)
    
    member = db.session.query(Member).filter(Member.id == data['member_idx']).first()
    if member is None:
        return api_response(status='F', message='Member not found', status_code=404)
    
    grocery_item = filter(lambda x: x.id == grocery_item_idx, grocery_list.items)[0]
    
    grocery_item.ticked = True
    grocery_item.ticked_by = member
    grocery_item.ticked_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

    target_item = filter(lambda t: t.id == grocery_item.item.id, grocery_item.target_container.items)

    if len(target_item) == 0:
        target_item = ContainerItem(
            item_idx=grocery_item.item.id,
            quantity=grocery_item.quantity,
            container=grocery_item.target_container
        )
        db.session.add(target_item)
    else:
        target_item = target_item[0]
        target_item.quantity += grocery_item.quantity
        db.session.merge(target_item)

    change_log = GroceryListChangeLog(
        grocery_list=grocery_list,
        grocery_list_item=grocery_item,
        member=member,
        change_type=db.session.query(GroceryListChangeType).filter(GroceryListChangeType.name == 'TICKED').first(),
        value_before='0',
        value_after='1',
    )

    try:
        db.session.add(change_log)
        db.session.merge(grocery_item)
        db.session.commit()
        # send_sse_update({'message': f'itemIdx:{grocery_item_idx}|memberIdx:{data["member_idx"]}'})
        return api_response(data=[grocery_item.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error ticking grocery item', status_code=400)
    


# tick all items
@grocery_list_bp.route('/grocery_list/tick_all_items/<string:grocery_list_id>', methods=['PUT'])
def tick_all_grocery_list_items(grocery_list_id):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'member_idx'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    grocery_list = db.session.query(GroceryList).filter(GroceryList.grocery_list_id == grocery_list_id).first()
    if grocery_list is None:
        return api_response(status='F', message='Grocery list not found', status_code=404)
    
    member = db.session.query(Member).filter(Member.id == data['member_idx']).first()
    if member is None:
        return api_response(status='F', message='Member not found', status_code=404)
    
    for grocery_item in grocery_list.items:
        grocery_item.ticked = True
        grocery_item.ticked_by = member
        grocery_item.ticked_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

        target_item = filter(lambda t: t.id == grocery_item.item.id, grocery_item.target_container.items)

        if len(target_item) == 0:
            target_item = ContainerItem(
                item_idx=grocery_item.item.id,
                quantity=grocery_item.quantity,
                container=grocery_item.target_container
            )
            db.session.add(target_item)
        else:
            target_item = target_item[0]
            target_item.quantity += grocery_item.quantity
            db.session.merge(target_item)


        db.session.merge(grocery_item)

    change_log = GroceryListChangeLog(
        grocery_list=grocery_list,
        grocery_list_item=grocery_item,
        member=member,
        change_type=db.session.query(GroceryListChangeType).filter(GroceryListChangeType.name == 'BATCH_TICK').first(),
        value_before='BATCH',
        value_after='BATCH',
    )
    db.session.add(change_log)

    try:
        db.session.commit()
        return api_response(data=[grocery_list.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error ticking grocery items', status_code=400)



# untick list item
@grocery_list_bp.route('/grocery_list/untick_item/<string:grocery_list_id>/<string:grocery_item_idx>', methods=['PUT'])
def untick_grocery_list_item(grocery_list_id, grocery_item_idx):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'member_idx'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)

    grocery_list = db.session.query(GroceryList).filter(GroceryList.grocery_list_id == grocery_list_id).first()
    if grocery_list is None:
        return api_response(status='F', message='Grocery list not found', status_code=404)
    
    member = db.session.query(Member).filter(Member.id == data['member_idx']).first()
    if member is None:
        return api_response(status='F', message='Member not found', status_code=404)
    
    grocery_item = filter(lambda x: x.id == grocery_item_idx, grocery_list.items)[0]
    
    grocery_item.ticked = False
    grocery_item.ticked_by = None
    grocery_item.ticked_time = None

    target_item = filter(lambda t: t.id == grocery_item.item.id, grocery_item.target_container.items)

    if len(target_item) > 0:
        target_item = target_item[0]
        target_item.quantity -= grocery_item.quantity
        db.session.merge(target_item)

    change_log = GroceryListChangeLog(
        grocery_listß=grocery_list,
        grocery_list_item=grocery_item,
        member=member,
        change_type=db.session.query(GroceryListChangeType).filter(GroceryListChangeType.name == 'UNTICKED').first(),
        value_before='1',
        value_after='0',
    )

    try:
        db.session.add(change_log)
        db.session.merge(grocery_item)
        db.session.commit()
        return api_response(data=[grocery_item.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error unticking grocery item', status_code=400)
    



# edit single grocery item
@grocery_list_bp.route('/grocery_list/edit_item/<string:grocery_list_id>/<string:grocery_item_idx>', methods=['PUT'])
def edit_grocery_list_item(grocery_list_id, grocery_item_idx):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'member_idx',
        'quantity',
        'name',
        'target_container_idx'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    member = db.session.query(Member).filter(Member.id == data['member_idx']).first()
    if member is None:
        return api_response(status='F', message='Member not found', status_code=404)
    
    grocery_item = db.session.query(GroceryListItem).\
        filter(
            GroceryListItem.id == grocery_item_idx,
            GroceryListItem.grocery_list.grocery_list_id == grocery_list_id
        ).first()
    
    if grocery_item is None:
        return api_response(status='F', message='Grocery item not found', status_code=404)
    
    snapshot = f'name:{grocery_item.item.name}|quantity:{grocery_item.quantity}|container:{grocery_item.target_container.id}'
    
    new_quantity = data.get('quantity', 1)
    new_target_container_idx = data.get('containerIdx', None)

    new_name = data.get('name', None)
    if new_name != grocery_item.item.name:
        item = grocery_item.item
        item.name = new_name
        db.session.merge(item)

    if new_target_container_idx != grocery_item.target_container.id:
        new_container = db.session.query(Container).filter(Container.id == new_target_container_idx).first()
        if new_container is None:
            db.session.rollback()
            return api_response(status='F', message='Target container not found', status_code=404)
        grocery_item.target_container = new_container

    grocery_item.quantity = new_quantity

    new_snapshot = f'name:{grocery_item.item.name}|quantity:{grocery_item.quantity}|container:{grocery_item.target_container.id}'
    
    change_log = GroceryListChangeLog(
        grocery_list=grocery_item.grocery_list,
        grocery_list_item=grocery_item,
        member=member,
        change_type=db.session.query(GroceryListChangeType).filter(GroceryListChangeType.name == 'EDITED').first(),
        value_before=snapshot,
        value_after=new_snapshot,
    )

    try:
        db.session.add(change_log)
        db.session.merge(grocery_item)
        db.session.commit()
        return api_response(data=[grocery_item.get_api_data()])
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error editing grocery item', status_code=400)




# delete single grocery item
@grocery_list_bp.route('/grocery_list/delete_item/<string:grocery_list_id>/<string:grocery_item_idx>', methods=['DELETE'])
def delete_grocery_list_item(grocery_list_id, grocery_item_idx):
    if not request.is_json:
        return api_response(status='F', message='Request is not JSON', status_code=400)
    
    data = request.json

    key_list = [
        'member_idx'
    ]

    if not all(k in data for k in key_list):
        return api_response(status='F', message='Missing required fields', status_code=400)
    
    member = db.session.query(Member).filter(Member.id == data['member_idx']).first()
    if member is None:
        return api_response(status='F', message='Member not found', status_code=404)
    
    grocery_item = db.session.query(GroceryListItem).\
        filter(
            GroceryListItem.id == grocery_item_idx,
            GroceryListItem.grocery_list.grocery_list_id == grocery_list_id
        ).first()
    
    if grocery_item is None:
        return api_response(status='F', message='Grocery item not found', status_code=404)
    
    change_log = GroceryListChangeLog(
        grocery_list=grocery_item.grocery_list,
        grocery_list_item=grocery_item,
        member=member,
        change_type=db.session.query(GroceryListChangeType).filter(GroceryListChangeType.name == 'DELETED').first(),
        value_before='',
        value_after='',
    )

    try:
        db.session.add(change_log)
        db.session.delete(grocery_item)
        db.session.commit()
        return api_response()
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return api_response(status='F', message='Error deleting grocery item', status_code=400)
    



# get available items and containers
@grocery_list_bp.route('/grocery_list/available_items/<string:household_id>', methods=['GET'])
def get_available_items(household_id):
    available_items = db.session.query(Item).filter(Item.household_idx == household_id).all()
    
    data = [{
        'availableItems': [
            i.get_api_data() for i in available_items
        ],
        'availableContainers': [
            c.get_api_data() for c in db.session.query(Container).filter(Container.household_idx == household_id).all()
        ]
    }]

    return api_response(data=data)



