from flask import Blueprint, request, jsonify
from models import db, Queue, Reservation, Service, HealthCenter, Doctor

queues_bp = Blueprint('queues', __name__, url_prefix=None)

@queues_bp.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_queues():
    queues = Queue.query.all()
    return jsonify([{'id_antrian': q.id_antrian, 'id_reservasi': q.id_reservasi, 'nomor_antrian': q.nomor_antrian, 'waktu_antrian': str(q.waktu_antrian)} for q in queues])

@queues_bp.route('/<int:id_antrian>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_queue(id_antrian):
    q = Queue.query.get_or_404(id_antrian)
    return jsonify({'id_antrian': q.id_antrian, 'id_reservasi': q.id_reservasi, 'nomor_antrian': q.nomor_antrian, 'waktu_antrian': str(q.waktu_antrian)})

@queues_bp.route('/user/<int:id_user>', methods=['GET'])
def get_queues_by_user(id_user):
    queues = (
        db.session.query(Queue, Reservation, Service, HealthCenter, Doctor)
        .join(Reservation, Queue.id_reservasi == Reservation.id_reservasi)
        .join(Service, Reservation.id_layanan == Service.id_layanan)
        .join(HealthCenter, Reservation.id_puskesmas == HealthCenter.id_puskesmas)
        .join(Doctor, HealthCenter.id_dokter == Doctor.id_dokter)
        .filter(Reservation.id_user == id_user)
        .all()
    )
    result = []
    for q, r, s, p, d in queues:
        result.append({
            'id_antrian': q.id_antrian,
            'id_reservasi': q.id_reservasi,
            'nomor_antrian': q.nomor_antrian,
            'waktu_antrian': str(q.waktu_antrian),
            'status': r.status,
            'tanggal_reservasi': r.tanggal_reservasi.strftime('%Y-%m-%d %H:%M:%S'),
            'nama_layanan': s.nama_layanan,
            'nama_puskesmas': p.nama_puskesmas,
            'nama_dokter': d.nama_dokter
        })
    return jsonify(result)

@queues_bp.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
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

@queues_bp.route('/<int:id_antrian>', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def update_queue(id_antrian):
    q = Queue.query.get_or_404(id_antrian)
    data = request.json
    q.id_reservasi = data.get('id_reservasi', q.id_reservasi)
    # nomor_antrian tidak boleh diubah manual
    q.waktu_antrian = data.get('waktu_antrian', q.waktu_antrian)
    db.session.commit()
    return jsonify({'id_antrian': q.id_antrian})

@queues_bp.route('/<int:id_antrian>', methods=['DELETE', 'OPTIONS'], strict_slashes=False)
def delete_queue(id_antrian):
    q = Queue.query.get_or_404(id_antrian)
    db.session.delete(q)
    db.session.commit()
    return jsonify({'message': 'Queue deleted'})