from flask import Flask
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# Import semua blueprint
from api.users.endpoints import users_bp
from api.notifications.endpoints import notifications_bp
from api.reservations.endpoints import reservations_bp
from api.services.endpoints import services_bp
from api.queues.endpoints import queues_bp
from api.health_centers.endpoints import health_centers_bp
from api.doctors.endpoints import doctors_bp
from api.doctor_schedules.endpoints import doctor_schedules_bp
from api.data_protected.endpoints import data_protected_bp

load_dotenv()  # Membaca file .env

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt')
CORS(app)

db.init_app(app)

jwt = JWTManager(app)

# Daftarkan semua blueprint
def register_blueprints(app):
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(notifications_bp, url_prefix='/api/v1/notifications')
    app.register_blueprint(reservations_bp, url_prefix='/api/v1/reservations')
    app.register_blueprint(services_bp, url_prefix='/api/v1/services')
    app.register_blueprint(queues_bp, url_prefix='/api/v1/queues')
    app.register_blueprint(health_centers_bp, url_prefix='/api/v1/health_centers')
    app.register_blueprint(doctors_bp, url_prefix='/api/v1/doctors')
    app.register_blueprint(doctor_schedules_bp, url_prefix='/api/v1/doctor_schedules')
    app.register_blueprint(data_protected_bp, url_prefix='/api/v1/protected')

register_blueprints(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 