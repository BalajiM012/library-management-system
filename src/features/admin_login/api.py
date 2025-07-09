from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from src.app_factory import db
from src.models import User

from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from src.app_factory import db
from src.models import User

admin_login_bp = Blueprint('admin_login', __name__, url_prefix='/admin')

@admin_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Authentication disabled - redirect directly to admin dashboard
    return redirect(url_for('home_ui.admin'))

@admin_login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_login.login'))
