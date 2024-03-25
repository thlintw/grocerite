from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Hello, World!"})


@main.route('/test')
def t():
    return jsonify({"message": "Hello, World!"})
