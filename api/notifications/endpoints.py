from flask import Blueprint, request, jsonify
from models import db, Notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([{'id_notifikasi': n.id_notifikasi, 'id_user': n.id_user, 'pesan': n.pesan, 'tanggal_notifikasi': n.tanggal_notifikasi} for n in notifications])

@notifications_bp.route('/<int:id_notifikasi>', methods=['GET'])
def get_notification(id_notifikasi):
    n = Notification.query.get_or_404(id_notifikasi)
    return jsonify({'id_notifikasi': n.id_notifikasi, 'id_user': n.id_user, 'pesan': n.pesan, 'tanggal_notifikasi': n.tanggal_notifikasi})

@notifications_bp.route('/', methods=['POST'])
def create_notification():
    data = request.json
    n = Notification(id_user=data['id_user'], pesan=data['pesan'])
    db.session.add(n)
    db.session.commit()
    return jsonify({'id_notifikasi': n.id_notifikasi}), 201

@notifications_bp.route('/<int:id_notifikasi>', methods=['PUT'])
def update_notification(id_notifikasi):
    n = Notification.query.get_or_404(id_notifikasi)
    data = request.json
    n.pesan = data.get('pesan', n.pesan)
    db.session.commit()
    return jsonify({'id_notifikasi': n.id_notifikasi})

@notifications_bp.route('/<int:id_notifikasi>', methods=['DELETE'])
def delete_notification(id_notifikasi):
    n = Notification.query.get_or_404(id_notifikasi)
    db.session.delete(n)
    db.session.commit()
    return jsonify({'message': 'Notification deleted'}) 