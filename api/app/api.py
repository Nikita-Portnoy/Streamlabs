from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies, verify_jwt_in_request, jwt_required
from functools import wraps

from app.model.user.user import User

API = Blueprint('API', __name__)

def premium_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        jwt_claims = get_jwt()
        if not jwt_claims['is_premium']:
            abort(403)

        return fn(*args, **kwargs)
    return wrapper


@API.after_request
def refresh_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now_timestamp = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now_timestamp + timedelta(minutes=15))

        if target_timestamp > exp_timestamp:
            jwt_identity = get_jwt_identity()
            account = User(public_id=jwt_identity)
            
            access_token = create_access_token(identity=account, additional_claims={"is_premium": account.is_premium})
            set_access_cookies(response, access_token)
            
            return response
    except (RuntimeError, KeyError):
        return response

@API.route("/", methods=['GET'])
def route_root():

    return jsonify({'status': 'All good'}), 200

@API.route("/user/register", methods = ['POST'])
def route_user_register():
    request_data = request.json()

    # TODO Data Validation
    # TODO Duplicate Check

    try:
        User.new_user(request_data['first_name'], request_data['last_name'], request_data['email'], request_data['password'])
        account = User(email=request_data['email'])
        account_dict = account.to_dict()

        return jsonify({'user': account_dict}), 200
    except Exception as e:
        return jsonify({'error': 'Request Failed', 'meessage': str(e)}), 400

@API.route("/user/login", methods = ['POST'])
def route_user_login():
    request_data = request.json()

    try:
        account = User(email=request_data['email'])
        assert account.integrity, "Invalid Credentials"
        account_dict = account.to_dict()

        response = jsonify({'user': account_dict})

        access_token = create_access_token(identity=account, additional_claims={"is_premium": account.is_premium})
        set_access_cookies(response, access_token)

        return response, 200
    except Exception as e:
        return jsonify({'error': 'Request Failed', 'meessage': str(e)}), 400

@API.route("/checkouts/new", methods = ['GET'])
def route_checkouts_new():
    pass

@API.route("/checkouts", methods = ['POST'])
def route_checkouts():
    request_data = request.json()

@API.route("/statistics", methods = ['GET'])
@jwt_required()
def route_statistics():
    
    return jsonify({'statistics': [
        {'name': 'Stat_1', 'value': 25},
        {'name': 'Stat_2', 'value': 12},
        {'name': 'Stat_3', 'value': 17},
        {'name': 'Stat_4', 'value': 11},
        {'name': 'Stat_5', 'value': 120}
    ]})

@API.route("/premium/statistics", methods = ['GET'])
@premium_only
def route_premium_statistics():
    
    return jsonify({'statistics': [
        {'name': 'Premium_1', 'value': 11},
        {'name': 'Premium_2', 'value': 18},
        {'name': 'Premium_3', 'value': 25},
        {'name': 'Premium_4', 'value': 48},
        {'name': 'Premium_5', 'value': 120}
    ]})

