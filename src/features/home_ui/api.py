
from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory
import os

home_ui_bp = Blueprint('home_ui', __name__)

@home_ui_bp.route('/')
def home():
    from flask import render_template
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('home_ui.admin'))
        else:
            return redirect(url_for('student_portal.student_portal'))
    return render_template('home.html')

@home_ui_bp.route('/admin')
def admin():
    from flask import render_template, session, redirect, url_for
    # Authentication disabled for admin page
    user = {'fullname': 'Admin'}
    return render_template('admin.html', user=user)

@home_ui_bp.route('/dataset_management')
def dataset_management():
    from flask import render_template
    return render_template('dataset_management.html')

@home_ui_bp.route('/student_portal')
def student_portal():
    from flask import render_template
    return render_template('student_portal.html')

@home_ui_bp.route('/history')
def history():
    from flask import render_template
    return render_template('history.html')
