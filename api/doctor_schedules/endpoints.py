from flask import Blueprint, request, jsonify
from models import db, DoctorSchedule

doctor_schedules_bp = Blueprint('doctor_schedules', __name__, url_prefix=None)

@doctor_schedules_bp.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_doctor_schedules():
    schedules = DoctorSchedule.query.all()
    return jsonify([{'id_jadwal': s.id_jadwal, 'nomor_str': s.nomor_str, 'hari': s.hari, 'jam_mulai': str(s.jam_mulai), 'jam_selesai': str(s.jam_selesai)} for s in schedules])

@doctor_schedules_bp.route('/<int:id_jadwal>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_doctor_schedule(id_jadwal):
    s = DoctorSchedule.query.get_or_404(id_jadwal)
    return jsonify({'id_jadwal': s.id_jadwal, 'nomor_str': s.nomor_str, 'hari': s.hari, 'jam_mulai': str(s.jam_mulai), 'jam_selesai': str(s.jam_selesai)})

@doctor_schedules_bp.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
def create_doctor_schedule():
    data = request.json
    s = DoctorSchedule(
        nomor_str=data['nomor_str'],
        hari=data['hari'],
        jam_mulai=data['jam_mulai'],
        jam_selesai=data['jam_selesai']
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'id_jadwal': s.id_jadwal}), 201

@doctor_schedules_bp.route('/<int:id_jadwal>', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def update_doctor_schedule(id_jadwal):
    s = DoctorSchedule.query.get_or_404(id_jadwal)
    data = request.json
    s.nomor_str = data.get('nomor_str', s.nomor_str)
    s.hari = data.get('hari', s.hari)
    s.jam_mulai = data.get('jam_mulai', s.jam_mulai)
    s.jam_selesai = data.get('jam_selesai', s.jam_selesai)
    db.session.commit()
    return jsonify({'id_jadwal': s.id_jadwal})

@doctor_schedules_bp.route('/<int:id_jadwal>', methods=['DELETE', 'OPTIONS'], strict_slashes=False)
def delete_doctor_schedule(id_jadwal):
    s = DoctorSchedule.query.get_or_404(id_jadwal)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Doctor schedule deleted'}) 