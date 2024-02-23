# api/api_routes.py
import base64
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from Api.v1.faculty.utils import get_all_services, get_all_services_counts
from models import Faculty
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  current_user, login_user
from decorators.auth_decorators import faculty_required, role_required

faculty_api = Blueprint('faculty_api', __name__)

# Api/v1/faculty/api_routes.py

def get_current_faculty_user():
    # Retrieve faculty ID from the session
    current_faculty_id = session.get('user_id')

    if current_faculty_id:
        # Try to get the faculty using the retrieved ID
        faculty = Faculty.query.get(current_faculty_id)

        if faculty:
            return faculty
        else:
            # Handle the case where faculty is not found more gracefully
            print(f"Faculty with ID {current_faculty_id} not found.")
            return None
    else:
        # Handle the case where there is no user_id in session
        print("No user_id found in session.")
        return None

# get the Current userID
def get_current_faculty_id():
    if current_user.is_authenticated:
        return current_user.FacultyId
    else:
        # Handle the case where the user is not authenticated or doesn't have a FacultyId
        return None

"""faculty_api_url = 'https://pupqcfis-com.onrender.com/api/all/Faculty_Profile'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiIzM2Y0ZWI4NWNjNDQ0MTQzOWFkMzMwYWUzMzJiNmYwYyJ9.5pjwXdaIIZf6Jm9zb26YueCPQhj6Tc18bbZ0vnX4S9M'  # Replace with your actual API key

@faculty_api.route('/login', methods=['POST'])
def faculty_login():
    # Existing code...
    Email = request.form['Email']
    Password = request.form['Password']

    # Prepare the data to send to the authentication endpoint
    payload = {
        'Email': Email,
        'Password': Password
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
        Email = request.form['Email']
        Password = request.form['Password']

        faculty = Faculty.query.filter_by(Email=Email).first()
        if faculty and check_password_hash(faculty.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=faculty.FacultyId)
            session['access_token'] = access_token
            session['user_id'] = faculty.FacultyId
            session['user_role'] = 'faculty'

            # Check if session is correctly set
            return redirect(url_for('faculty_dashboard'))
        else:
            flash('Invalid Email or Password', 'danger')

    return redirect(url_for('faculty_portal'))


#===============================================================================================================#
#==================================================FACULTY======================================================#
#===============================================================================================================#


# TESTING AREA
@faculty_api.route('/profile', methods=['GET'])
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
@role_required('faculty')
def fetchFacultyDetails():
    user_id = session.get('user_id')

    faculty = Faculty.query.get(user_id)

    if faculty:
        # # Convert userImg to base64 string if it exists
        # user_img_base64 = base64.b64encode(faculty.ProfilePic).decode('utf-8') if faculty.ProfilePic else None
        gender_string = get_gender_string(faculty.Gender)  # Ensure get_gender_string() is defined

        # Construct and return the JSON response
        return jsonify({
            'FacultyType': faculty.FacultyType,
            'FirstName': faculty.FirstName,
            'LastName': faculty.LastName,
            'MiddleName': faculty.MiddleName,
            'Email': faculty.Email,
            'ResidentialAddress': faculty.ResidentialAddress,
            'Gender': gender_string,
            'BirthDate': faculty.BirthDate.strftime('%Y-%m-%d') if faculty.BirthDate else None,
            'MobileNumber': faculty.MobileNumber,
            # 'ProfilePic': user_img_base64,
        })
    else:
        flash('User not found', 'danger')
        return redirect(url_for('faculty_api.faculty_login'))


def get_gender_string(gender_code):
    # Implement this function based on how you store gender information
    gender_dict = {1: "Male", 2: "Female", 3: "Other"}
    return gender_dict.get(gender_code, "Unknown")


@faculty_api.route('/update-faculty-details', methods=['POST'])
def updatefetchFacultyDetails():
    user_id = session.get('user_id')

    faculty = Faculty.query.get(user_id)

    if faculty:
        flash('User not found', 'danger')
        return jsonify({'Message': 'User not found'}), 404

        # user_img_base64 = base64.b64encode(faculty.ProfilePic).decode('utf-8') if faculty.ProfilePic else None
        gender_string = get_gender_string(faculty.Gender)  # Ensure get_gender_string() is defined
    if request.is_json:
        faculty.Email = request.json.get('Email', faculty.Email)
        faculty.MobileNumber = request.json.get('MobileNumber', faculty.MobileNumber)
        faculty.address = request.json.get('address', faculty.address)
    else:
        # Update from form data
        faculty.Email = request.form.get('Email', faculty.Email)
        faculty.MobileNumber = request.form.get('MobileNumber', faculty.MobileNumber)
        faculty.address = request.form.get('address', faculty.address)
    
    # Check if Email and MobileNumber are not None or empty
    if faculty.Email is not None and faculty.MobileNumber is not None:
        # db.session.commit()
        return jsonify({'Message': 'Faculty details updated successfully'})
    else:
        flash('Email and MobileNumber cannot be empty', 'danger')
        return jsonify({'Message': 'Email and MobileNumber cannot be empty'}), 400


#=====================================API====================================#

@faculty_api.route('/student_services', methods=['GET'])
def all_student_services():
    # Assuming you have access to the faculty ID (you may need to retrieve it based on your authentication mechanism)
    services_data = get_all_services()

    if services_data[0]:  # Check if the first element of the tuple (all_services_list) has data
        return jsonify(success=True, message="All faculty services data retrieved successfully.", data=services_data)
    else:
        return jsonify(success=False, message="No data available or data is invalid.")
    

@faculty_api.route('/requestall', methods=['GET'])
def all_services():
    # Assuming you have access to the faculty ID (you may need to retrieve it based on your authentication mechanism)
    status_counts_list = get_all_services_counts()

    return jsonify(success=True, message="All faculty services data retrieved successfully.", data=status_counts_list)
