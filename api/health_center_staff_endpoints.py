from flask import Blueprint, request, jsonify
from models import db, HealthCenterStaff, HealthCenter, User

health_center_staff_bp = Blueprint('health_center_staff', __name__, url_prefix='/api/v1/health_center_staff')

@health_center_staff_bp.route('/<int:id_user>', methods=['GET'])
def get_assignments(id_user):
    assignments = HealthCenterStaff.query.filter_by(id_user=id_user).all()
    return jsonify([a.id_puskesmas for a in assignments])

@health_center_staff_bp.route('/', methods=['POST'])
def assign_puskesmas():
    data = request.json
    id_user = data['id_user']
    id_puskesmas_list = data['id_puskesmas']
    # Hapus assignment lama
    HealthCenterStaff.query.filter_by(id_user=id_user).delete()
    # Tambah assignment baru
    for id_puskesmas in id_puskesmas_list:
        db.session.add(HealthCenterStaff(id_user=id_user, id_puskesmas=id_puskesmas))
    db.session.commit()
    return jsonify({'message': 'Assignment updated', 'id_user': id_user, 'id_puskesmas': id_puskesmas_list}) 