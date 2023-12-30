# api/api_routes.py
import base64
from decorators.auth_decorators import role_required
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import AddSubjects, CertificationRequest, ChangeOfSubjects, CrossEnrollment, GradeEntry, ManualEnrollment, Notification, OverloadApplication, PetitionRequest, ShiftingApplication, Student, TutorialRequest
from werkzeug.utils import secure_filename
from datetime import datetime #, timedelta, timezone
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
# needed in the utils.py
#have problem
#condition needed it can put in utils.py
def getCurrentUser():
    current_user_id = session.get('user_id')
    return Student.query.get(current_user_id)    

def getCurrentUserStudentNumber():
    current_student_number = session.get('StudentNumber')
    return Student.query.get(current_student_number)

#===============================================================#
#Downloadable files for Adding Subjects
@student_api.route('/download/pdf_file/Adding_subject_form')
def download_AddingSubs():
    pdf_path = "static/pdf_files/Adding_subject_form.pdf"  # Replace with the actual path to your PDF file
    return os.sendfle(pdf_path, as_attachment=True, download_name="Adding_subject_form.pdf")

#Downloadable files for Change of Schedule and Subjects
@student_api.route('/download/pdf_file/Change_of_subjects')
def download_Change_Sched_Subs():
    pdf_path = "static/pdf_files/Change_of_subjects.pdf"  # Replace with the actual path to your PDF file
    return os.sendfile(pdf_path, as_attachment=True, download_name="Change_of_subjects.pdf")

#Downloadable files for Accreditation
@student_api.route('/download/pdf_file/Accreditation-for-Shiftees-and-Regular')
def download_Accreditation():
    pdf_path = "static/pdf_files/Accreditation-for-Shiftees-and-Regular.pdf"  # Replace with the actual path to your PDF file
    return os.send_file(pdf_path, as_attachment=True, download_name="Accreditation-for-Shiftees-and-Regular.pdf")

#Downloadable files for OverLoads
@student_api.route('/download/pdf_file/Overload-3-6-units')
def download_Overload_Subs():
    pdf_path = "static/pdf_files/Overload-3-6-units.pdf"  # Replace with the actual path to your PDF file
    return os.send_file(pdf_path, as_attachment=True, download_name="Overload-3-6-units.pdf")

#Downloadable files for RO Form
@student_api.route('/download/pdf_file/RO-Form')
def download_RO_form():
    pdf_path = "static/pdf_files/RO-Form.pdf"  # Replace with the actual path to your PDF file
    return os.send_file(pdf_path, as_attachment=True, download_name="RO-Form.pdf")




# Api/v1/student/api_routes.py
#================================================================
# Function to check if the user is logged in
def is_user_logged_in_overload():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_overload'))
        else:
            flash('Invalid Email or Password', 'danger')

    return render_template('student/login_for_overload.html')

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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_certification'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login_certification.html')

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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_changesubsched'))

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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_enrollment'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in addingofsubject
def is_user_logged_in_addingofsubjects():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for student to goto student_enrollment
@student_api.route('/login-AddingofSubjects', methods=['POST'])
def login_AddingofSubjects():
    if is_user_logged_in_addingofsubjects():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_addingofsubjects'))

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

            return redirect(url_for('student_portal_addingofsubjects'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login_addsubjects.html')

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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_tutorial'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login_tutorial.html')

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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_shifting'))
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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_petition'))
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
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'

            return redirect(url_for('student_portal_gradeentry'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login_gradeentry.html')

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
        StudentNumber = request.form['StudentNumber']
        Password = request.form['Password']
        
        student = Student.query.filter_by(StudentNumber=StudentNumber).first()
        if student and check_password_hash(student.Password, Password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.StudentId)
            session['access_token'] = access_token
            session['user_id'] = student.StudentId
            session['user_role'] = 'student'
            
            return redirect(url_for('student_portal_crossenrollment'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('student/login_crossenrollment.html')

#===========================================================#
#==============The real login in the true manners===========#
#===========================================================#

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
            
            # Set the last activity timestamp
           # session['last_activity'] = datetime.now()

            return redirect(url_for('student_dashboard'))

        else:
            flash('Invalid Email or Password', 'danger')

    return redirect(url_for('studentLogin'))

    # Middleware to check for inactivity and redirect to login if needed
"""@student_api.before_request
def check_user_activity():
    if 'user_id' in session and 'last_activity' in session:
        last_activity = session['last_activity']
        now_utc = datetime.now(timezone.utc)
        
        # Convert last_activity to an aware datetime object
        if not last_activity.tzinfo:
            last_activity = last_activity.replace(tzinfo=timezone.utc)

        inactive_time = now_utc - last_activity

        # Redirect to login if inactive for 5 minutes
        if inactive_time > timedelta(minutes=5):
            return redirect(url_for('studentLogin'))
    
    # Update the last activity timestamp
    session['last_activity'] = datetime.now(timezone.utc)"""

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
#take 1 - it only presenting message in terminal 
"""def update_student_profile(form_data, StudentId):
    Email = form_data['Email']
    address = form_data['address']
    MobileNumber = form_data['MobileNumber']

    # You can perform additional validation or checks here if needed

    student = Student.query.get(StudentId)
    if student:
        student.Email = Email
        student.address = address
        student.MobileNumber = MobileNumber
        db.session.commit()
        return True  # Indicates successful update
    else:
        return False  # Indicates failure to find the student or update"""
#take 2
@student_api.route('/update-student-details', methods=['POST'])
def updateStudentDetails():
    user_id = getCurrentUser()
    student = Student.query.get(user_id)

    if not student:
        flash('User not found', 'danger')
        return jsonify({'message': 'User not found'}), 404

    # Check if the request is JSON or form data
   # Check if the request is JSON or form data
    if request.is_json:
        # Update from JSON data
        student.Email = request.json.get('Email', student.Email)
        student.MobileNumber = request.json.get('MobileNumber', student.MobileNumber)
        student.address = request.json.get('address', student.address)
    else:
        # Update from form data
        student.Email = request.form.get('Email', student.Email)
        student.MobileNumber = request.form.get('MobileNumber', student.MobileNumber)
        student.address = request.form.get('address', student.address)

    # Check if Email and MobileNumber are not None or empty
    if student.Email is not None and student.MobileNumber is not None:
        # db.session.commit()
        return jsonify({'message': 'Student details updated successfully'})
    else:
        flash('Email and MobileNumber cannot be empty', 'danger')
        return jsonify({'message': 'Email and MobileNumber cannot be empty'}), 400



#================================================================================#
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
    Name = form_data['Name']
    StudentNumber = form_data['StudentNumber']
    programcourse = form_data['programcourse']
    semester = form_data['semester']
    subjects_to_add = form_data['subjects_To_Add']
    justification = form_data['justification']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    # Check if a file is provided
    if 'fileoverload' not in files:
        flash('No file part', 'danger')
        return None

    fileoverload = files['fileoverload']
    # Check if the file field is empty
    if fileoverload.filename == '':
        flash('No selected file', 'danger')
        return None

    file_data = fileoverload.read()  # Read the file data
    file_filename = secure_filename(fileoverload.filename)

    # Additional validation logic can be added here

    # Check if any of the required fields is empty
    if not Name or not StudentNumber or not programcourse or not semester or not subjects_to_add:
        flash('Please fill out all required fields.', 'danger')
        return None

    new_overload_application = OverloadApplication(
        StudentNumber=StudentNumber,
        Name=Name,
        programcourse=programcourse,
        semester=semester,
        subjects_to_add=subjects_to_add,
        justification=justification,
        file_filename=file_filename,
        file_data=file_data,
        user_responsible=user_responsible,
        status=status,
        StudentId=StudentId,
        created_at=datetime.utcnow()  # Set created_at to the current timestamp
    )
    
    return new_overload_application
#===============================================================================================#

#crossenrollment
def create_crossenrollment_form(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    school_for_cross_enrollment = form_data['school_for_cross_enrollment']
    total_number_of_units = int(form_data['total_number_of_units'])
    authorized_subjects_to_take = form_data['authorized_subjects_to_take']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    if not StudentNumber or not Name or not school_for_cross_enrollment or not authorized_subjects_to_take:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    files = request.files

    # Check if 'fileTutorial' is provided
    if 'applicationLetter' not in files:
        flash('Please provide the tutorial file.', 'danger')
        return None

    applicationLetter = files['applicationLetter']

    # Check if 'permitToCrossEnroll' is provided
    if 'permitToCrossEnroll' not in files:
        flash('Please provide the second file.', 'danger')
        return None

    permitToCrossEnroll = files['permitToCrossEnroll']

    # Check if fileTutorial is provided and has a filename
    if applicationLetter.filename == '':
        flash('No selected tutorial file', 'danger')
        return None

    # Read the file data for fileTutorial
    application_letter_data = applicationLetter.read()
    application_letter_filename = secure_filename(applicationLetter.filename)

    # Check if permitToCrossEnroll is provided and has a filename
    if permitToCrossEnroll.filename == '':
        flash('No selected second file', 'danger')
        return None

    # Read the file data for permitToCrossEnroll
    permit_to_cross_enroll_data = permitToCrossEnroll.read()
    permit_to_cross_enroll_filename = secure_filename(permitToCrossEnroll.filename)

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
    enrollment_type = form_data['enrollmentType']
    reason = form_data['reason']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    if 'me_file' not in files:
        flash('Please provide the tutorial file.', 'danger')
        return None

    me_file = files['me_file']

    if me_file.filename == '':
        flash('No Selected me_file', 'danger')
        return None
    
    me_file_filename = secure_filename(me_file.filename)
    me_file_data = me_file.read()
    
    if not StudentNumber or not Name or not enrollment_type or not reason:
        flash('Please fill out all fields and provide valid values.', 'danger')
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

    # Log the form submission
    #log_form_submission_to_file(form_data)
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
    subject_code = form_data['subject_code']
    subject_name = form_data['subject_name']
    petition_type = form_data['petition_type']
    request_reason = form_data['request_reason']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    if not StudentNumber or not Name or not subject_code or not subject_name or not petition_type or not request_reason:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    new_petition_request = PetitionRequest(
        StudentNumber=StudentNumber,
        Name=Name,
        subject_code=subject_code,
        subject_name=subject_name,
        petition_type=petition_type,
        request_reason=request_reason,
        user_responsible=user_responsible,
        created_at=datetime.utcnow(),
        status=status,
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

    files = request.files
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

    if 'fileshifting' not in files:
        flash('Please provide the shifitng file.', 'danger')
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

    new_shifting_application = ShiftingApplication(
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


#======================================================================#
# tutorial
def create_tutorial_request(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    subject_code = form_data['subjectCode']
    subject_name = form_data['subjectName']
    user_responsible = form_data['user_responsible']
    status = form_data['status']

    if 'fileTutorial' not in files:
        flash('Please provide the tutorial file.', 'danger')
        return None

    fileTutorial = files['fileTutorial']

    if fileTutorial.filename == '':
        flash('No selected file', 'danger')
        return None
    
    file_data = fileTutorial.read()  # Read the file data
    file_filename = secure_filename(fileTutorial.filename) 
    # Check if other inputs are provided

    if not StudentNumber or not Name or not subject_code or not subject_name:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    # Additional validation logic can be added here

    new_tutorial_request = TutorialRequest(
        StudentNumber=StudentNumber,
        Name=Name,
        subject_code=subject_code,
        subject_name=subject_name,
        file_filename=file_filename,
        file_data=file_data,
        created_at=datetime.utcnow(),
        user_responsible=user_responsible,
        status=status,
        StudentId=StudentId,
    )
    
    return new_tutorial_request
#===============================================================================================#
#Notification
def create_notification(StudentNumber, service_type, user_responsible, status, message, StudentId):
    # Assuming StudentNumber is either part of the form or can be retrieved from the database
    # using StudentId. The following line is a placeholder for actual retrieval logic.
    StudentNumber = get_student_number_by_id(StudentId)

    # Create a new Notification object
    new_notification = Notification(
        StudentNumber=StudentNumber,
        service_type=service_type,
        user_responsible=user_responsible,
        status=status,
        message=message,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        StudentId=StudentId
    )

    return new_notification
#===============================================================================================#



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




def get_student_number_by_id(StudentId):
    # Query the database for the student using filter_by
    student = Student.query.filter_by(StudentId=StudentId).first()

    # Check if the student exists and return the StudentNumber
    if student:
        return student.StudentNumber
    else:
        # Return None if no student is found
        return None









