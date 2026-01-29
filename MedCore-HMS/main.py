from flask import Flask, redirect, url_for
from config import Config
from models import db, login_manager, migrate
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import models to ensure they're registered with SQLAlchemy
    with app.app_context():
        from models import user, patient, department, room, treatment, medication, vital_sign, activity_log
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.patients import patients_bp
    from routes.medical_records import medical_records_bp
    from routes.hospital import hospital_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(medical_records_bp)
    app.register_blueprint(hospital_bp)
    
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
