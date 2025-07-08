from flask import Blueprint, jsonify
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/logout', methods=['POST', 'OPTIONS'])
@cross_origin()
def logout():
    # Untuk method OPTIONS, Flask otomatis handle jika method di route
    return jsonify({"message": "Logout successful"}), 200 