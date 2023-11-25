# api/api_routes.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import  Faculty

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  login_user
from decorators.auth_decorators import faculty_required

faculty_api = Blueprint('faculty_api', __name__)

# Api/v1/faculty/api_routes.py

@faculty_api.route('/login', methods=['POST'])
def faculty_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        faculty = Faculty.query.filter_by(email=email).first()
        if faculty and check_password_hash(faculty.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=faculty.facultyID)
            session['access_token'] = access_token
            session['user_role'] = 'faculty'

            # Store additional faculty details in the session
            session['user_id'] = faculty.facultyID
            session['faculty_Number'] = faculty.faculty_Number
            session['name'] = faculty.name
            session['email'] = faculty.email
            session['address'] = faculty.address
            session['gender'] = faculty.gender
            session['dateofBirth'] = faculty.dateofBirth
            session['placeofBirth'] = faculty.placeofBirth
            session['mobile_number'] = faculty.mobile_number
            session['userImg'] = faculty.userImg

            return render_template('faculty/home.html', faculty_details=session)

        else:
            flash('Invalid email or password', 'danger')

    return redirect(url_for('faculty_portal'))

#===============================================================================================================#
#==================================================FACULTY======================================================#
#===============================================================================================================#


# TESTING AREA
@faculty_api.route('/profile', methods=['GET'])
@jwt_required()
def faculty_profile():
    current_user_id = get_jwt_identity()
    # Debug print statement
    faculty = Faculty.query.get(current_user_id)
    if faculty:
        return jsonify(faculty.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('faculty_api.faculty_login'))
    
