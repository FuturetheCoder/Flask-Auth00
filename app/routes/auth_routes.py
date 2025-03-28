from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.validators import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    response, status_code = AuthService.register(request.get_json())
    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    response, status_code = AuthService.login(request.get_json())
    return jsonify(response), status_code

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    try:
        return jsonify(current_user.to_dict), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching profile', 'error': str(e)}), 500 