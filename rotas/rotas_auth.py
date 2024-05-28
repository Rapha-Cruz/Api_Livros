from flask import Blueprint, request, jsonify
from utils.auth import generate_token, token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Hello {current_user}! This is a protected route.'})