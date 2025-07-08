from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
import json

users_bp = Blueprint('users', __name__)

@users_bp.route('/check', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({"status": "OK"})

@users_bp.route('/', methods=['GET'])
def check():
    users = User.query.all()
    return jsonify([{'id_user': u.id_user, 'username': u.username, 'tipe_user': u.tipe_user} for u in users])

@users_bp.route('/<int:id_user>', methods=['GET'])
def get_user(id_user):
    user = User.query.get_or_404(id_user)
    return jsonify({'id_user': user.id_user, 'username': user.username, 'tipe_user': user.tipe_user})

@users_bp.route('/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    user = User.query.get_or_404(id_user)
    data = request.json
    user.username = data.get('username', user.username)
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    tipe_user = data.get('tipe_user', user.tipe_user)
    if tipe_user not in ['admin', 'staff', 'patien']:
        return jsonify({'error': 'Invalid tipe_user'}), 400
    user.tipe_user = tipe_user
    db.session.commit()
    return jsonify({'id_user': user.id_user, 'username': user.username, 'tipe_user': user.tipe_user})

@users_bp.route('/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    user = User.query.get_or_404(id_user)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

# JWT Register (tidak perlu login)
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    tipe_user = data.get('tipe_user', 'patien')
    if tipe_user not in ['admin', 'staff', 'patien']:
        return jsonify({'error': 'Invalid tipe_user'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, tipe_user=tipe_user)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered', 'id_user': user.id_user, 'username': user.username, 'tipe_user': user.tipe_user}), 201

# JWT Login (tidak perlu login)
@users_bp.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    identity = json.dumps({'id_user': user.id_user, 'username': user.username, 'tipe_user': user.tipe_user})
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'tipe_user': user.tipe_user})

# JWT Refresh
from flask_jwt_extended import jwt_required, get_jwt_identity
@users_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}) 

# Endpoint logout
@users_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    # Tidak perlu melakukan apapun, cukup response sukses
    return jsonify({"message": "Logout successful"}), 200 