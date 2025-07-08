from flask import Blueprint, request, jsonify
from models import db, HealthCenter

health_centers_bp = Blueprint('health_centers', __name__, url_prefix=None)

@health_centers_bp.route('/', methods=['GET'], strict_slashes=False)
def get_health_centers():
    health_centers = HealthCenter.query.all()
    return jsonify([{'kode_faskes': h.kode_faskes, 'nama_puskesmas': h.nama_puskesmas, 'alamat': h.alamat, 'jam_operasional': str(h.jam_operasional), 'nomor_kontak': h.nomor_kontak, 'id_dokter': h.id_dokter} for h in health_centers])

@health_centers_bp.route('/<int:kode_faskes>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_health_center(kode_faskes):
    h = HealthCenter.query.get_or_404(kode_faskes)
    return jsonify({'kode_faskes': h.kode_faskes, 'nama_puskesmas': h.nama_puskesmas, 'alamat': h.alamat, 'jam_operasional': str(h.jam_operasional), 'nomor_kontak': h.nomor_kontak, 'id_dokter': h.id_dokter})

@health_centers_bp.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
def create_health_center():
    data = request.json
    h = HealthCenter(
        nama_puskesmas=data['nama_puskesmas'],
        alamat=data['alamat'],
        jam_operasional=data.get('jam_operasional'),
        nomor_kontak=data.get('nomor_kontak'),
        id_dokter=data.get('id_dokter')
    )
    db.session.add(h)
    db.session.commit()
    return jsonify({'kode_faskes': h.kode_faskes}), 201

@health_centers_bp.route('/<int:kode_faskes>', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def update_health_center(kode_faskes):
    h = HealthCenter.query.get_or_404(kode_faskes)
    data = request.json
    h.nama_puskesmas = data.get('nama_puskesmas', h.nama_puskesmas)
    h.alamat = data.get('alamat', h.alamat)
    h.jam_operasional = data.get('jam_operasional', h.jam_operasional)
    h.nomor_kontak = data.get('nomor_kontak', h.nomor_kontak)
    h.id_dokter = data.get('id_dokter', h.id_dokter)
    db.session.commit()
    return jsonify({'kode_faskes': h.kode_faskes})

@health_centers_bp.route('/<int:kode_faskes>', methods=['DELETE', 'OPTIONS'], strict_slashes=False)
def delete_health_center(kode_faskes):
    h = HealthCenter.query.get_or_404(kode_faskes)
    db.session.delete(h)
    db.session.commit()
    return jsonify({'message': 'Health center deleted'})