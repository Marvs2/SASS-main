# api/api_routes.py
from flask import Blueprint, jsonify, request, redirect, url_for, flash, session
from models import  Admin

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from decorators.auth_decorators import admin_required
admin_api = Blueprint('admin_api', __name__)

# Api/v1/admin/api_routes.py

@admin_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=admin.adm_Id)
            session['access_token'] = access_token
            session['user_role'] = 'admin'
            return redirect(url_for('admin_home'))
        else:
            flash('Invalid email or password', 'danger')
    return redirect(url_for('admin_login'))



#===================================================
# TESTING AREA
@admin_api.route('/profile', methods=['GET'])
@admin_required
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    # Debug print statement
    admin = Admin.query.get(current_user_id)
    if admin:
        return jsonify(admin.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('admin_api.login'))