from flask import Blueprint, request, jsonify
from models import db, Queue, Reservation
from datetime import datetime

queues_bp = Blueprint('queues', __name__)

@queues_bp.route('/', methods=['GET'])
def get_queues():
    queues = Queue.query.all()
    return jsonify([{'id_antrian': q.id_antrian, 'id_reservasi': q.id_reservasi, 'nomor_antrian': q.nomor_antrian, 'waktu_antrian': str(q.waktu_antrian)} for q in queues])

@queues_bp.route('/<int:id_antrian>', methods=['GET'])
def get_queue(id_antrian):
    q = Queue.query.get_or_404(id_antrian)
    return jsonify({'id_antrian': q.id_antrian, 'id_reservasi': q.id_reservasi, 'nomor_antrian': q.nomor_antrian, 'waktu_antrian': str(q.waktu_antrian)})

@queues_bp.route('/', methods=['POST'])
def create_queue():
    data = request.json
    id_reservasi = data['id_reservasi']
    waktu_antrian = data['waktu_antrian']

    # Ambil data reservasi terkait
    reservasi = Reservation.query.get(id_reservasi)
    if not reservasi:
        return jsonify({'error': 'Reservasi tidak ditemukan'}), 400

    nomor_antrian = reservasi.id_antrian

    q = Queue(
        id_reservasi=id_reservasi,
        nomor_antrian=nomor_antrian,
        waktu_antrian=waktu_antrian
    )
    db.session.add(q)
    db.session.commit()

    # Setelah queue dibuat, update reservation dengan id_antrian queue jika perlu (opsional, bisa dihapus jika tidak perlu)
    # reservasi.id_antrian = q.id_antrian
    # db.session.commit()

    return jsonify({
        'id_antrian': q.id_antrian,
        'nomor_antrian': q.nomor_antrian,
        'id_reservasi': reservasi.id_reservasi
    }), 201

@queues_bp.route('/<int:id_antrian>', methods=['PUT'])
def update_queue(id_antrian):
    q = Queue.query.get_or_404(id_antrian)
    data = request.json
    q.id_reservasi = data.get('id_reservasi', q.id_reservasi)
    # nomor_antrian tidak boleh diubah manual
    q.waktu_antrian = data.get('waktu_antrian', q.waktu_antrian)
    db.session.commit()
    return jsonify({'id_antrian': q.id_antrian})

@queues_bp.route('/<int:id_antrian>', methods=['DELETE'])
def delete_queue(id_antrian):
    q = Queue.query.get_or_404(id_antrian)
    db.session.delete(q)
    db.session.commit()
    return jsonify({'message': 'Queue deleted'}) 