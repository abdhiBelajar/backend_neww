from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

data_protected_bp = Blueprint('data_protected', __name__)

@data_protected_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user = json.loads(get_jwt_identity())
    tipe_user = user.get("tipe_user", "patien")
    roles = [tipe_user]
    # Response berbeda sesuai role
    if tipe_user == "admin":
        message = "Welcome, Admin! You have full access."
    elif tipe_user == "staff":
        message = "Welcome, Staff! You have staff-level access."
    elif tipe_user == "patien":
        message = "Welcome, Patient! You have patient-level access."
    else:
        message = "Unknown role."
    return jsonify({
        "message": message,
        "user_logged": user,
        "roles": roles
    }), 200 