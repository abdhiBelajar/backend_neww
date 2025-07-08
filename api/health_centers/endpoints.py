from flask import Blueprint, request, jsonify
from models import db, HealthCenter

health_centers_bp = Blueprint('health_centers', __name__, url_prefix=None)

@health_centers_bp.route('/', methods=['GET'], strict_slashes=False)
def get_health_centers():
    health_centers = HealthCenter.query.all()
    return jsonify([
        {
            'id_puskesmas': h.id_puskesmas,
            'kode_faskes': h.kode_faskes,
            'nama_puskesmas': h.nama_puskesmas,
            'alamat': h.alamat,
            'jam_operasional': h.jam_operasional,
            'nomor_kontak': h.nomor_kontak,
            'id_dokter': h.id_dokter
        } for h in health_centers
    ])

@health_centers_bp.route('/<int:id_puskesmas>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_health_center(id_puskesmas):
    h = HealthCenter.query.get_or_404(id_puskesmas)
    return jsonify({
        'id_puskesmas': h.id_puskesmas,
        'kode_faskes': h.kode_faskes,
        'nama_puskesmas': h.nama_puskesmas,
        'alamat': h.alamat,
        'jam_operasional': h.jam_operasional,
        'nomor_kontak': h.nomor_kontak,
        'id_dokter': h.id_dokter
    })

@health_centers_bp.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
def create_health_center():
    data = request.json
    default_jam_operasional = {
        "Senin": {"buka": "08:00", "tutup": "14:00"},
        "Selasa": {"buka": "08:00", "tutup": "14:00"},
        "Rabu": {"buka": "08:00", "tutup": "14:00"},
        "Kamis": {"buka": "08:00", "tutup": "14:00"},
        "Jumat": {"buka": "08:00", "tutup": "11:00"},
        "Sabtu": {"buka": "08:00", "tutup": "12:00"},
        "Minggu": {"tutup": True}
    }
    h = HealthCenter(
        kode_faskes=data['kode_faskes'],
        nama_puskesmas=data['nama_puskesmas'],
        alamat=data['alamat'],
        jam_operasional=data.get('jam_operasional', default_jam_operasional),
        nomor_kontak=data.get('nomor_kontak'),
        id_dokter=data.get('id_dokter')
    )
    db.session.add(h)
    db.session.commit()
    return jsonify({'id_puskesmas': h.id_puskesmas}), 201

@health_centers_bp.route('/<int:id_puskesmas>', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def update_health_center(id_puskesmas):
    h = HealthCenter.query.get_or_404(id_puskesmas)
    data = request.json
    default_jam_operasional = {
        "Senin": {"buka": "08:00", "tutup": "14:00"},
        "Selasa": {"buka": "08:00", "tutup": "14:00"},
        "Rabu": {"buka": "08:00", "tutup": "14:00"},
        "Kamis": {"buka": "08:00", "tutup": "14:00"},
        "Jumat": {"buka": "08:00", "tutup": "11:00"},
        "Sabtu": {"buka": "08:00", "tutup": "12:00"},
        "Minggu": {"tutup": True}
    }
    h.kode_faskes = data.get('kode_faskes', h.kode_faskes)
    h.nama_puskesmas = data.get('nama_puskesmas', h.nama_puskesmas)
    h.alamat = data.get('alamat', h.alamat)
    h.jam_operasional = data.get('jam_operasional', h.jam_operasional or default_jam_operasional)
    h.nomor_kontak = data.get('nomor_kontak', h.nomor_kontak)
    h.id_dokter = data.get('id_dokter', h.id_dokter)
    db.session.commit()
    return jsonify({'id_puskesmas': h.id_puskesmas})

@health_centers_bp.route('/<int:id_puskesmas>', methods=['DELETE', 'OPTIONS'], strict_slashes=False)
def delete_health_center(id_puskesmas):
    h = HealthCenter.query.get_or_404(id_puskesmas)
    db.session.delete(h)
    db.session.commit()
    return jsonify({'message': 'Health center deleted'})