# api/api_routes.py
import base64
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import AddSubjects, CertificationRequest, ChangeOfSubjects, CrossEnrollment, GradeEntry, ManualEnrollment, OverloadApplication, PetitionRequest, Student
from werkzeug.utils import secure_filename
from datetime import datetime
#from models import Services
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS 

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
def authenticate_user(username, Password):
    # Your authentication logic goes here
    # Check if the provided username and Password match a user in your database
    # If authenticated, retrieve the user ID and set it in the session
    user = User.query.filter_by(username=username).first()  # Replace User with your actual model
    if user and user.check_password(Password):  # Replace check_password with your validation logic
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
    session['user_id'] = student.StudentId
    session['StudentNumber'] = student.StudentNumber
    session['Name'] = student.Name
    session['Gender'] = student.Gender
    session['Email'] = student.Email
    session['address'] = student.address
    session['DateofBirth'] = student.DateofBirth
    session['PlaceofBirth'] = student.PlaceofBirth
    session['ResidentialAddress'] = student.ResidentialAddress
    session['MobileNumber'] = student.MobileNumber
    session['userImg'] = student.userImg

# Login function for student to go to student_overload
@student_api.route('/login-Overload', methods=['POST'])
def login_Overload():
    # ... (other code)
    if is_user_logged_in_overload():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_overload'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']

        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Use the function to store user details in the session
            store_user_details_in_session(student)

            return redirect(url_for('student_portal_overload'))
        else:
            flash('Invalid Email or Password', 'danger')

    return render_template('student/login.html')

#========================================================

def is_user_logged_in_certification():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

# Login function for student to goto certification
@student_api.route('/login-Certification', methods=['GET', 'POST'])
def login_Certification():
    if is_user_logged_in_certification():
        # If the user is already logged in, redirect to the certifications page
        return redirect(url_for('student_portal_certification'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['Name'] = student.Name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_certification', student_detailss=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
def is_user_logged_in_changesubsched():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

# Login function for student to goto changesubsched
@student_api.route('/login-Changesubsched', methods=['GET', 'POST'])
def login_Changesubsched():
    if is_user_logged_in_changesubsched():
        # If the user is already logged in, redirect to the changesubsched page
        return redirect(url_for('student_portal_changesubsched'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['Name'] = student.Name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_changesubsched', student_detailss=session))

        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in
def is_user_logged_in_enrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-Enrollment', methods=['GET', 'POST'])
def login_Enrollment():
    if is_user_logged_in_enrollment():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_enrollment'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['Name'] = student.Name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_enrollment', student_detailss=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in addingofsubject
def is_user_logged_in_addingofsubject():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-AddingofSubjects', methods=['GET', 'POST'])
def login_Addingofsubject():
    if is_user_logged_in_addingofsubject():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_addingsubject'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['name'] = student.name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_addingsubject', student_details=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in tutorial of subjects
def is_user_logged_in_tutorial():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-Tutorial', methods=['GET', 'POST'])
def login_Tutorial():
    if is_user_logged_in_tutorial():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_tutorial'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['name'] = student.name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_tutorial', student_detailss=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in shifting
def is_user_logged_in_shifting():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-Shifting', methods=['GET', 'POST'])
def login_Shifting():
    if is_user_logged_in_shifting():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_shifting'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['name'] = student.name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_shifting', student_detailss=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in shifting
def is_user_logged_in_petition():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-Petition', methods=['GET', 'POST'])
def login_Petition():
    if is_user_logged_in_petition():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_petition'))

    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['name'] = student.name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_petition', student_detailss=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in gradeentry
def is_user_logged_in_gradeentry():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-Gradeentry', methods=['GET', 'POST'])
def login_Gradeentry():
    if is_user_logged_in_gradeentry():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_gradeentry'))
    
    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['name'] = student.name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_gradeentry', student_detailss=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================

# Function to check if the user is logged in shifting
def is_user_logged_in_crossenrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-Crossenrollment', methods=['GET', 'POST'])
def login_Crossenrollment():
    if is_user_logged_in_crossenrollment():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_crossenrollment'))

    if request.method == 'POST':
        StudentNumber = request.data['StudentNumber']
        Password = request.data['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.StudentId
            session['StudentNumber'] = student.StudentNumber
            session['name'] = student.name
            session['Gender'] = student.Gender
            session['Email'] = student.Email
            session['address'] = student.address
            session['DateofBirth'] = student.DateofBirth
            session['PlaceofBirth'] = student.PlaceofBirth
            session['ResidentialAddress'] = student.ResidentialAddress
            session['MobileNumber'] = student.MobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_crossenrollment', student_detailss=session))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#===========================================================#
#==============The real login in the true manners===========#
#===========================================================#
#for All Students
@student_api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']

        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_dashboard'))

        else:
            flash('Invalid Email or Password', 'danger')

    return redirect(url_for('studentLogin'))


#=====================================================================#



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


def get_Gender_string(Gender_code):
    if Gender_code == 1:
        return 'Male'
    elif Gender_code == 2:
        return 'Female'
    else:
        return 'Undefined'  # Handle any other values

#applicable to all the applications if you want student
@student_api.route('/student-details', methods=['GET'])
def fetchStudentDetails():
    user_id = session.get('user_id')

    student = Student.query.get(user_id)

    if student:
        # Convert userImg to base64 string
        user_img_base64 = base64.b64encode(student.userImg).decode('utf-8')

        Gender_string = get_Gender_string(student.Gender)

        return jsonify({
            'Name': student.Name,
            "StudentNumber": student.StudentNumber,
            "Gender": Gender_string,
            "Email": student.Email,
            "MobileNumber": student.MobileNumber,
            "address": student.address,
            "DateofBirth": student.DateofBirth,
            "PlaceofBirth": student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': user_img_base64,  # Return base64-encoded string
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

#overload
# Create function for OverloadApplication
def create_overload_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    programcourse = form_data['programcourse']
    semester = form_data['semester']
    subjects_to_add = form_data['subjectsToAdd']
    justification = form_data['justification']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    # Check if a file is provided
    if 'file' not in files:
        flash('No file part', 'danger')
        return None

    file = files['file']
    # Check if the file field is empty
    if file.filename == '':
        flash('No selected file', 'danger')
        return None

    file_data = file.read()  # Read the file data
    file_filename = secure_filename(file.filename)

    # Additional validation logic can be added here

    # Check if any of the required fields is empty
    if not StudentNumber or not Name or not semester or not subjects_to_add or not justification:
        flash('Please fill out all required fields.', 'danger')
        return None

    new_overload_application = OverloadApplication(
        Name=Name,  # Adjust as per your application logic
        StudentNumber=StudentNumber,
        programcourse=programcourse,
        semester=semester,
        subjects_to_add=subjects_to_add,
        justification=justification,
        file_filename=file_filename,
        file_data=file_data,
        user_responsible=user_responsible,
        status=status,
        StudentId=StudentId
    )

    return new_overload_application
#===============================================================================================#

#crossenrollment
def create_crossenrollment_form(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    school_for_cross_enrollment = form_data['crossEnrollmentSchool']
    total_number_of_units = int(form_data['crossEnrollmentUnits'])
    authorized_subjects_to_take = form_data['authorizedSubjects']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    application_letter_file = files.get('applicationLetter')
    permit_to_cross_enroll_file = files.get('permitToCrossEnroll')

    if not StudentNumber or not Name or not school_for_cross_enrollment or total_number_of_units <= 0 or not authorized_subjects_to_take:
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
        StudentNumber=StudentNumber,
        Name=Name,
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
        StudentId=StudentId,  # Pass the StudentId from the login
    )

    return new_cross_enrollment

#===============================================================================================#

#manualenrollment
# Manual Enrollment Form function
def create_manualenrollment_form(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    enrollment_type = form_data['enrollment_type']
    reason = form_data['reason']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    me_file = files.get('me_file')

    if not StudentNumber or not Name or not enrollment_type or not reason:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    if not me_file:
        flash('Please provide the manual enrollment file.', 'danger')
        return None

    me_file_filename = secure_filename(me_file.filename)
    me_file_data = me_file.read()

    new_manual_enrollment = ManualEnrollment(
        StudentNumber=StudentNumber,
        Name=Name,
        enrollment_type=enrollment_type,
        reason=reason,
        me_file_filename=me_file_filename,
        me_file_data=me_file_data,
        user_responsible=user_responsible,
        status=status,
        created_at=datetime.utcnow(),
        StudentId=StudentId,
    )

    return new_manual_enrollment

#========================================Change of Subjects============================#

def create_addsubjects_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    subject_Names = form_data['subject_Names']
    enrollment_type = form_data['enrollment_type']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    if 'filesubject' not in files:
        flash('Please provide the Subjects file.', 'danger')
        return None

    filesubject = files['filesubject']

    if filesubject.filename == '':
        flash('No selected file', 'danger')
        return None
    
    file_data = filesubject.read()  # Read the file data
    file_name = secure_filename(filesubject.filename) 
    # Check if other inputs are provided

    if not StudentNumber or not Name or not subject_Names or not enrollment_type:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None  # Replace 'add_subjects' with the actual route

    # Additional validation logic can be added here

    new_addsubjects_application = AddSubjects(
        StudentNumber=StudentNumber,
        Name=Name,
        subject_Names=subject_Names,
        enrollment_type=enrollment_type,
        file_data=file_data,
        file_name=file_name,
        user_responsible=user_responsible,
        status=status,
        StudentId=StudentId,
    )
    
    return new_addsubjects_application

    
#=========================================================#

#changeofsubjects
# Change Subjects Form function
def create_changesubjects_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    enrollment_type = form_data['enrollment_type']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    ace_form = files.get('ace_form')

    if not StudentNumber or not Name or not enrollment_type:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    if not ace_form:
        flash('Please provide the manual enrollment file.', 'danger')
        return None

    ace_form_filename = secure_filename(ace_form.filename)
    ace_form_data = ace_form.read()

    new_changesubjects_application = ChangeOfSubjects(
        StudentNumber=StudentNumber,
        Name=Name,
        enrollment_type=enrollment_type,
        ace_form_filename=ace_form_filename,
        ace_form_data=ace_form_data,
        user_responsible=user_responsible,
        status=status,
        created_at=datetime.utcnow(),
        StudentId=StudentId,
    )

    return new_changesubjects_application

#=====================================Petition Requests==============================================#

def create_petitionrequest_form(form_data, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    subjectCode = form_data['subjectCode']
    subjectName = form_data['subjectName']
    petitionType = form_data['petitionType']
    requestReason = form_data['requestReason']
    userResponsible = form_data['userResponsible']
    status = form_data['status']

    if not StudentNumber or not Name or not subjectCode or not subjectName or not petitionType or not requestReason or not userResponsible:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    new_petition_request = PetitionRequest(
        StudentNumber=StudentNumber,
        Name=Name,
        subject_code=subjectCode,
        subject_name=subjectName,
        petition_type=petitionType,
        request_reason=requestReason,
        user_responsible=userResponsible,
        status=status,
        created_at=datetime.utcnow(),
        StudentId=StudentId,
    )

    return new_petition_request

#=================================================Grade entry========================================#

def create_gradeentry_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    application_type = form_data['application_type']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

     # Check if a file is provided
    if 'completion_form' not in files:
        flash('No file part', 'danger')
        return None

    completion_form = files['completion_form']
    # Check if the file field is empty
    if completion_form.filename == '':
        flash('No selected file', 'danger')
        return None

    completion_form_data = completion_form.read()  # Read the file data
    completion_form_filename = secure_filename(completion_form.filename)
#==========================================================#
     # Check if a file is provided
    if 'class_record' not in files:
        flash('No file part', 'danger')
        return None

    class_record = files['class_record']
    # Check if the file field is empty
    if class_record.filename == '':
        flash('No selected file', 'danger')
        return None

    class_record_data = class_record.read()  # Read the file data
    class_record_filename = secure_filename(class_record.filename)
#==========================================================#
     # Check if a file is provided
    if 'affidavit' not in files:
        flash('No file part', 'danger')
        return None

    affidavit = files['affidavit']
    # Check if the file field is empty
    if affidavit.filename == '':
        flash('No selected file', 'danger')
        return None

    affidavit_data = affidavit.read()  # Read the file data
    affidavit_filename = secure_filename(affidavit.filename)

            # Check if a other input is provided
    if not StudentNumber or not Name or not application_type:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None  # Replace 'add_subjects' with the actual route

    if not completion_form or not class_record or not affidavit:
        flash('Please provide both application letter and permit to cross-enroll files.', 'danger')
        return None


    new_gradeentry_application = GradeEntry(
        StudentNumber=StudentNumber,
        Name=Name,
        application_type=application_type,
        completion_form_filename=completion_form_filename,
        completion_form_data=completion_form_data,
        class_record_filename=class_record_filename,
        class_record_data=class_record_data,
        affidavit_filename=affidavit_filename,
        affidavit_data=affidavit_data,
        user_responsible=user_responsible,
        status=status,
        created_at=datetime.utcnow(),  # Set the creation time
        StudentId=StudentId,  # Pass the StudentId from the login
    )

    return new_gradeentry_application


#====================================Certificate Requests============================================#
#====================================================================================================#


def create_certification_request(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    certification_type = form_data['certification_type']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

     # Check if a file is provided
    if 'request_form' not in files:
        flash('No file part', 'danger')
        return None

    request_form = files['request_form']
    # Check if the file field is empty
    if request_form.filename == '':
        flash('No selected file', 'danger')
        return None

    request_form_data = request_form.read()  # Read the file data
    request_form_filename = secure_filename(request_form.filename)
#==========================================================#
     # Check if a file is provided
    if 'identification_card' not in files:
        flash('No file part', 'danger')
        return None

    identification_card = files['identification_card']
    # Check if the file field is empty
    if identification_card.filename == '':
        flash('No selected file', 'danger')
        return None

    identification_card_data = identification_card.read()  # Read the file data
    identification_card_filename = secure_filename(identification_card.filename)
#==========================================================#
    is_representative = 'is_representative' in form_data  # Check if the checkbox is present in the form data
#==========================================================#
     # Check if a file is provided
    if 'authorization_letter' not in files:
        flash('No file part', 'danger')
        return None

    authorization_letter = files['authorization_letter']
    # Check if the file field is empty
    if authorization_letter.filename == '':
        flash('No selected file', 'danger')
        return None

    authorization_letter_data = authorization_letter.read()  # Read the file data
    authorization_letter_filename = secure_filename(authorization_letter.filename)
#========================================================#
     # Check if a file is provided
    if 'representative_id' not in files:
        flash('No file part', 'danger')
        return None

    representative_id = files['representative_id']
    # Check if the file field is empty
    if representative_id.filename == '':
        flash('No selected file', 'danger')
        return None

    representative_id_data = representative_id.read()  # Read the file data
    representative_id_filename = secure_filename(representative_id.filename)

    if not StudentNumber or not Name or not certification_type or not request_form or not identification_card:
        flash('Please fill out all required fields and provide valid values.', 'danger')
        return None

    # Create CertificationRequest instance
    new_certification_request = CertificationRequest(
        StudentNumber=StudentNumber,
        Name=Name,
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
        StudentId=StudentId,
    )

    return new_certification_request


#===============================================================================================#
def create_shifting_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    current_program = form_data['currentProgram']
    residency_year = form_data['residencyYear']
    intended_program = form_data['intendedProgram']
    qualifications = form_data['qualifications']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    if 'filesubject' not in files:
        flash('Please provide the Subjects file.', 'danger')
        return None

    fileshifting = files['fileshifting']

    if fileshifting.filename == '':
        flash('No selected file', 'danger')
        return None
    
    file_data = fileshifting.read()  # Read the file data
    file_filename = secure_filename(fileshifting.filename) 
    # Check if other inputs are provided

    if not StudentNumber or not Name or not current_program or not residency_year:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None  # Replace 'add_subjects' with the actual route

    # Additional validation logic can be added here

    new_shifting_application = AddSubjects(
        StudentNumber=StudentNumber,
        Name=Name,
        current_program=current_program,
        residency_year=residency_year,
        intended_program=intended_program,
        qualifications=qualifications,
        file_filename=file_filename,
        file_data=file_data,
        user_responsible=user_responsible,
        status=status,
        StudentId=StudentId,
    )
    
    return new_shifting_application

#===============================================================================================#
#===============================Semester, Program, YearLevel====================================#
#===============================================================================================#

"""# Insert function for Program
def insert_program(form_data):
    # Get the form data
    programCode = form_data['programCode']
    programName = form_data['programName']

    new_program = Program(
        programCode=programCode,
        programName=programName,
    )
    return new_program

# Insert function for YearLevel
def insert_year_level(form_data):

        # Get the form data
    yearLevel = form_data['yearLevel']
    #programId = form_data['programId']

    new_year_level = YearLevel(
        yearLevel=yearLevel,
       # programId=programId,
    )
    return new_year_level

# Insert function for Semester
def insert_semester(form_data):
    semesterName = form_data['semesterName']
    
    new_semester = Semester(
        semesterName=semesterName, 
    #yearId=yearId
    )
    
    return new_semester

# Insert function for CourseSub
def insert_course_sub(form_data):

    courseSub_Code = form_data['courseSub_Code']
    Sub_Description = form_data['Sub_Description']

    new_course_sub = CourseSub(
        courseSub_Code=courseSub_Code, Sub_Description=Sub_Description,
    )
    return new_course_sub
"""














