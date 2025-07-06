from flask import Blueprint, request, jsonify
from models import db, Service

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{'id_layanan': s.id_layanan, 'nama_layanan': s.nama_layanan, 'deskripsi': s.deskripsi, 'tarif': str(s.tarif)} for s in services])

@services_bp.route('/<int:id_layanan>', methods=['GET'])
def get_service(id_layanan):
    s = Service.query.get_or_404(id_layanan)
    return jsonify({'id_layanan': s.id_layanan, 'nama_layanan': s.nama_layanan, 'deskripsi': s.deskripsi, 'tarif': str(s.tarif)})

@services_bp.route('/', methods=['POST'])
def create_service():
    data = request.json
    s = Service(
        nama_layanan=data['nama_layanan'],
        deskripsi=data.get('deskripsi'),
        tarif=data.get('tarif')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'id_layanan': s.id_layanan}), 201

@services_bp.route('/<int:id_layanan>', methods=['PUT'])
def update_service(id_layanan):
    s = Service.query.get_or_404(id_layanan)
    data = request.json
    s.nama_layanan = data.get('nama_layanan', s.nama_layanan)
    s.deskripsi = data.get('deskripsi', s.deskripsi)
    s.tarif = data.get('tarif', s.tarif)
    db.session.commit()
    return jsonify({'id_layanan': s.id_layanan})

@services_bp.route('/<int:id_layanan>', methods=['DELETE'])
def delete_service(id_layanan):
    s = Service.query.get_or_404(id_layanan)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Service deleted'}) 