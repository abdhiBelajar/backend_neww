from flask import Blueprint, request, jsonify
from models import db, Reservation, Queue

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([{'id_reservasi': r.id_reservasi, 'id_user': r.id_user, 'id_puskesmas': r.id_puskesmas, 'id_layanan': r.id_layanan, 'id_antrian': r.id_antrian, 'tanggal_reservasi': r.tanggal_reservasi, 'status': r.status} for r in reservations])

@reservations_bp.route('/<int:id_reservasi>', methods=['GET'])
def get_reservation(id_reservasi):
    r = Reservation.query.get_or_404(id_reservasi)
    return jsonify({'id_reservasi': r.id_reservasi, 'id_user': r.id_user, 'id_puskesmas': r.id_puskesmas, 'id_layanan': r.id_layanan, 'id_antrian': r.id_antrian, 'tanggal_reservasi': r.tanggal_reservasi, 'status': r.status})

@reservations_bp.route('/', methods=['POST'])
def create_reservation():
    data = request.json
    id_user = data['id_user']
    id_puskesmas = data['id_puskesmas']
    id_layanan = data['id_layanan']
    tanggal_reservasi = data['tanggal_reservasi']
    status = data['status']

    # Buat reservasi tanpa id_antrian dulu
    r = Reservation(
        id_user=id_user,
        id_puskesmas=id_puskesmas,
        id_layanan=id_layanan,
        tanggal_reservasi=tanggal_reservasi,
        status=status
    )
    db.session.add(r)
    db.session.commit()

    # Hitung nomor antrian otomatis
    from datetime import datetime
    tanggal_obj = datetime.fromisoformat(tanggal_reservasi)
    jumlah_antrian = db.session.query(Queue).join(Reservation).filter(
        Reservation.id_puskesmas == id_puskesmas,
        Reservation.id_layanan == id_layanan,
        db.func.date(Reservation.tanggal_reservasi) == tanggal_obj.date()
    ).count()
    nomor_antrian = jumlah_antrian + 1

    # Buat queue baru
    q = Queue(
        id_reservasi=r.id_reservasi,
        nomor_antrian=nomor_antrian,
        waktu_antrian=tanggal_obj.time()
    )
    db.session.add(q)
    db.session.commit()

    # Update kolom id_antrian di reservations
    r.id_antrian = q.id_antrian
    db.session.commit()

    return jsonify({'id_reservasi': r.id_reservasi, 'id_antrian': q.id_antrian, 'nomor_antrian': q.nomor_antrian}), 201

@reservations_bp.route('/<int:id_reservasi>', methods=['PUT'])
def update_reservation(id_reservasi):
    r = Reservation.query.get_or_404(id_reservasi)
    data = request.json
    r.id_user = data.get('id_user', r.id_user)
    r.id_puskesmas = data.get('id_puskesmas', r.id_puskesmas)
    r.id_layanan = data.get('id_layanan', r.id_layanan)
    r.id_antrian = data.get('id_antrian', r.id_antrian)
    r.tanggal_reservasi = data.get('tanggal_reservasi', r.tanggal_reservasi)
    r.status = data.get('status', r.status)
    db.session.commit()
    return jsonify({'id_reservasi': r.id_reservasi})

@reservations_bp.route('/<int:id_reservasi>', methods=['DELETE'])
def delete_reservation(id_reservasi):
    r = Reservation.query.get_or_404(id_reservasi)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Reservation deleted'}) 