from flask import Blueprint, request, jsonify
from models import db, Reservation, Queue, HealthCenterStaff, HealthCenter, User

reservations_bp = Blueprint('reservations', __name__, url_prefix=None)

@reservations_bp.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([{'id_reservasi': r.id_reservasi, 'id_user': r.id_user, 'id_puskesmas': r.id_puskesmas, 'id_layanan': r.id_layanan, 'id_antrian': r.id_antrian, 'tanggal_reservasi': r.tanggal_reservasi, 'status': r.status} for r in reservations])

@reservations_bp.route('/<int:id_reservasi>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_reservation(id_reservasi):
    r = Reservation.query.get_or_404(id_reservasi)
    return jsonify({'id_reservasi': r.id_reservasi, 'id_user': r.id_user, 'id_puskesmas': r.id_puskesmas, 'id_layanan': r.id_layanan, 'id_antrian': r.id_antrian, 'tanggal_reservasi': r.tanggal_reservasi, 'status': r.status})

@reservations_bp.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
def create_reservation():
    data = request.json
    required_fields = ['id_user', 'id_puskesmas', 'id_layanan', 'tanggal_reservasi', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} wajib diisi'}), 400

    id_user = data['id_user']
    id_puskesmas = data['id_puskesmas']
    id_layanan = data['id_layanan']
    tanggal_reservasi = data['tanggal_reservasi']
    status = data['status']

    # Validasi id_puskesmas harus ada di tabel health_centers
    if not HealthCenter.query.get(id_puskesmas):
        return jsonify({'error': 'id_puskesmas tidak ditemukan'}), 400

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
    jumlah_antrian = db.session.query(Queue).join(
        Reservation, Queue.id_reservasi == Reservation.id_reservasi
    ).filter(
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

    return jsonify({
        'message': 'Reservasi berhasil',
        'nomor_antrian': q.nomor_antrian,
        'id_antrian': q.id_antrian,
        'id_reservasi': r.id_reservasi
    }), 201

@reservations_bp.route('/<int:id_reservasi>', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def update_reservation(id_reservasi):
    r = Reservation.query.get_or_404(id_reservasi)
    data = request.json
    # Jika status ingin diubah ke cancelled atau confirmed, update status saja
    if data.get('status') in ['cancelled', 'confirmed']:
        r.status = data['status']
        db.session.commit()
        return jsonify({'id_reservasi': r.id_reservasi, 'status': r.status})
    # Hanya izinkan update tanggal_reservasi (reschedule)
    if 'tanggal_reservasi' not in data:
        return jsonify({'error': 'tanggal_reservasi wajib diisi untuk reschedule'}), 400
    old_tanggal = r.tanggal_reservasi
    from datetime import datetime
    try:
        tanggal_obj = datetime.fromisoformat(data['tanggal_reservasi'])
    except Exception as e:
        return jsonify({'error': f'Format tanggal_reservasi tidak valid: {str(e)}'}), 400
    r.tanggal_reservasi = tanggal_obj
    db.session.commit()

    # Update waktu_antrian di Queue jika ada
    if r.id_antrian:
        q = Queue.query.get(r.id_antrian)
        if q:
            q.waktu_antrian = tanggal_obj.time()
            db.session.commit()

    return jsonify({'id_reservasi': r.id_reservasi, 'old_tanggal_reservasi': str(old_tanggal), 'new_tanggal_reservasi': str(r.tanggal_reservasi)})

@reservations_bp.route('/<int:id_reservasi>', methods=['DELETE', 'OPTIONS'], strict_slashes=False)
def delete_reservation(id_reservasi):
    r = Reservation.query.get_or_404(id_reservasi)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Reservation deleted'})

@reservations_bp.route('/staff/<int:id_user>', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_reservations_for_staff(id_user):
    # Ambil semua id_puskesmas yang di-assign ke staff ini
    assigned_puskesmas = db.session.query(HealthCenterStaff.id_puskesmas).filter_by(id_user=id_user).all()
    puskesmas_ids = [p[0] for p in assigned_puskesmas]
    # Ambil semua reservasi untuk puskesmas-puskesmas tersebut
    reservations = Reservation.query.filter(Reservation.id_puskesmas.in_(puskesmas_ids)).all()
    result = []
    for r in reservations:
        # Ambil nama layanan dari relasi service
        nama_layanan = r.service.nama_layanan if r.service else None
        # Ambil nomor antrian dari relasi queue
        nomor_antrian = r.queue.nomor_antrian if r.queue else None
        result.append({
            'id_reservasi': r.id_reservasi,
            'id_user': r.id_user,
            'id_puskesmas': r.id_puskesmas,
            'tanggal_reservasi': r.tanggal_reservasi.strftime('%Y-%m-%d %H:%M:%S'),
            'status': r.status,
            'layanan': nama_layanan,
            'nomor_antrian': nomor_antrian
        })
    return jsonify(result)