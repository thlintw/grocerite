from apiflask import APIBlueprint
from flask import jsonify
from ..api_utils import api_response
from ..utils import get_id
from firebase_admin import firestore

main = APIBlueprint('main', __name__)

@main.route('/')
def index():
    return api_response(data=['OK'])

@main.route('/wake_up')
def wake_up():
    return api_response(data=['god morgon!'])



from .household import household_bp
from .common import common_bp
from .grocery_list import grocery_list_bp
from .user import user_bp

main.register_blueprint(common_bp)
main.register_blueprint(household_bp)
main.register_blueprint(grocery_list_bp)
main.register_blueprint(user_bp)


@main.route('/test')
def test():
    data = {
        'items': [
            {
                'name': 'apple',
                'quantity': 5
            },
            {
                'name': 'banana',
                'quantity': 9
            }
        ],
    }

    fb = firestore.client()
    doc_ref = fb.collection('test').document('wfiQlTREK4Z0LVbWm9E6')
    doc_ref.set(data)

    return api_response(data=['OK'])