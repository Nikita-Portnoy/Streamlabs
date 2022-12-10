from flask import Blueprint, jsonify, request

API = Blueprint('API', __name__)

@API.route("/", methods=['GET'])
def route_root():

    return jsonify({'status': 'All good'}), 200

@API.route("/user/register", methods = ['POST'])
def route_user_register():
    pass

@API.route("/user/login", methods = ['POST'])
def route_user_login():
    pass

# Protected
@API.route("/statistics", methods = ['GET'])
def route_statistics():
    
    return jsonify({'statistics': [
        {'name': 'Stat_1', 'value': 25},
        {'name': 'Stat_2', 'value': 12},
        {'name': 'Stat_3', 'value': 17},
        {'name': 'Stat_4', 'value': 11},
        {'name': 'Stat_5', 'value': 120}
    ]})

@API.route("/premium/statistics", methods = ['GET'])
def route_premium_statistics():
    
    return jsonify({'statistics': [
        {'name': 'Premium_1', 'value': 11},
        {'name': 'Premium_2', 'value': 18},
        {'name': 'Premium_3', 'value': 25},
        {'name': 'Premium_4', 'value': 48},
        {'name': 'Premium_5', 'value': 120}
    ]})

