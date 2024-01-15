# api/api_routes.py
import base64
import logging
from operator import and_

from sqlalchemy import desc, func
from decorators.auth_decorators import role_required
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import CourseEnrolled, Services, SubjectList, db, Class, ClassSubject, Course, Metadata, Student, StudentClassSubjectGrade, Subject
from werkzeug.utils import secure_filename
from datetime import datetime #, timedelta, timezone
#from models import Services
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS 
from decorators.auth_decorators import role_required

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

def get_student_number_by_id(StudentId):
    # Query the database for the student using filter_by
    student = Student.query.filter_by(StudentId=StudentId).first()

    # Check if the student exists and return the StudentNumber
    if student:
        return student.StudentNumber
    else:
        # Return None if no student is found
        return None
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
@role_required('student')
def fetchStudentDetails():
    user_id = session.get('user_id')

    student = Student.query.get(user_id)

    if student:
        Gender_string = get_Gender_string(student.Gender)

        return jsonify({
            'FirstName': student.FirstName,
            'LastName': student.LastName,
            'MiddleName': student.MiddleName,
            'StudentNumber': student.StudentNumber,
            'Gender': Gender_string,
            'Email': student.Email,
            'ResidentialAddress': student.ResidentialAddress,
            'DateOfBirth': student.DateOfBirth,
            'PlaceOfBirth': student.PlaceOfBirth,
            'MobileNumber': student.MobileNumber,
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
    
@student_api.route('/student-subjects', methods=['GET'])
@role_required('student')
def fetchStudentSubjects():
    # Retrieve student ID from the session
    student_id = session.get('user_id')

    if student_id is None:
        return jsonify({'error': 'User not authenticated'}), 401

    # Get current subjects for the student
    subjects = (
        db.session.query(Subject)
        .join(ClassSubject, Subject.SubjectId == ClassSubject.SubjectId)
        .join(StudentClassSubjectGrade, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
        .join(CourseEnrolled, CourseEnrolled.CourseId == ClassSubject.ClassId)
        .filter(CourseEnrolled.StudentId == student_id)
        .distinct(Subject.SubjectId)
        .all()
    )

    # Convert the result to a list of dictionaries
    subject_list = [
        {
            'SubjectId': subject.SubjectId,
            'SubjectCode': subject.SubjectCode,
            'Name': subject.Name,
            'Credits': subject.Credits,
            # Add more fields as needed
        }
        for subject in subjects
    ]

    return jsonify(subject_list)



#================================================================================#
#functions
def create_services_application(form_data, files, StudentId, FacultyId):
    ServiceType = 'add_subject'
    ServiceDetails = form_data.get('serviceDetails', '')
    
    subjectIDs = form_data.getlist('subjectIDs')
    subjectIDs = [int(id) for id in subjectIDs]  # Convert to integers

    ServicesImg = files.get('servicesImg')
    Servicesdata = files.get('servicesdata')

    ServicesImg_data = ServicesImg.read() if ServicesImg else None
    Servicesdata_data = Servicesdata.read() if Servicesdata else None

    # Add additional validations as needed
    Status = 'pending'
    try:
        new_service_application = Services(
            StudentId=StudentId,
            FacultyId=FacultyId,
            ServiceType=ServiceType,
            ServiceDetails=ServiceDetails,
            ServicesImg=ServicesImg_data,
            Servicesdata=Servicesdata_data,
            Status=Status,
        )
        db.session.add(new_service_application)
        db.session.commit()
        db.session.refresh(new_service_application)

        created_service_id = new_service_application.ServiceId
        for subjectID in subjectIDs:
            subject_list_entry = SubjectList(
                SubjectId=subjectID,
                ServiceId=created_service_id
            )
            db.session.add(subject_list_entry)
        # Commit the new SubjectList entries to the database
        db.session.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        print(f'An error occurred: {e}')
        # Optionally, re-raise the exception if you want it to be handled further up the call stack
        raise e


    return new_service_application