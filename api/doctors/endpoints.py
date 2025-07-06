from flask import Blueprint, request, jsonify
from models import db, Doctor

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{'id_dokter': d.id_dokter, 'nomor_str': d.nomor_str, 'nama_dokter': d.nama_dokter, 'spesialis': d.spesialis} for d in doctors])

@doctors_bp.route('/<int:id_dokter>', methods=['GET'])
def get_doctor(id_dokter):
    d = Doctor.query.get_or_404(id_dokter)
    return jsonify({'id_dokter': d.id_dokter, 'nomor_str': d.nomor_str, 'nama_dokter': d.nama_dokter, 'spesialis': d.spesialis})

@doctors_bp.route('/', methods=['POST'])
def create_doctor():
    data = request.json
    d = Doctor(
        nomor_str=data['nomor_str'],
        nama_dokter=data['nama_dokter'],
        spesialis=data.get('spesialis')
    )
    db.session.add(d)
    db.session.commit()
    return jsonify({'id_dokter': d.id_dokter}), 201

@doctors_bp.route('/<int:id_dokter>', methods=['PUT'])
def update_doctor(id_dokter):
    d = Doctor.query.get_or_404(id_dokter)
    data = request.json
    d.nomor_str = data.get('nomor_str', d.nomor_str)
    d.nama_dokter = data.get('nama_dokter', d.nama_dokter)
    d.spesialis = data.get('spesialis', d.spesialis)
    db.session.commit()
    return jsonify({'id_dokter': d.id_dokter})

@doctors_bp.route('/<int:id_dokter>', methods=['DELETE'])
def delete_doctor(id_dokter):
    d = Doctor.query.get_or_404(id_dokter)
    db.session.delete(d)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted'}) 