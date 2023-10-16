# api/api_routes.py
from flask import Blueprint, jsonify, request, redirect, url_for, flash, session
from models import  Faculty

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  login_user
from decorators.auth_decorators import faculty_required

faculty_api = Blueprint('faculty_api', __name__)

# Api/v1/faculty/api_routes.py

@faculty_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print("EMAIL: ", email)
        print("passworD: ", password)


        faculty = Faculty.query.filter_by(email=email).first()
        if faculty and check_password_hash(faculty.password, password):
       
            session['user_id'] = faculty.facultyID
            session['user_role'] = 'faculty'
            return redirect(url_for('faculty_home'))
        else:
            flash('Invalid email or password', 'danger')
    return redirect(url_for('faculty_api.login'))


#===================================================
# TESTING AREA
@faculty_api.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    # Debug print statement
    faculty = Faculty.query.get(current_user_id)
    if faculty:
        return jsonify(faculty.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('faculty_api.login'))