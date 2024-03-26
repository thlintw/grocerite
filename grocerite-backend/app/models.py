from .db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table, Unicode
from sqlalchemy.orm import relationship
from datetime import datetime

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

user_household = Table('user_household', db.metadata,
    Column('user_idx', Integer, ForeignKey('user.id'), primary_key=True),
    Column('household_idx', Integer, ForeignKey('household.id'), primary_key=True)
)

class User(TimestampMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    f_uid = Column(String(100), nullable=False, unique=True)
    nickname = Column(String(100))
    picture = Column(String(255))    
    households = relationship('Household', secondary='user_household', back_populates='users')    

household_member = Table('household_member', db.metadata,
    Column('household_idx', Integer, ForeignKey('household.id'), primary_key=True),
    Column('member_idx', Integer, ForeignKey('member.id'), primary_key=True)
)

class Household(TimestampMixin, db.Model):
    __tablename__ = 'household'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    members = relationship('Member', secondary=household_member, back_populates='households')
    containers = relationship('Container', back_populates='household')
    grocery_lists = relationship('GroceryList', back_populates='household')
    stores = relationship('Store', back_populates='household')

class MemberPFP(TimestampMixin, db.Model):
    __tablename__ = 'member_pfp'
    id = Column(Integer, primary_key=True)
    image_path = Column(String(255), nullable=False)

class Member(TimestampMixin, db.Model):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False) # user-defined name
    pfp_idx = Column(Integer, ForeignKey('member_pfp.id'), nullable=False)
    pfp = relationship('MemberPFP', back_populates='members')
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='members')
    user_idx = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='households')

class ContainerType(TimestampMixin, db.Model):
    __tablename__ = 'container_type'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False) # non-i18n name: 'fridge', 'freezer', 'pantry', 'cupboard', 'drawer', 'other'
    image_path = Column(String(255), nullable=False)

class Container(TimestampMixin, db.Model):
    __tablename__ = 'container'
    id = Column(Integer, primary_key=True)
    type_idx = Column(Integer, ForeignKey('container_type.id'), nullable=False)
    type = relationship('ContainerType', back_populates='containers')
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='containers')
    name = Column(Unicode(100), nullable=False) # user-defined name

class GroceryList(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list'
    id = Column(Integer, primary_key=True)
    starred = Column(Boolean, default=False)
    name = Column(Unicode(100), nullable=False) # user-defined name
    description = Column(Unicode(255))
    asignee_member_idx = Column(Integer, ForeignKey('member.id'), nullable=True) # can be unassigned
    asignee = relationship('Member', back_populates='grocery_lists')
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='grocery_lists')
    items = relationship('GroceryListItem', back_populates='grocery_list')

class GroceryListItemCate(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list_item_cate'
    id = Column(Integer, primary_key=True)
    # non-i18n name: 'produce', 'dairy', 'meat', 'frozen', 'canned', 'baking', 'beverage', 'snack', 'other'
    name = Column(Unicode(100), nullable=False) 
    image_path = Column(String(255), nullable=False)

class GroceryListItem(TimestampMixin, db.Model):
    __tablename__ = 'grocery_list_item'
    id = Column(Integer, primary_key=True)
    cate_idx = Column(Integer, ForeignKey('grocery_list_item_cate.id'), nullable=False)
    cate = relationship('GroceryListItemCate', back_populates='items')
    name = Column(Unicode(100), nullable=False)
    quantity = Column(Unicode(50))
    ticked = Column(Boolean, default=False)
    ticked_time = Column(DateTime)
    ticked_by_member_idx = Column(Integer, ForeignKey('member.id'), nullable=True)
    ticked_by = relationship('Member', back_populates='grocery_list_items')
    place = Column(Unicode(100))
    grocery_list_idx = Column(Integer, ForeignKey('grocery_list.id'), nullable=False)
    grocery_list = relationship('GroceryList', back_populates='items')

class Store(TimestampMixin, db.Model):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    location = Column(Unicode(255))
    household_idx = Column(Integer, ForeignKey('household.id'), nullable=False)
    household = relationship('Household', back_populates='stores')