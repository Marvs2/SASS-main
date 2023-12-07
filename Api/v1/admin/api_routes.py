# api/api_routes.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from Api.v1.student.api_routes import API_KEYS
from models import Admin, Student

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from decorators.auth_decorators import admin_required

import os

# Access API keys from environment variables
WEBSITE1_API_KEY = os.getenv('WEBSITE1_API_KEY')
WEBSITE2_API_KEY = os.getenv('WEBSITE2_API_KEY')
WEBSITE3_API_KEY = os.getenv('WEBSITE3_API_KEY')
WEBSITE4_API_KEY = os.getenv('WEBSITE4_API_KEY')
WEBSITE5_API_KEY = os.getenv('WEBSITE5_API_KEY')

API_KEYS = {
    'website1': WEBSITE1_API_KEY,   
    'website2': WEBSITE2_API_KEY,
    'website3': WEBSITE3_API_KEY,
    'website4': WEBSITE4_API_KEY,
    'website5': WEBSITE5_API_KEY,
    # Add more websites and keys as needed
}
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
            
            #Store additional admin details in the session
            session['adm_Id'] = admin.adm_Id
            session['admin_Number'] = admin.admin_Number
            session['name'] = admin.name
            session['email'] = admin.email
            session['gender'] = admin.gender
            session['dateofBirth'] = admin.dateofBirth
            session['placeofBirth'] = admin.placeofBirth
            session['mobile_number'] = admin.mobile_number

            return render_template('admin/dashboard.html', admin_details=session)
        else:
            flash('Invalid email or password', 'danger')

    return redirect(url_for('admin_portal'))



#===================================================
# TESTING AREA
@admin_api.route('/profile', methods=['GET'])
@jwt_required()
def admin_profile():
    current_user_id = get_jwt_identity()
    # Debug print statement
    admin = Admin.query.get(current_user_id)
    if admin:
        return jsonify(admin.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('admin_api.login'))
    
"""# Route to fetch the list of students as JSON
@admin_api.route('/student_list', methods=['GET'])
def get_student_list():
    api_key = request.headers.get('X-Api-Key')  # Get the API key from the request header

    if api_key in API_KEYS.values():
        # Fetch all students from the database
        students = Student.query.all()

        # Convert the list of students to a JSON-friendly format
        students_data = [
            {
                'student_id': student.student_id,
                'studentNumber': student.studentNumber,
                'name': student.name,
                'email': student.email,
                'address': student.address,
                'gender': student.gender,
                'dateofBirth': student.dateofBirth,
                'placeofBirth': student.placeofBirth,
                'mobileNumber': student.mobileNumber,
                'userImg': student.userImg
            }
            for student in students
        ]

        # Return the list of students as JSON
        return jsonify(message="You got API data", students=students_data)
    else:
        return jsonify(message="Invalid key you can't have access")
"""
