from flask import Blueprint, request, jsonify
from models import db, Service

services_bp = Blueprint('services', __name__, url_prefix=None)

@services_bp.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_services():
    services = Service.query.all()
    return jsonify([{'id_layanan': s.id_layanan, 'nama_layanan': s.nama_layanan, 'deskripsi': s.deskripsi, 'tarif': str(s.tarif)} for s in services])

@services_bp.route('/<int:id_layanan>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_service(id_layanan):
    s = Service.query.get_or_404(id_layanan)
    return jsonify({'id_layanan': s.id_layanan, 'nama_layanan': s.nama_layanan, 'deskripsi': s.deskripsi, 'tarif': str(s.tarif)})

@services_bp.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
def create_service():
    data = request.json
    # Cek apakah nama_layanan sudah ada
    existing = Service.query.filter_by(nama_layanan=data['nama_layanan']).first()
    if existing:
        return jsonify({'error': 'Nama layanan sudah ada, gunakan nama lain.'}), 400
    s = Service(
        nama_layanan=data['nama_layanan'],
        deskripsi=data.get('deskripsi'),
        tarif=data.get('tarif')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'id_layanan': s.id_layanan}), 201

@services_bp.route('/<int:id_layanan>', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def update_service(id_layanan):
    s = Service.query.get_or_404(id_layanan)
    data = request.json
    s.nama_layanan = data.get('nama_layanan', s.nama_layanan)
    s.deskripsi = data.get('deskripsi', s.deskripsi)
    s.tarif = data.get('tarif', s.tarif)
    db.session.commit()
    return jsonify({'id_layanan': s.id_layanan})

@services_bp.route('/<int:id_layanan>', methods=['DELETE', 'OPTIONS'], strict_slashes=False)
def delete_service(id_layanan):
    s = Service.query.get_or_404(id_layanan)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Service deleted'}) 