# api/api_routes.py
import base64
from Api.v1.student.utils import  get_student_services, getAllSubjects, getCurrentSubject, getStudentClassSGrade, getSubjectFuture, getSubjectsGrade
from decorators.auth_decorators import role_required
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import  db, AddSubjects, CertificationRequest, ChangeSubject, CrossEnrollment, GradeEntry, ManualEnrollment, Notification, OverloadApplication, PetitionRequest, ShiftingApplication, Student, TutorialRequest
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
#Chartjs sample
# def get_student_services(student_id):
#     addsubjects_list = AddSubjects.query.filter_by(StudentId=student_id).all()
#     changesubjects_list = ChangeOfSubjects.query.filter_by(StudentId=student_id).all()
#     manual_enrollments_list = ManualEnrollment.query.filter_by(StudentId=student_id).all()
#     certification_request_list = CertificationRequest.query.filter_by(StudentId=student_id).all()
#     grade_entry_list = GradeEntry.query.filter_by(StudentId=student_id).all()
#     cross_enrollment_list = CrossEnrollment.query.filter_by(StudentId=student_id).all()
#     petition_requests_list = PetitionRequest.query.filter_by(StudentId=student_id).all()
#     shifting_applications_list = ShiftingApplication.query.filter_by(StudentId=student_id).all()
#     overload_applications_list = OverloadApplication.query.filter_by(StudentId=student_id).all()
#     tutorial_requests_list = TutorialRequest.query.filter_by(StudentId=student_id).all()

#     services_data = {
#         'addsubjects_list': [subject.to_dict() for subject in addsubjects_list],
#         'changesubjects_list': [subject.to_dict() for subject in changesubjects_list],
#         'manual_enrollments_list': [subject.to_dict() for subject in manual_enrollments_list],
#         'certification_request_list': [subject.to_dict() for subject in certification_request_list],
#         'grade_entry_list': [subject.to_dict() for subject in grade_entry_list],
#         'cross_enrollment_list': [subject.to_dict() for subject in cross_enrollment_list],
#         'petition_requests_list': [subject.to_dict() for subject in petition_requests_list],
#         'shifting_applications_list': [subject.to_dict() for subject in shifting_applications_list],
#         'overload_applications_list': [subject.to_dict() for subject in overload_applications_list],
#         'tutorial_requests_list': [subject.to_dict() for subject in tutorial_requests_list],
#     }

#     return services_data
#Concatinated all the services
@student_api.route('/check_student_services', methods=['GET'])
def check_student_services():
    # Assuming you have access to the student ID (you may need to retrieve it based on your authentication mechanism)
    user_id = getCurrentUser().StudentId

    # Get student services
    services_data = get_student_services(user_id)

    if services_data:
        return jsonify(success=True, message="Student services data is valid.")
    else:
        return jsonify(error=True, message="No data available or data is invalid.")


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
#take 1 - it only presenting Message in terminal 
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
        return jsonify({'Message': 'User not found'}), 404

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
        return jsonify({'Message': 'Student details updated successfully'})
    else:
        flash('Email and MobileNumber cannot be empty', 'danger')
        return jsonify({'Message': 'Email and MobileNumber cannot be empty'}), 400



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
            'MobileNumber': student.MobileNumber,
            'ResidentialAddress': student.ResidentialAddress,
            'DateOfBirth': student.DateOfBirth,
            'PlaceOfBirth': student.PlaceOfBirth,
        })
    else:
        flash('User not found', 'danger')
        return redirect(url_for('student_api.login'))
    
@student_api.route('/all/student', methods=['GET'])
def allstudent():
    api_key = request.headers.get('X-Api-Key')  # Get the API key from the request header

    if api_key in API_KEYS.values():
        return jsonify(Message="You got API data")
    else:
        return jsonify(Message="Invalid key you cant have an access")


# Getting the subjects grades
@student_api.route('/grades', methods=['GET'])
@role_required('student')
def subjectsGrade():
    student = getCurrentUser()
    print('STUDEINT ID: ', student.StudentId)
    if student:
        json_subjects_grade = getSubjectsGrade(student.StudentId)
        if json_subjects_grade:
            return (json_subjects_grade)
        else:
            return jsonify(error="No data available")
    else:
        return render_template('404.html'), 404
    

@student_api.route('/currentsubject', methods=['GET'])
@role_required('student')
def currentsubject():
    student = getCurrentUser()
    print('STUDEINT ID: ', student.StudentId)
    if student:
        json_current_subject = getCurrentSubject(student.StudentId)
        if json_current_subject:
            return (json_current_subject)
        else:
            return jsonify(error="No data available")
    else:
        return render_template('404.html'), 404
    
#For 3rd sem only 
@student_api.route('/studentsubject', methods=['GET'])
@role_required('student')
def subjectsstudent():
    student = getCurrentUser()
    print('STUDEINT ID: ', student.StudentId)
    if student:
        json_subjects_grade = getStudentClassSGrade(student.StudentId)
        if json_subjects_grade:
            return (json_subjects_grade)
        else:
            return jsonify(error="No data available")
    else:
        return render_template('404.html'), 404
    
# for 3rd eyar becasue all the grades are finalized
@student_api.route('/futuresubject', methods=['GET'])
@role_required('student')
def subjectsfuture():
    student = getCurrentUser()
    print('STUDEINT ID: ', student.StudentId)
    if student:
        json_subjects_grade = getSubjectFuture(student.StudentId)
        if json_subjects_grade:
            return (json_subjects_grade)
        else:
            return jsonify(error="No data available")
    else:
        return render_template('404.html'), 404
    
@student_api.route('/allsubject', methods=['GET'])
@role_required('student')
def subjectsall():
    student = getCurrentUser()
    print('STUDEINT ID: ', student.StudentId)
    if student:
        json_subjects_grade = getAllSubjects(student.StudentId)
        if json_subjects_grade:
            return (json_subjects_grade)
        else:
            return jsonify(error="No data available")
    else:
        return render_template('404.html'), 404
    
#====================================== FUNCTION FOR ADDING OF SUBJECTS  =========================================================#
def create_services_application(form_data, files, StudentId):
    FacultyRole = 'Academic Head'

    # Extract individual form data
    SenderName = form_data.get('SenderName', '')
    SenderContactNo = form_data.get('SenderContactNo', '')
    selectedSubjects = form_data.get('selectedSubjects', '')  # Assuming this field holds the selected subjects
    ServiceDetails = form_data.get('ServiceDetails', '')

    PaymentFile = files.get('PaymentFile')  # Adjust the key based on your form
    PaymentFile_data = PaymentFile.read() if PaymentFile else None

    # Add additional validations as needed
    Status = 'Pending'

    try:
        # Create a new service application
        new_service_application = AddSubjects(
            StudentId=StudentId,
            FacultyRole=FacultyRole,
            Subject=selectedSubjects,  # Use the modified field name
            ServiceDetails=ServiceDetails,
            PaymentFile=PaymentFile_data,
            SenderName=SenderName,
            SenderContactNo=SenderContactNo,
            Status=Status,
        )

        db.session.add(new_service_application)
        db.session.commit()
        db.session.refresh(new_service_application)

        created_service_id = new_service_application.AddSubjectId

    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        print(f'An error occurred: {e}')
        # Optionally, re-raise the exception if you want it to be handled further up the call stack
        raise e

    return created_service_id

#=========================================== FUNCTION FOR CHANGE OF SUBJECTS ============================================

def create_change_subject(form_data, files, StudentId):
    FacultyRole = 'Academic Head'

    # Extract individual form data
    FromSubject = form_data.get('fromSubjects', '')
    ToSubject = form_data.get('toSubjects', '')
    SenderName = form_data.get('SenderName', '')
    SenderContactNo = form_data.get('SenderContactNo', '')
    ServiceDetails = form_data.get('ServiceDetails', '')

    PaymentFile = files.get('PaymentFile')  # Adjust the key based on your form

    PaymentFile_data = PaymentFile.read() if PaymentFile else None


    # Add additional validations as needed
    Status = 'pending'

    try:
        # Create a new service application
        changeApplication = ChangeSubject(
            StudentId=StudentId,
            FacultyRole=FacultyRole,
            FromSubject=FromSubject, 
            ToSubject=ToSubject, 
            ServiceDetails=ServiceDetails,
            PaymentFile=PaymentFile_data,
            SenderName=SenderName,
            SenderContactNo=SenderContactNo,
            Status=Status,
        )

        db.session.add(changeApplication)
        db.session.commit()
        db.session.refresh(changeApplication)

        created_change_id = changeApplication.ChangeSubjectId

    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        print(f'An error occurred: {e}')
        # Optionally, re-raise the exception if you want it to be handled further up the call stack
        raise e

    return created_change_id

#===============================================================================================#
#====================================Students Functions=========================================#
#===============================================================================================#

#overload DONE
# Create function for OverloadApplication
def create_overload_application(form_data, files, current_StudentId):
    Name = form_data['Name']
    StudentNumber = form_data['StudentNumber']
    ProgramCourse = form_data['ProgramCourse']
    Semester = form_data['Semester']
    SubjectsToAdd = form_data['SubjectsToAdd']
    Justification = form_data['Justification']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

    # Check if a file is provided
    if 'fileoverload' not in files:
        flash('No file part', 'danger')
        return None

    fileoverload = files['fileoverload']
    # Check if the file field is empty
    if fileoverload.filename == '':
        flash('No selected file', 'danger')
        return None

    Overloaddata = fileoverload.read()  # Read the file data
    Overloadfilename = secure_filename(fileoverload.filename)

    # Additional validation logic can be added here

    # Check if any of the required fields is empty
    if not Name or not StudentNumber or not ProgramCourse or not Semester or not SubjectsToAdd:
        flash('Please fill out all required fields.', 'danger')
        return None

    new_overload_application = OverloadApplication(
        StudentId=current_StudentId,
        StudentNumber=StudentNumber,
        Name=Name,
        ProgramCourse=ProgramCourse,
        Semester=Semester,
        SubjectsToAdd=SubjectsToAdd,
        Justification=Justification,
        Overloadfilename=Overloadfilename,
        Overloaddata=Overloaddata,
        UserResponsible=UserResponsible,
        Status=Status,
        created_at=datetime.utcnow()  # Set created_at to the current timestamp
    )
    
    return new_overload_application

#===============================================================================================#

#crossenrollment
def create_crossenrollment_form(form_data, files, current_StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    SchoolforCrossEnrollment = form_data['SchoolforCrossEnrollment']
    TotalNumberofUnits = int(form_data['TotalNumberofUnits'])
    AuthorizedSubjectstoTake = form_data['AuthorizedSubjectstoTake']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

    if not StudentNumber or not Name or not SchoolforCrossEnrollment or not AuthorizedSubjectstoTake:
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
    ApplicationLetterdata = applicationLetter.read()
    ApplicationLetterfilename = secure_filename(applicationLetter.filename)

    # Check if permitToCrossEnroll is provided and has a filename
    if permitToCrossEnroll.filename == '':
        flash('No selected second file', 'danger')
        return None

    # Read the file data for permitToCrossEnroll
    PermitCrossEnrolldata = permitToCrossEnroll.read()
    PermitCrossEnrollfilename = secure_filename(permitToCrossEnroll.filename)

    new_cross_enrollment = CrossEnrollment(
        StudentId=current_StudentId,  # Pass the StudentId from the login
        StudentNumber=StudentNumber,
        Name=Name,
        SchoolforCrossEnrollment=SchoolforCrossEnrollment,
        TotalNumberofUnits=TotalNumberofUnits,
        AuthorizedSubjectstoTake=AuthorizedSubjectstoTake,
        ApplicationLetterfilename=ApplicationLetterfilename,
        ApplicationLetterdata=ApplicationLetterdata,
        PermitCrossEnrollfilename=PermitCrossEnrollfilename,
        PermitCrossEnrolldata=PermitCrossEnrolldata,
        UserResponsible=UserResponsible,
        Status=Status,
        created_at=datetime.utcnow(),  # Set the creation time
    )

    return new_cross_enrollment

#manualenrollment
# Manual Enrollment Form function
def create_manualenrollment_form(form_data, files, current_StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    EnrollmentType = form_data['enrollmentType']
    Reason = form_data['Reason']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']


    me_file = files['me_file']

    if me_file.filename == '':
        flash('No Selected File', 'danger')
        return None
    
    # if not StudentNumber or not Name or not EnrollmentType or not Reason:
    #     flash('Please fill out all fields and provide valid values.', category='danger')
    #     return None
    
    MeFilefilename = secure_filename(me_file.filename)
    MeFiledata = me_file.read()

    new_manual_enrollment = ManualEnrollment(
        StudentId=current_StudentId,
        StudentNumber=StudentNumber,
        Name=Name,
        EnrollmentType=EnrollmentType,
        Reason=Reason,
        MeFilefilename=MeFilefilename,
        MeFiledata=MeFiledata,
        UserResponsible=UserResponsible,
        Status=Status,
        created_at=datetime.utcnow(),
    )

    return new_manual_enrollment

#========================================Change of Subjects============================#

def create_addsubjects_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    SubjectNames = form_data['SubjectNames']
    EnrollmentType = form_data['EnrollmentType']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

    if 'filesubject' not in files:
        flash('Please provide the Subjects file.', 'danger')
        return None

    filesubject = files['filesubject']

    if filesubject.filename == '':
        flash('No selected file', 'danger')
        return None
    
    AddSubjectFiledata = filesubject.read()  # Read the file data
    AddSubjectFilefilename = secure_filename(filesubject.filename) 
    # Check if other inputs are provided

    if not StudentNumber or not Name or not SubjectNames or not EnrollmentType:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None  # Replace 'add_subjects' with the actual route

    # Log the form submission
    #log_form_submission_to_file(form_data)
    # Additional validation logic can be added here

    new_addsubjects_application = AddSubjects(
        StudentId=StudentId,
        StudentNumber=StudentNumber,
        Name=Name,
        SubjectNames=SubjectNames,
        EnrollmentType=EnrollmentType,
        AddSubjectFiledata=AddSubjectFiledata,
        AddSubjectFilefilename=AddSubjectFilefilename,
        UserResponsible=UserResponsible,
        Status=Status,
    )
    
    return new_addsubjects_application
    
#=========================================================#


#=====================================Petition Requests==============================================#

def create_petitionrequest_form(form_data, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    SubjectCode = form_data['SubjectCode']
    SubjectName = form_data['SubjectName']
    PetitionType = form_data['PetitionType']
    RequestReason = form_data['RequestReason']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

    if not StudentNumber or not Name or not SubjectCode or not SubjectName or not PetitionType or not RequestReason:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    new_petition_request = PetitionRequest(
        StudentId=StudentId,
        StudentNumber=StudentNumber,
        Name=Name,
        SubjectCode=SubjectCode,
        SubjectName=SubjectName,
        PetitionType=PetitionType,
        RequestReason=RequestReason,
        UserResponsible=UserResponsible,
        Status=Status,
        created_at=datetime.utcnow(),
    )

    return new_petition_request

#=================================================Grade entry========================================#

def create_gradeentry_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    ApplicationType = form_data['ApplicationType']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

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

    CompletionFormdata = completion_form.read()  # Read the file data
    CompletionFormfilename = secure_filename(completion_form.filename)
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

    ClassRecorddata = class_record.read()  # Read the file data
    ClassRecordfilename = secure_filename(class_record.filename)
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

    Affidavitdata = affidavit.read()  # Read the file data
    Affidavitfilename = secure_filename(affidavit.filename)

            # Check if a other input is provided
    if not StudentNumber or not Name or not ApplicationType:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None  # Replace 'add_subjects' with the actual route

    if not completion_form or not class_record or not affidavit:
        flash('Please provide both application letter and permit to cross-enroll files.', 'danger')
        return None


    new_gradeentry_application = GradeEntry(
        StudentNumber=StudentNumber,
        Name=Name,
        ApplicationType=ApplicationType,
        CompletionFormfilename=CompletionFormfilename,
        CompletionFormdata=CompletionFormdata,
        ClassRecordfilename=ClassRecordfilename,
        ClassRecorddata=ClassRecorddata,
        Affidavitfilename=Affidavitfilename,
        Affidavitdata=Affidavitdata,
        UserResponsible=UserResponsible,
        Status=Status,
        created_at=datetime.utcnow(),  # Set the creation time
        StudentId=StudentId,  # Pass the StudentId from the login
    )

    return new_gradeentry_application


#====================================Certificate Requests============================================#
#====================================================================================================#


def create_certification_request(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    CertificationType = form_data['CertificationType']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

    # Required file checks
    for field_name in ['request_form', 'identification_card']:
        if field_name not in files or files[field_name].filename == '':
            flash(f'No file provided for {field_name}', 'danger')
            return None

    request_form = files['request_form']
    identification_card = files['identification_card']

    # Reading file data
    RequestFormdata = request_form.read()
    RequestFormfilename = secure_filename(request_form.filename)
    IdentificationCarddata = identification_card.read()
    IdentificationCardfilename = secure_filename(identification_card.filename)

    IsRepresentative = 'IsRepresentative' in form_data and form_data['IsRepresentative'] == 'on'

    # Representative file checks
    AuthorizationLetterdata = AuthorizationLetterfilename = None
    RepresentativeIddata = RepresentativeIdfilename = None

    if IsRepresentative:
        if 'authorization_letter' not in files or files['authorization_letter'].filename == '':
            flash('Authorization letter is required for representatives', 'danger')
            return None

        if 'representative_id' not in files or files['representative_id'].filename == '':
            flash('Representative ID is required for representatives', 'danger')
            return None

        authorization_letter = files['authorization_letter']
        representative_id = files['representative_id']

        AuthorizationLetterdata = authorization_letter.read()
        AuthorizationLetterfilename = secure_filename(authorization_letter.filename)
        RepresentativeIddata = representative_id.read()
        RepresentativeIdfilename = secure_filename(representative_id.filename)

    # Create CertificationRequest instance
    new_certification_request = CertificationRequest(
        StudentNumber=StudentNumber,
        Name=Name,
        CertificationType=CertificationType,
        RequestFormfilename=RequestFormfilename,
        RequestFormdata=RequestFormdata,
        IdentificationCardfilename=IdentificationCardfilename,
        IdentificationCarddata=IdentificationCarddata,
        IsRepresentative=IsRepresentative,
        AuthorizationLetterfilename=AuthorizationLetterfilename,
        AuthorizationLetterdata=AuthorizationLetterdata,
        RepresentativeIdfilename=RepresentativeIdfilename,
        RepresentativeIddata=RepresentativeIddata,
        created_at=datetime.utcnow(),
        UserResponsible=UserResponsible,
        Status=Status,
        StudentId=StudentId,
    )

    return new_certification_request


#===============================================================================================#
def create_shifting_application(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    CurrentProgram = form_data['CurrentProgram']
    ResidencyYear = form_data['ResidencyYear']
    IntendedProgram = form_data['IntendedProgram']
    Qualifications = form_data['Qualifications']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

    if 'fileshifting' not in files:
        flash('Please provide the shifitng file.', 'danger')
        return None

    fileshifting = files['fileshifting']

    if fileshifting.filename == '':
        flash('No selected file', 'danger')
        return None
    
    Shiftingdata = fileshifting.read()  # Read the file data
    Shiftingfilename = secure_filename(fileshifting.filename) 
    # Check if other inputs are provided

    if not StudentNumber or not Name or not CurrentProgram or not ResidencyYear:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None  # Replace 'add_subjects' with the actual route

    # Additional validation logic can be added here

    new_shifting_application = ShiftingApplication(
        StudentId=StudentId,
        StudentNumber=StudentNumber,
        Name=Name,
        CurrentProgram=CurrentProgram,
        ResidencyYear=ResidencyYear,
        IntendedProgram=IntendedProgram,
        Qualifications=Qualifications,
        Shiftingfilename=Shiftingfilename,
        Shiftingdata=Shiftingdata,
        UserResponsible=UserResponsible,
        Status=Status,
    )
    
    return new_shifting_application


#======================================================================#
# tutorial
def create_tutorial_request(form_data, files, StudentId):
    StudentNumber = form_data['StudentNumber']
    Name = form_data['Name']
    SubjectCode = form_data['SubjectCode']
    SubjectName = form_data['SubjectName']
    UserResponsible = form_data['UserResponsible']
    Status = form_data['Status']

    if 'fileTutorial' not in files:
        flash('Please provide the tutorial file.', 'danger')
        return None

    fileTutorial = files['fileTutorial']

    if fileTutorial.filename == '':
        flash('No selected file', 'danger')
        return None
    
    Tutorialdata = fileTutorial.read()  # Read the file data
    Tutorialfilename = secure_filename(fileTutorial.filename) 
    # Check if other inputs are provided

    if not StudentNumber or not Name or not SubjectCode or not SubjectName:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return None

    # Additional validation logic can be added here

    new_tutorial_request = TutorialRequest(
        StudentId=StudentId,
        StudentNumber=StudentNumber,
        Name=Name,
        SubjectCode=SubjectCode,
        SubjectName=SubjectName,
        Tutorialfilename=Tutorialfilename,
        Tutorialdata=Tutorialdata,
        UserResponsible=UserResponsible,
        Status=Status,
        created_at=datetime.utcnow(),
    )
    
    return new_tutorial_request
#===============================================================================================#
#Notification
def create_notification(StudentNumber, ServiceType, UserResponsible, Status, Message, StudentId):
    # Assuming StudentNumber is either part of the form or can be retrieved from the database
    # using StudentId. The following line is a placeholder for actual retrieval logic.
    StudentNumber = get_student_number_by_id(StudentId)

    # Create a new Notification object
    new_notification = Notification(
        StudentNumber=StudentNumber,
        ServiceType=ServiceType,
        UserResponsible=UserResponsible,
        Status=Status,
        Message=Message,
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
def insert_Semester(form_data):
    SemesterName = form_data['SemesterName']
    
    new_Semester = Semester(
        SemesterName=SemesterName, 
    #yearId=yearId
    )
    
    return new_Semester

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









