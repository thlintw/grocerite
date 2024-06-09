from .db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table, Unicode, Text, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from .utils import get_id

class TimestampMixin:
    created_at = Column(BigInteger, default=int(datetime.utcnow().timestamp()), nullable=False)
    updated_at = Column(BigInteger, default=int(datetime.utcnow().timestamp()), onupdate=int(datetime.utcnow().timestamp()), nullable=False)


user_household = Table('user_household', db.metadata,
    Column('user_idx', Integer, ForeignKey('user.id'), primary_key=True),
    Column('household_idx', Integer, ForeignKey('household.id'), primary_key=True)
)

class User(TimestampMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    fb_uid = Column(String(100), nullable=False, unique=True)
    user_id = Column(String(100), nullable=False, unique=True, default=f'U-{get_id(l=9)}')
    nickname = Column(String(100))
    picture = Column(String(255))
    last_used_household_idx = Column(Integer, ForeignKey('household.id'))
    last_used_household = relationship('Household', backref='last_used_users', foreign_keys=[last_used_household_idx])
    households = relationship('Household', secondary='user_household', backref='users')

    def get_api_data(self):
        return {
            'idx': self.id,
            'username': self.username,
            'email': self.email,
            'fbUid': self.fb_uid,
            'userId': self.user_id,
            'nickname': self.nickname,
            'picture': self.picture,
            'preferences': self.get_preferences(),
            'households': [h.get_api_data() for h in self.households],
            'lastUsedHousehold': self.last_used_household.get_api_data() if self.last_used_household else None
        }
    
    def get_preferences(self):
        prefs = {
            key: '' for key in user_pref_keys
        }
        for p in self.preferences:
            prefs[p.key] = p.value
        return prefs
    

user_pref_keys = [
    'PREFERRED_LOCALE',
]

class UserPreference(TimestampMixin, db.Model):
    __tablename__ = 'user_preference'
    id = Column(Integer, primary_key=True)
    user_idx = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='preferences')
    key = Column(Unicode(100), nullable=False)
    value = Column(Unicode(255), nullable=False)


household_member = Table('household_member', db.metadata,
    Column('household_idx', Integer, ForeignKey('household.id'), primary_key=True),
    Column('member_idx', Integer, ForeignKey('member.id'), primary_key=True)
)

class Household(TimestampMixin, db.Model):
    __tablename__ = 'household'
    id = Column(Integer, primary_key=True)
    household_id = Column(String(100), nullable=False, unique=True, default=f'H-{get_id(l=9)}')
    name = Column(Unicode(100), nullable=False)
    members = relationship('Member', secondary=household_member, back_populates='household')
    containers = relationship('Container', back_populates='household')
    grocery_lists = relationship('GroceryList', back_populates='household')
    stores = relationship('Store', back_populates='household')
    icon_idx = Column(Integer) # not actually a reference... to be implemented

    def get_api_data(self):
        return {
            'idx': self.id,
            'name': self.name,
            'iconIdx': self.icon_idx,
            'householdId': self.household_id,
            'creatorId': self.members[0].user.user_id,
            'members': [
                m.get_api_data() for m in self.members
            ],
            'containers': [
                c.get_api_data() for c in self.containers
            ],
            'groceryLists': [
                g.get_api_data() for g in self.grocery_lists
            ],
        }


# class MemberPFP(TimestampMixin, db.Model):
#     __tablename__ = 'member_pfp'
#     id = Column(Integer, primary_key=True)
#     image_path = Column(String(255))

class Member(TimestampMixin, db.Model):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False) # user-defined name
    pfp_idx = Column(Integer)
    pfp_bg_color = Column(String(10))
    pfp_presenting = Column(String(10))
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='members', foreign_keys=[household_idx])
    user_idx = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='member')
    is_creator = Column(Boolean, default=False)

    def get_api_data(self):
        return {
            'idx': self.id,
            'name': self.name,
            'pfpIdx': self.pfp_idx,
            'pfpBgColor': self.pfp_bg_color,
            'pfpPresenting': self.pfp_presenting,
            'householdIdx': self.household_idx,
            'userId': self.user.user_id,
            'isCreator': self.is_creator
        }
    

class ContainerType(TimestampMixin, db.Model):
    __tablename__ = 'container_type'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False) # non-i18n name: 'fridge', 'freezer', 'pantry', 'cupboard', 'drawer', 'other'
    image_path = Column(String(255))

    def __repr__(self):
        return f'<ContainerType {self.name}>'

class Container(TimestampMixin, db.Model):
    __tablename__ = 'container'
    id = Column(Integer, primary_key=True)
    container_id = Column(String(100), nullable=False, unique=True)
    type_idx = Column(Integer, ForeignKey('container_type.id'), nullable=False)
    type = relationship('ContainerType', backref='containers')
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='containers')
    name = Column(Unicode(100), nullable=False) # user-defined name
    comment = Column(Text)

    def get_api_data(self):
        return {
            'idx': self.id,
            'name': self.name,
            'householdIdx': self.household_idx,
            'comment': self.comment,
            'type': self.type.name
        }

class ItemCategory(TimestampMixin, db.Model):
    __tablename__ = 'item_category'
    id = Column(Integer, primary_key=True)
    # non-i18n name: 'produce', 'dairy', 'meat', 'frozen', 'canned', 'baking', 'beverage', 'snack', 'other'
    name = Column(Unicode(100), nullable=False)
    image_path = Column(String(255))

class UserDefinedCategory(TimestampMixin, db.Model):
    __tablename__ = 'user_defined_category'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', backref='user_defined_categories')

class ItemIcon(TimestampMixin, db.Model):
    __tablename__ = 'item_icon'
    id = Column(Integer, primary_key=True)
    image_path = Column(String(255))

class Item(TimestampMixin, db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', backref='items')
    cate_idx = Column(Integer, ForeignKey('item_category.id'), nullable=False)
    cate = relationship('ItemCategory', backref='items')
    icon_idx = Column(Integer, ForeignKey('item_icon.id'), nullable=False)
    icon = relationship('ItemIcon', backref='items')

    def get_api_data(self):
        cq = sum([i.quantity for i in self.container_items if not i.is_removed])
        return {
            'idx': self.id,
            'name': self.name,
            'currentQuantity': cq
        }


class UserDefinedItem(TimestampMixin, db.Model):
    __tablename__ = 'user_defined_item'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    cate_idx = Column(Integer, ForeignKey('user_defined_category.id'), nullable=True)
    cate = relationship('UserDefinedCategory', backref='items')
    user_defined_cate_idx = Column(Integer, ForeignKey('item_category.id'), nullable=True)
    user_defined_cate = relationship('ItemCategory', backref='user_defined_items')
    icon_idx = Column(Integer, ForeignKey('item_icon.id'))
    icon = relationship('ItemIcon', backref='user_defined_items')


class GroceryListIcon(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list_icon'
    id = Column(Integer, primary_key=True)
    image_path = Column(String(255))


class GroceryList(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list'
    id = Column(Integer, primary_key=True)
    grocery_list_id = Column(String(100), nullable=False, unique=True, default=f'GL-{get_id(l=12)}')
    name = Column(Unicode(100), nullable=False) # user-defined name
    description = Column(Unicode(255))
    assignee_member_idx = Column(Integer, ForeignKey('member.id'), nullable=True) # can be unassigned
    assignee = relationship('Member', backref='grocery_lists')
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='grocery_lists')
    # icon_idx = Column(Integer, ForeignKey('item_icon.id'), nullable=False)
    # icon = relationship('ItemIcon', backref='grocery_lists')
    icon_idx= Column(Integer)
    items = relationship('GroceryListItem', back_populates='grocery_list')
    deadline = Column(BigInteger)
    deadline_dt = Column(DateTime)
    
    def get_api_data(self):
        return {
            'idx': self.id,
            'name': self.name,
            'iconIdx': self.icon_idx,
            'description': self.description,
            'assignee': self.assignee.get_api_data() if self.assignee else None,
            'householdIdx': self.household_idx,
            'iconIdx': self.icon_idx,
            'items': [
                i.get_api_data() for i in self.items
            ],
            'deadline': self.deadline,
            'deadlineString': self.deadline_dt.strftime('%Y-%m-%d') if self.deadline_dt else None
        }
    
    def is_active(self):
        return all([not i.ticked for i in self.items])
    

class Currency(TimestampMixin, db.Model):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    symbol = Column(Unicode(10), nullable=False)
    code = Column(Unicode(10), nullable=False)


class GroceryListItem(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list_item'
    id = Column(Integer, primary_key=True)
    item_idx = Column(Integer, ForeignKey('item.id'), nullable=True)
    item = relationship('Item', backref='grocery_list_items')
    user_defined_item_idx = Column(Integer, ForeignKey('user_defined_item.id'), nullable=True) # to be implemented
    user_defined_item = relationship('UserDefinedItem', backref='grocery_list_items')
    grocery_list_idx = Column(Integer, ForeignKey('grocery_list.id'), nullable=False)
    grocery_list = relationship('GroceryList', back_populates='items')
    label = Column(Unicode(100), nullable=False) # to be implemented
    quantity = Column(Unicode(50))
    unit = Column(Unicode(50)) # to be implemented
    ticked = Column(Boolean, default=False)
    ticked_time = Column(DateTime)
    ticked_by_member_idx = Column(Integer, ForeignKey('member.id'), nullable=True)
    ticked_by = relationship('Member', backref='grocery_list_items')
    store_idx = Column(Integer, ForeignKey('store.id'), nullable=True) # to be implemented
    store = relationship('Store', backref='grocery_list_items')
    target_container_idx = Column(Integer, ForeignKey('container.id'), nullable=False)
    target_container = relationship('Container', backref='grocery_list_items')
    currency_idx = Column(Integer, ForeignKey('currency.id'), nullable=True) # premium?
    currency = relationship('Currency', backref='grocery_list_items')
    price = Column(Unicode(50)) # premium?
    

    def get_api_data(self):
        return {
            'idx': self.id,
            'name': self.item.name,
            'quantity': self.quantity,
            'ticked': self.ticked,
            'tickedBy': self.ticked_by.get_api_data() if self.ticked_by else None,
            'targetContainer': self.target_container.name if self.target_container else None,
            'category': self.item.cate.name,
        }


class GroceryListChangeType(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list_change_type'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False) # tick, untick, comment, add, remove, edit, star, unstar, store, unstore

    
class GroceryListChangeLog(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list_change_log'
    id = Column(Integer, primary_key=True)
    grocery_list_idx = Column(Integer, ForeignKey('grocery_list.id'), nullable=False)
    grocery_list = relationship('GroceryList', backref='change_logs')
    member_idx = Column(Integer, ForeignKey('member.id'), nullable=False)
    member = relationship('Member', backref='change_logs')
    change_type_idx = Column(Integer, ForeignKey('grocery_list_change_type.id'), nullable=False)
    change_type = relationship('GroceryListChangeType', backref='change_logs')
    grocery_list_item_idx = Column(Integer, ForeignKey('grocery_list_item.id'), nullable=True)
    grocery_list_item = relationship('GroceryListItem', backref='change_logs')
    value_before = Column(String(255))
    value_after = Column(String(255))


class ContainerItem(TimestampMixin, db.Model):
    __tablename__ = 'container_item'
    id = Column(Integer, primary_key=True)
    item_idx = Column(Integer, ForeignKey('item.id'), nullable=True)
    item = relationship('Item', backref='container_items')
    user_defined_item_idx = Column(Integer, ForeignKey('user_defined_item.id'), nullable=True)
    user_defined_item = relationship('UserDefinedItem', backref='container_items')
    container_idx = Column(Integer, ForeignKey('container.id'), nullable=False)
    container = relationship('Container', backref='items')
    store_idx = Column(Integer, ForeignKey('store.id'), nullable=True)
    store = relationship('Store', backref='container_items')
    quantity = Column(Unicode(50))
    comment = Column(Text)
    is_removed = Column(Boolean, default=False)
    


class Store(TimestampMixin, db.Model):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    store_id = Column(String(100), nullable=False, unique=True)
    name = Column(Unicode(100), nullable=False)
    location = Column(Unicode(255))
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='stores')


class HouseholdConfig(TimestampMixin, db.Model):
    __tablename__ = 'household_config'
    id = Column(Integer, primary_key=True)
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', backref='config')
    key = Column(Unicode(100), nullable=False)
    value = Column(Unicode(255), nullable=False) 
