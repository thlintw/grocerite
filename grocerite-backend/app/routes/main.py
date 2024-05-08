from apiflask import APIBlueprint
from flask import jsonify
from ..api_utils import api_response
from ..utils import get_id

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

import time

@main.route('/test')
def test():
    a = set([3, 5, 6, 7, 8, 9])
    b = set([1, 2, 3, 4, 5])

    print(3 in b-a)

    return api_response(data=[list(a-b), list(b-a)])