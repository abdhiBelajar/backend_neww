from datetime import datetime, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, Text, DECIMAL
from sqlalchemy.orm import relationship

# Inisialisasi SQLAlchemy (nanti di app.py, db harus diinisialisasi)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tipe_user = db.Column(db.Enum('admin', 'staff', 'patien'), nullable=True)
    notifications = relationship('Notification', backref='user', lazy=True)
    reservations = relationship('Reservation', backref='user', lazy=True)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id_notifikasi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.BigInteger, db.ForeignKey('users.id_user'), nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    tanggal_notifikasi = db.Column(db.TIMESTAMP, nullable=True)

class Service(db.Model):
    __tablename__ = 'services'
    id_layanan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_layanan = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    tarif = db.Column(db.Numeric(10,2), nullable=True)
    reservations = relationship('Reservation', backref='service', lazy=True)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id_reservasi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.BigInteger, db.ForeignKey('users.id_user'), nullable=False)
    id_puskesmas = db.Column(db.Integer, db.ForeignKey('health_centers.kode_faskes'), nullable=False)
    id_layanan = db.Column(db.Integer, db.ForeignKey('services.id_layanan'), nullable=False)
    id_antrian = db.Column(db.Integer, db.ForeignKey('queues.id_antrian'), nullable=True)
    tanggal_reservasi = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'cancelled'), nullable=False)
    queue = db.relationship('Queue', uselist=False, foreign_keys=[id_antrian])

class Queue(db.Model):
    __tablename__ = 'queues'
    id_antrian = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_reservasi = db.Column(db.Integer, db.ForeignKey('reservations.id_reservasi'), nullable=False)
    nomor_antrian = db.Column(db.Integer, nullable=False)
    waktu_antrian = db.Column(db.Time, nullable=False)
    reservation = db.relationship('Reservation', backref='queues', foreign_keys=[id_reservasi])

class HealthCenter(db.Model):
    __tablename__ = 'health_centers'
    id_puskesmas = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kode_faskes = db.Column(db.Integer, nullable=False)
    nama_puskesmas = db.Column(db.String(255), nullable=False)
    alamat = db.Column(db.String(255), nullable=False)
    jam_operasional = db.Column(db.JSON, nullable=True)
    nomor_kontak = db.Column(db.Text, nullable=True)
    id_dokter = db.Column(db.Integer, db.ForeignKey('doctors.id_dokter'), nullable=True)
    reservations = relationship('Reservation', backref='health_center', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id_dokter = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomor_str = db.Column(db.String(255), unique=True, nullable=False)
    nama_dokter = db.Column(db.String(255), nullable=False)
    spesialis = db.Column(db.String(255), nullable=True)
    schedules = relationship('DoctorSchedule', backref='doctor', lazy=True)
    health_centers = relationship('HealthCenter', backref='doctor', lazy=True)

class DoctorSchedule(db.Model):
    __tablename__ = 'doctor_schedules'
    id_jadwal = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomor_str = db.Column(db.String(255), db.ForeignKey('doctors.nomor_str'), nullable=False)
    hari = db.Column(db.Enum('Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'), nullable=False)
    jam_mulai = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)

class HealthCenterStaff(db.Model):
    __tablename__ = 'health_center_staff'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_puskesmas = db.Column(db.Integer, db.ForeignKey('health_centers.id_puskesmas'), nullable=False)
    id_user = db.Column(db.BigInteger, db.ForeignKey('users.id_user'), nullable=False) 