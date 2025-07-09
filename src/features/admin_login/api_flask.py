from flask import Blueprint, render_template, redirect, url_for, session

admin_login_bp = Blueprint('admin_login', __name__, template_folder='templates')

@admin_login_bp.route('/admin')
def admin():
    # Check if admin is logged in (simple example)
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login.login'))
    user = {'fullname': 'Admin User'}  # Example user info
    return render_template('admin.html', user=user)

@admin_login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_login.login'))

@admin_login_bp.route('/login')
def login():
    # Placeholder login page or redirect
    return "Admin Login Page - Implement login form here"
