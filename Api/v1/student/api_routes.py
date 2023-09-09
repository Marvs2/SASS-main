# api/api_routes.py
from flask import Blueprint, jsonify, request, redirect, url_for, flash, session
from models import  Student

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  login_user
from flask_cors import CORS 

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

student_api = Blueprint('student_api', __name__)
CORS(student_api)  # Apply CORS to the student_api blueprint

# Api/v1/student/api_routes.py

@student_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        studentsNumber = request.form['studentsNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentsNumber=studentsNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.id)
            session['access_token'] = access_token
            session['user_role'] = 'student'
            return redirect(url_for('student_home'))
        else:
            flash('Invalid email or password', 'danger')
    return redirect(url_for('student_portal'))



#===================================================
# TESTING AREA
@student_api.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    print("CURRENT USER ID: ", current_user_id)
    # Debug print statement
    student = Student.query.get(current_user_id)
    if student:
        return jsonify(student.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('student_api.login'))
    
    
@student_api.route('/all/student', methods=['GET'])
def allstudent():
    api_key = request.headers.get('X-Api-Key')  # Get the API key from the request header

    if api_key in API_KEYS.values():
        return jsonify(message="You got API data")
    else:
        return jsonify(message="Invalid key you cant have an access")


# ...

#@student_api.route('/update/<int:student_id>', methods=['POST','PUT', 'DELETE'])
#@jwt_required()
#def update_student(student_id):
#    current_user_id = get_jwt_identity()
#    student = Student.query.get(student_id)

#    if not student:
#        return jsonify(message="Student not found"), 404

#    if student.id != current_user_id:
#        return jsonify(message="Unauthorized"), 401

#    if request.method == 'POST':
        # Update student information based on the form data
#        student.name = request.form.get('name', student.name)
#        student.email = request.form.get('email', student.email)
#        student.address = request.form.get('address', student.address)
#        student.dateofBirth = request.form.get('dateofBirth', student.dateofBirth)
#        student.placeofBirth = request.form.get('placeofBirth', student.placeofBirth)
#        student.mobileNumber = request.form.get('mobileNumber', student.mobileNumber)
#        student.userImg = request.form.get('userImg', student.userImg)
#        db.session.commit()
#        return jsonify(message="Student information updated successfully")
