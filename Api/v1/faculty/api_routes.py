# api/api_routes.py
import base64
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import Faculty
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  login_user
from decorators.auth_decorators import faculty_required

faculty_api = Blueprint('faculty_api', __name__)

# Api/v1/faculty/api_routes.py

def get_current_faculty_user():
    current_faculty_id = session.get('user_id')
    if current_faculty_id:
        faculty = Faculty.query.get(current_faculty_id)
        if faculty:
            return faculty
        else:
            # Handle case where faculty is not found
            print(f"Faculty with ID {current_faculty_id} not found.")
            return None
    else:
        # Handle case where there is no user_id in session
        print("No user_id found in session.")
        return None



"""faculty_api_url = 'https://pupqcfis-com.onrender.com/api/all/Faculty_Profile'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiIzM2Y0ZWI4NWNjNDQ0MTQzOWFkMzMwYWUzMzJiNmYwYyJ9.5pjwXdaIIZf6Jm9zb26YueCPQhj6Tc18bbZ0vnX4S9M'  # Replace with your actual API key

@faculty_api.route('/login', methods=['POST'])
def faculty_login():
    # Existing code...
    email = request.form['email']
    password = request.form['password']

    # Prepare the data to send to the authentication endpoint
    payload = {
        'email': email,
        'password': password
    }

    response = requests.post(faculty_api_url, json=payload)

    if response.status_code == 200:
        # Assuming the API returns a token upon successful login
        token = response.json().get('token')

        # Store the token in session or use it for further API requests
        session['token'] = token

        # Redirect to faculty dashboard or other route
        return redirect(url_for('faculty_dashboard'))
    else:
        flash('Failed to authenticate', 'danger')

    return redirect(url_for('faculty_portal'))"""


@faculty_api.route('/faculty_login', methods=['POST'])
def faculty_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        faculty = Faculty.query.filter_by(email=email).first()
        if faculty and check_password_hash(faculty.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=faculty.facultyID)
            session['access_token'] = access_token
            session['user_id'] = faculty.facultyID
            session['user_role'] = 'faculty'

            # Check if session is correctly set
            return redirect(url_for('faculty_dashboard'))
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
    
def get_gender_string(gender_code):
    if gender_code == 1:
        return 'Male'
    elif gender_code == 2:
        return 'Female'
    else:
        return 'Undefined'  # Handle any other values

@faculty_api.route('/faculty-details', methods=['GET'])
def fetchFacultyDetails():
    user_id = session.get('user_id')

    # Retrieve the faculty object from the database using the user_id
    faculty = Faculty.query.get(user_id)

    if faculty:
        # Convert userImg to base64 string if it exists
        user_img_base64 = base64.b64encode(faculty.userImg).decode('utf-8') if faculty.userImg else None
        gender_string = get_gender_string(faculty.gender)  # Ensure get_gender_string() is defined

        # Construct and return the JSON response
        return jsonify({
            "facultyNumber": faculty.facultyNumber,
            "name": faculty.name,
            "email": faculty.email,
            "address": faculty.address,
            "gender": gender_string,
            "dateofBirth": faculty.dateofBirth.strftime('%Y-%m-%d') if faculty.dateofBirth else None,
            "placeofBirth": faculty.placeofBirth,
            "mobile_number": faculty.mobile_number,
            "userImg": user_img_base64,
        })
    else:
        # For API, it's better to return a JSON response instead of using flash and redirect
        return jsonify({"error": "User not found"}), 404


def get_gender_string(gender_code):
    # Implement this function based on how you store gender information
    gender_dict = {1: "Male", 2: "Female", 3: "Other"}
    return gender_dict.get(gender_code, "Unknown")