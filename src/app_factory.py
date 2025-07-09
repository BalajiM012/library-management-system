from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'public'))
    app = Flask(__name__, static_folder=static_dir, static_url_path='', template_folder=template_dir)
    app.secret_key = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_db.sqlite3'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'

    @app.route('/test')
    def test():
        return "Test route is working"

    db.init_app(app)
    jwt = JWTManager(app)

    # Import models here to register with SQLAlchemy
    from src.models import User, Book, BorrowRecord, Fees

    # Import and register blueprints
    from src.features.book_recommendation.api import book_recommendation_bp
    from src.features.book_management.api import book_management_bp
    from src.features.student_login.api import student_login_bp
    from src.features.user_login import api_flask as user_login_bp
    from src.features.admin_login import api as admin_login_bp

    from src.features.demand_forecast.api import demand_forecast_bp
    from src.features.due_date_fine_tracking.api import due_date_fine_tracking_bp
    from src.features.automated_fine_calculation.api import automated_fine_calculation_bp
    from src.features.home_ui.api import home_ui_bp
    from src.features.dashboard.api import dashboard_bp
    from src.features.student_portal.api import student_portal_bp
    from src.features.dataset_management.api import dataset_management_bp
    from src.features.history.api import history_bp
    from src.features.manage_users.api import manage_users_bp
    from src.features.student.api import student_bp

    app.register_blueprint(book_recommendation_bp)
    app.register_blueprint(book_management_bp)
    app.register_blueprint(student_login_bp)
    app.register_blueprint(user_login_bp.user_login_bp)
    app.register_blueprint(admin_login_bp.admin_login_bp)
    app.register_blueprint(demand_forecast_bp)
    app.register_blueprint(due_date_fine_tracking_bp)
    app.register_blueprint(automated_fine_calculation_bp)
    app.register_blueprint(home_ui_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_portal_bp)
    app.register_blueprint(dataset_management_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(manage_users_bp)
    app.register_blueprint(student_bp)

    # Initialize and start the scheduler for automated fine calculation
    from src.features.automated_fine_calculation.scheduler import start_scheduler
    start_scheduler(app)

    return app
