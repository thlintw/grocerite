from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Household

household = Blueprint('household', __name__)

@household.route('/households', methods=['POST'])
def create_household():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    household = Household(name=name)
    db.session.add(household)
    db.session.commit()
    return jsonify({'id': household.id, 'name': household.name}), 201

@household.route('/households/<int:id>', methods=['GET'])
def get_household(id):
    household = Household.query.get(id)
    if household is None:
        return jsonify({'error': 'Household not found'}), 404
    return jsonify({'id': household.id, 'name': household.name})

@household.route('/households', methods=['GET'])
def list_households():
    households = Household.query.all()
    return jsonify([{'id': h.id, 'name': h.name} for h in households])

@household.route('/households/<int:id>', methods=['PUT'])
def update_household(id):
    household = Household.query.get(id)
    if household is None:
        return jsonify({'error': 'Household not found'}), 404
    data = request.get_json()
    household.name = data.get('name', household.name)
    db.session.commit()
    return jsonify({'id': household.id, 'name': household.name})

@household.route('/households/<int:id>', methods=['DELETE'])
def delete_household(id):
    household = Household.query.get(id)
    if household is None:
        return jsonify({'error': 'Household not found'}), 404
    db.session.delete(household)
    db.session.commit()
    return jsonify({'success': True})