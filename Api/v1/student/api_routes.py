# api/api_routes.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import CertificationRequest, CrossEnrollment, ManualEnrollment, PetitionRequest, Student
from werkzeug.utils import secure_filename
from datetime import datetime
#from models import Services
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  login_user
from flask_cors import CORS 
from decorators.auth_decorators import student_required, faculty_required, prevent_authenticated, admin_required, role_required

import os

student_api_base_url = os.getenv("STUDENT_API_BASE_URL")

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

#===============================================================

"""# Function to authenticate the user (usually happens during login)
def authenticate_user(username, password):
    # Your authentication logic goes here
    # Check if the provided username and password match a user in your database
    # If authenticated, retrieve the user ID and set it in the session
    user = User.query.filter_by(username=username).first()  # Replace User with your actual model
    if user and user.check_password(password):  # Replace check_password with your validation logic
        session['user_id'] = user.id  # Assuming user.id is the ID of the authenticated user
        return True
    return False"""

# Api/v1/student/api_routes.py
#================================================================
# Function to check if the user is logged in
def is_user_logged_in_overload():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

def store_user_details_in_session(student):
    # Store user details in the session
    session['user_id'] = student.student_id
    session['studentNumber'] = student.studentNumber
    session['name'] = student.name
    session['gender'] = student.gender
    session['email'] = student.email
    session['address'] = student.address
    session['dateofBirth'] = student.dateofBirth
    session['placeofBirth'] = student.placeofBirth
    session['mobileNumber'] = student.mobileNumber
    session['userImg'] = student.userImg

# Login function for students to go to student_overload
@student_api.route('/login-Overload', methods=['POST'])
def login_Overload():
    # ... (other code)
    if is_user_logged_in_overload():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_overload'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']

        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Use the function to store user details in the session
            store_user_details_in_session(student)

            return redirect(url_for('student_portal_overload'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('student/login.html')

#========================================================

def is_user_logged_in_certification():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

# Login function for students to goto certification
@student_api.route('/login-Certification', methods=['GET', 'POST'])
def login_Certification():
    if is_user_logged_in_certification():
        # If the user is already logged in, redirect to the certifications page
        return redirect(url_for('student_portal_certification'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_certification', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
def is_user_logged_in_changesubsched():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

# Login function for students to goto changesubsched
@student_api.route('/login-Changesubsched', methods=['GET', 'POST'])
def login_Changesubsched():
    if is_user_logged_in_changesubsched():
        # If the user is already logged in, redirect to the changesubsched page
        return redirect(url_for('student_portal_changesubsched'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_changesubsched', student_detailss=session))

        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in
def is_user_logged_in_enrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Enrollment', methods=['GET', 'POST'])
def login_Enrollment():
    if is_user_logged_in_enrollment():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_enrollment'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_enrollment', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in addingofsubject
def is_user_logged_in_addingofsubject():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-AddingofSubjects', methods=['GET', 'POST'])
def login_Addingofsubject():
    if is_user_logged_in_addingofsubject():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_addingsubject'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_addingsubject', student_details=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in tutorial of subjects
def is_user_logged_in_tutorial():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Tutorial', methods=['GET', 'POST'])
def login_Tutorial():
    if is_user_logged_in_tutorial():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_tutorial'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_tutorial', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in shifting
def is_user_logged_in_shifting():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Shifting', methods=['GET', 'POST'])
def login_Shifting():
    if is_user_logged_in_shifting():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_shifting'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_shifting', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in shifting
def is_user_logged_in_petition():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Petition', methods=['GET', 'POST'])
def login_Petition():
    if is_user_logged_in_petition():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_petition'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_petition', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in gradeentry
def is_user_logged_in_gradeentry():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Gradeentry', methods=['GET', 'POST'])
def login_Gradeentry():
    if is_user_logged_in_gradeentry():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_gradeentry'))
    
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_gradeentry', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================

# Function to check if the user is logged in shifting
def is_user_logged_in_crossenrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Crossenrollment', methods=['GET', 'POST'])
def login_Crossenrollment():
    if is_user_logged_in_crossenrollment():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_crossenrollment'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_crossenrollment', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

"""# Main login function
@student_api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']

        student = Student.query.filter_by(studentNumber=studentNumber).first()

        if student:
            # Debugging print
            print(f"Stored Password Hash: {student.password}")
            print(f"Provided Password: {password}")

            if check_password_hash(student.password, password):
                # Successfully authenticated
                print("Authentication Successful!")

                access_token = create_access_token(identity=student.student_id)
                session['access_token'] = access_token
                session['user_role'] = 'student'

                # Store additional student details in the session
                session['user_id'] = student.student_id
                session['studentNumber'] = student.studentNumber
                session['name'] = student.name
                # ... (other details)

                return render_template('student/home.html', student_details=session)

            else:
                print("Invalid password")
                flash('Invalid student number or password', 'danger')

        else:
            print("Student not found")
            flash('Invalid student number or password', 'danger')

    return redirect(url_for('student_portal'))"""


#====================================================================#
#================The real login in the true manners==================#
#====================================================================#
#for All Students
@student_api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']

        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_id'] = student.student_id
            session['user_role'] = 'student'

            return render_template('student/dashboard.html', student_details=session)

        else:
            flash('Invalid email or password', 'danger')

    return redirect(url_for('studentLogin'))


#=====================================================================#
# @app.route('/student/profile')
# @role_required('student')
# def studentprofile():
#     # Retrieve student details from the database based on the user_id stored in the session
#     student_id = session.get('user_id')
#     student = Student.query.get(student_id)

#     # Check if the student is found in the database
#     if student:
#         student_details = {
#             'studentNumber': student.studentNumber,
#             'name': student.name,
#             'gender': student.gender,
#             'email': student.email,
#             'address': student.address,
#             'dateofBirth': student.dateofBirth,
#             'placeofBirth': student.placeofBirth,
#             'mobileNumber': student.mobileNumber,
#             'userImg': student.userImg,
#         }

#         if student_details['gender'] == 1:
#             student_details['gender'] = 'Male'
#         elif student_details['gender'] == 2:
#             student_details['gender'] = 'Female'
#         else:
#             student_details['gender'] = 'Undefined'  # Handle any other values

#         return render_template('student/profile.html', student_details=student_details)
#     else:
#         flash('Student not found', 'danger')
#         return redirect(url_for('studentLogin'))
#===================================================
"""@app.route('/api/submit_service_request', methods=['POST'])
def api_submit_service_request():
    # Retrieve form data and create a new Services object
    service_type = request.form.get('serviceType')
    student_id = request.form.get('studentID')
    student_name = request.form.get('studentName')

    # Add other fields based on your requirements

    # Create a new Services object
    new_service = Services(
        service_type=service_type,
        student_id=student_id,
        student_name=student_name,
        created_at=datetime.utcnow(),
        # Add other fields based on your requirements
    )

    # Save the new service request to the database
    db.session.add(new_service)
    db.session.commit()

    # Return a response (you can customize this based on your needs)
    return jsonify({'message': 'Service request submitted successfully!'})"""


#===================================================
# TESTING AREA
@student_api.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    # Debug print statement
    student = Student.query.get(current_user_id)
    if student:
        return jsonify(student.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('student_api.login'))


def get_gender_string(gender_code):
    if gender_code == 1:
        return 'Male'
    elif gender_code == 2:
        return 'Female'
    else:
        return 'Undefined'  # Handle any other values

@student_api.route('/student-details', methods=['GET'])
# @jwt_required()
def fetchStudentDetails():
    user_id = session.get('user_id')

    # Debug print statement
    student = Student.query.get(user_id)
    if student:
        gender_string = get_gender_string(student.gender)

        return jsonify({
            "studentName": student.name,
            "studentNumber": student.studentNumber,
            "gender": gender_string,
            "email": student.email,
            "mobileNumber": student.mobileNumber,
            "address": student.address,
            "dateofBirth": student.dateofBirth,
            "placeofBirth": student.placeofBirth,
        })
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
    

#===============================================================================================#
#====================================Students Functions=========================================#
#===============================================================================================#

#crossenrollment
def create_crossenrollment_form(form_data, files, student_id):
    studentNumber = form_data['studentNumber']
    name = form_data['name']
    school_for_cross_enrollment = form_data['crossEnrollmentSchool']
    total_number_of_units = int(form_data['crossEnrollmentUnits'])
    authorized_subjects_to_take = form_data['authorizedSubjects']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    application_letter_file = files.get('applicationLetter')
    permit_to_cross_enroll_file = files.get('permitToCrossEnroll')

    if not studentNumber or not name or not school_for_cross_enrollment or total_number_of_units <= 0 or not authorized_subjects_to_take:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    if not application_letter_file or not permit_to_cross_enroll_file:
        flash('Please provide both application letter and permit to cross-enroll files.', 'danger')
        return None

    application_letter_filename = secure_filename(application_letter_file.filename)
    application_letter_data = application_letter_file.read()

    permit_to_cross_enroll_filename = secure_filename(permit_to_cross_enroll_file.filename)
    permit_to_cross_enroll_data = permit_to_cross_enroll_file.read()

    new_cross_enrollment = CrossEnrollment(
        studentNumber=studentNumber,
        name=name,
        school_for_cross_enrollment=school_for_cross_enrollment,
        total_number_of_units=total_number_of_units,
        authorized_subjects_to_take=authorized_subjects_to_take,
        application_letter_filename=application_letter_filename,
        application_letter_data=application_letter_data,
        permit_to_cross_enroll_filename=permit_to_cross_enroll_filename,
        permit_to_cross_enroll_data=permit_to_cross_enroll_data,
        user_responsible=user_responsible,
        status=status,
        created_at=datetime.utcnow(),  # Set the creation time
        student_id=student_id,  # Pass the student_id from the login
    )

    return new_cross_enrollment

#===============================================================================================#

#manualenrollment
# Manual Enrollment Form function
def create_manualenrollment_form(form_data, files, student_id):
    studentNumber = form_data['studentNumber']
    name = form_data['name']
    enrollment_type = form_data['enrollment_type']
    reason = form_data['reason']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    me_file = files.get('me_file')

    if not studentNumber or not name or not enrollment_type or not reason:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    if not me_file:
        flash('Please provide the manual enrollment file.', 'danger')
        return None

    me_file_filename = secure_filename(me_file.filename)
    me_file_data = me_file.read()

    new_manual_enrollment = ManualEnrollment(
        studentNumber=studentNumber,
        name=name,
        enrollment_type=enrollment_type,
        reason=reason,
        me_file_filename=me_file_filename,
        me_file_data=me_file_data,
        user_responsible=user_responsible,
        status=status,
        created_at=datetime.utcnow(),
        student_id=student_id,
    )

    return new_manual_enrollment

#====================================================================================================#
#=====================================Petition Requests==============================================#
#====================================================================================================#

def create_petitionrequest_form(form_data, student_id):
    studentNumber = form_data['studentNumber']
    name = form_data['name']
    subjectCode = form_data['subjectCode']
    subjectName = form_data['subjectName']
    petitionType = form_data['petitionType']
    requestReason = form_data['requestReason']
    userResponsible = form_data['userResponsible']
    status = form_data['status']

    if not studentNumber or not name or not subjectCode or not subjectName or not petitionType or not requestReason or not userResponsible:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    new_petition_request = PetitionRequest(
        studentNumber=studentNumber,
        name=name,
        subject_code=subjectCode,
        subject_name=subjectName,
        petition_type=petitionType,
        request_reason=requestReason,
        user_responsible=userResponsible,
        status=status,
        created_at=datetime.utcnow(),
        student_id=student_id,
    )

    return new_petition_request

#====================================================================================================#
#====================================Certificate Requests============================================#
#====================================================================================================#


def create_certification_request(form_data, files, student_id):
    studentNumber = form_data['studentNumber']
    name = form_data['name']
    certification_type = form_data['certification_type']
    request_form_file = files.get('request_form_file')
    identification_card_file = files.get('identification_card_file')
    is_representative = 'is_representative' in form_data  # Check if the checkbox is present in the form data
    authorization_letter_file = files.get('authorization_letter_file')
    representative_id_file = files.get('representative_id_file')
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    # Validate required fields
    if not studentNumber or not name or not certification_type or not request_form_file or not identification_card_file:
        flash('Please fill out all required fields and provide valid values.', 'danger')
        return None

    # Read file data
    request_form_filename = secure_filename(request_form_file.filename) if request_form_file else None
    request_form_data = request_form_file.read() if request_form_file else None

    identification_card_filename = secure_filename(identification_card_file.filename) if identification_card_file else None
    identification_card_data = identification_card_file.read() if identification_card_file else None

    authorization_letter_filename = secure_filename(authorization_letter_file.filename) if authorization_letter_file else None
    authorization_letter_data = authorization_letter_file.read() if authorization_letter_file else None

    representative_id_filename = secure_filename(representative_id_file.filename) if representative_id_file else None
    representative_id_data = representative_id_file.read() if representative_id_file else None

    # Create CertificationRequest instance
    new_certification_request = CertificationRequest(
        studentNumber=studentNumber,
        name=name,
        certification_type=certification_type,
        request_form_filename=request_form_filename,
        request_form_data=request_form_data,
        identification_card_filename=identification_card_filename,
        identification_card_data=identification_card_data,
        is_representative=is_representative,
        authorization_letter_filename=authorization_letter_filename,
        authorization_letter_data=authorization_letter_data,
        representative_id_filename=representative_id_filename,
        representative_id_data=representative_id_data,
        created_at=datetime.utcnow(),
        user_responsible=user_responsible,
        status=status,
        student_id=student_id,
    )

    return new_certification_request
