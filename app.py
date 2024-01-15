import io
from operator import and_
from flask import Flask, abort, render_template, jsonify, redirect, request, flash, send_file, url_for, session
from flask_login import login_user
# from Api.v1.student.utils import get_student_class_data
from models import Class, ClassSubject, Course, CourseEnrolled, Metadata, Student, Faculty, StudentClassSubjectGrade, Subject, db, init_db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime, timezone #, timedelta, 
#from models import Services
#from models import init_db
from Api.v1.student.api_routes import create_services_application, fetchStudentDetails, get_student_number_by_id, getCurrentUser, getCurrentUserStudentNumber, student_api #getStudentClassSubjectGrade, #, update_student_profile #log_form_submission_to_file

import os
from dotenv import load_dotenv

from flask_jwt_extended import JWTManager

from decorators.auth_decorators import prevent_authenticated, role_required, student_required


load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
# SETUP YOUR POSTGRE DATABASE HERE
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}  
app.config['SESSION_COOKIE_MAX_SIZE'] = 4096  # Set to a value that works for your application
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_KEY_PREFIX'] = 'your_prefix'
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes (in seconds)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = os.getenv('SECRET_KEY')  # Replace 'your-secret-key' with an actual secret key
jwt = JWTManager(app)
init_db(app)

student_api_base_url = os.getenv("STUDENT_API_BASE_URL")
faculty_api_base_url = os.getenv("FACULTY_API_BASE_URL")

@app.context_processor
def custom_context_processor():
    authenticated = False
    if 'user_role' in session:
        authenticated = True
    return {'authenticated': authenticated}

#========================= LANDING PAGE ===================================

@app.route('/')
def index():
    session.permanent = True
    return render_template('main/home.html')

#===========================================================================
@app.route('/')
@prevent_authenticated
def home():
    session.permanent = True
    return render_template('main/home.html')

#=============================== LOGOUT FUNCTION ====================================

@app.route('/logout')
def logout():
    
    session.clear()
    return redirect(url_for('studentLogin'))  

@app.route('/logoutfaculty')
def logoutfaculty():

    session.clear()
    return redirect(url_for('faculty_portal'))

#========================================================================
#downloads
#=====================================================================================================

def upload_image():
    StudentNumber = request.form['StudentNumber']
    student = Student.query.filter_by(StudentNumber=StudentNumber).first()

    if student:
        image_file = request.files['image']
        if image_file:
            image_data = image_file.read()
            student.save_image(image_data)
            return 'Image uploaded successfully'
    
    return 'Error uploading image'

#=========================== LANDING PAGE SERVICES ROUTE ==============================================

@app.route('/services/foroverloadofsubject')
def overload():
    return render_template("/services/subject_overload.html")

@app.route('/services/addingofsubjects')
def adding():
    return render_template("/services/adding_of_subject.html")

@app.route('/services/changeofsubject/schedule')
def change():
    return render_template("/services/change_of_subject.html")

@app.route('/services/gradeentry')
def correction():
    return render_template("/services/grade_entry.html")

@app.route('/services/crossenrollment')
def cross_enrollment():
    return render_template("/services/cross_enrollment.html")

@app.route('/services/shifting')
def shifting():
    return render_template("/services/shifting.html")

@app.route('/services/manualenrollment')
def enrollment():
    return render_template("/services/manual_enrollment.html")

@app.route('/services/onlinepetitionofsubject')
def petition():
    return render_template("/services/petition.html")

@app.route('/services/requestfortutorialofsubjects')
def tutorial():
    return render_template("/services/tutorial.html")

@app.route('/services/certification')
def certification():
    return render_template("/services/certification.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

#==================================== LANDING PAGE ACADEMIC ROUTE ==============================================
@app.route('/academic/generalregulations')
def regulation():
    return render_template("/academic/regulation.html")

@app.route('/academic/codeofconduct')
def conduct():
    return render_template("/academic/conduct.html")

@app.route('/academic/academicprocedures')
def procedures():
    return render_template("/academic/procedures.html")

@app.route('/academic/codeofdiscipline')
def discipline():
    return render_template("/academic/discipline.html")

#========================================= STUDENT SERVICES ====================================================
@app.route('/student/addingsubject')
@student_required
def studentaddingsubject():
    current_user = getCurrentUser()
    student_id = current_user.StudentId

    current_date = datetime.now()
    
    result = db.session.query(
        Metadata.CourseId,
        Metadata.Year,
        Metadata.Semester,
        Metadata.Batch
    ).join(
        CourseEnrolled, Metadata.CourseId == CourseEnrolled.CourseId
    ).filter(
        and_(
            CourseEnrolled.StudentId == student_id,
            CourseEnrolled.DateEnrolled <= current_date,
    ) & CourseEnrolled.Status.in_([0, 1])
    ).order_by(
        Metadata.Year.desc(),  # Assuming you want the most recent entry first
        Metadata.Semester.desc(),
        CourseEnrolled.DateEnrolled.desc()
    ).first()

    courseID, year, semester, batch = result
    
    course = db.session.query(Course).filter(Course.CourseId == courseID).first()

    selections = (
        db.session.query(Subject)
        .join(ClassSubject, ClassSubject.SubjectId == Subject.SubjectId)
        .join(Class, Class.ClassId == ClassSubject.ClassId)
        .join(Metadata, Metadata.MetadataId == Class.MetadataId)
        .join(CourseEnrolled, CourseEnrolled.CourseId == Metadata.CourseId)
        .filter(CourseEnrolled.StudentId == student_id)
        .filter(Metadata.Semester == semester)  # Add the desired semester filter
        .filter(Metadata.Batch == batch)  # Add the desired semester filter
        .all()
    )

    # Extracting details of each Subject from the result
    selection_list = [selections.to_dict() for selections in selections]

    subjects = (
        db.session.query(Subject)
        .join(ClassSubject, Subject.SubjectId == ClassSubject.SubjectId)
        .join(StudentClassSubjectGrade, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
        .join(CourseEnrolled, CourseEnrolled.CourseId == ClassSubject.ClassId)
        .filter(CourseEnrolled.StudentId == student_id)
        .all()
    ) 

    # Extracting details of each Subject from the result
    subject_list = [subject.to_dict() for subject in subjects]

    return render_template("/student/addingsubject.html", selection_list=selection_list, subject_list=subject_list, course=course, student_api_base_url=student_api_base_url)


@app.route('/student/addingsubject/submitapplication', methods=['POST'])
@role_required('student')
def submitapplication():
    try:
        current_StudentId = session.get('user_id')
        current_FacultyId = request.form.get('facultyId')
        
        # Pass StudentId and FacultyId to the function
        new_service_application = create_services_application(request.form, request.files, current_StudentId, current_FacultyId)

        if new_service_application:
            flash('Service Request submitted successfully!', 'success')
            return redirect(url_for('studentaddingsubject'))  # Redirect to the appropriate route
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('/student/addingsubject.html')

#======================================== STUDENT DASHBOARD ====================================================
@app.route('/student/dashboard') 
@student_required
@role_required('student')
def student_dashboard():
    session.permanent=True
    return render_template('/student/dashboard.html')

#======================================== STUDENT PROFILE ======================================================

@app.route('/student/profile', methods=['GET'])
@student_required
@role_required('student') 
def studentprofile():
    return render_template('/student/profile.html', student_api_base_url=student_api_base_url)

@app.route('/student/profile/updated', methods=['GET', 'POST']) 
def student_update_profile():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        
        email = request.form.get('Email')
        mobile_number = request.form.get('MobileNumber')
        address = request.form.get('address')
        user_id = getCurrentUser()

        if isinstance(user_id, Student):
            user_id = user_id.StudentId

        student = Student.query.get(user_id)

        if student:
            try:
                student.Email = email
                student.MobileNumber = mobile_number
                student.address = address

                db.session.commit()
                flash('Profile Updated Successfully!', category='success')
                return redirect(url_for('studentprofile'))
            except Exception as e:
                # Handle the specific exception or log the error
                flash(f'Error updating profile: {str(e)}', category='error')
                db.session.rollback()  # Rollback changes in case of an error
        else:
            flash('Student not found. Please try again!', category='error')

    return render_template('/student/profile.html')


@app.route('/student/addingsubjects', methods=['GET', 'POST'])
@role_required('student')
def student_adding_subjects():
    if request.method == 'POST':
        email = request.form.get('Email')
        mobile_number = request.form.get('MobileNumber')
        address = request.form.get('address')
        user_id = getCurrentUser()
        
    
    current_user = getCurrentUser()
    student_id = current_user.StudentId

    current_date = datetime.now()

    # Join tables to get the current semester of a student
    result = db.session.query(
        Metadata.CourseId,
        Metadata.Year,
        Metadata.Semester,
        Metadata.Batch
    ).join(
        CourseEnrolled, Metadata.CourseId == CourseEnrolled.CourseId
    ).filter(
        and_(
            CourseEnrolled.StudentId == student_id,
            CourseEnrolled.DateEnrolled <= current_date,
    ) & CourseEnrolled.Status.in_([0, 1])
    ).order_by(
        Metadata.Year.desc(),  # Assuming you want the most recent entry first
        Metadata.Semester.desc(),
        CourseEnrolled.DateEnrolled.desc()
    ).first()

    courseID, year, semester, batch = result
    
    course = db.session.query(Course).filter(Course.CourseId == courseID).first()
    print(course.CourseCode)

    subjects = (
        db.session.query(Subject)
        .join(ClassSubject, ClassSubject.SubjectId == Subject.SubjectId)
        .join(Class, Class.ClassId == ClassSubject.ClassId)
        .join(Metadata, Metadata.MetadataId == Class.MetadataId)
        .join(CourseEnrolled, CourseEnrolled.CourseId == Metadata.CourseId)
        .filter(CourseEnrolled.StudentId == student_id)
        .filter(Metadata.Semester == semester)  # Add the desired semester filter
        .filter(Metadata.Batch == batch)  # Add the desired semester filter
        .all()
    )

    # Extracting details of each Subject from the result
    subject_details = [subject.to_dict() for subject in subjects]


    return render_template('student/addingsubjects.html', subject_details=subject_details, course=course)
    # else:
    #     return jsonify(message="No class subject data available"), 400

@app.route('/student/certification', methods=['GET'])
def cetification():
    return render_template('student/certification.html', student_api_base_url=student_api_base_url)

@app.route('/student/changeofsubject', methods=['GET'])
def changeofsubject():
    current_user_id = session.get('user_id')
    current_year = request.args.get('year', type=int) or datetime.now().year
    current_semester = request.args.get('semester', type=int) # You need to define how to determine the current semester

    results = api_student_class_subjects(current_user_id, current_year, current_semester)
    return jsonify([dict(row) for row in results])
    return render_template('student/changeofsubject.html')


#==================================== STUDENT CHANGE PASSWORD ===========================================================

@app.route('/student/changepassword')
def studentpassword():
    return render_template('/student/changepassword.html')

# Assuming you have a function `check_password_requirements` to check password requirements
def check_password_requirements(password):
    # Check if the password meets the specified requirements
    length_requirement = len(password) >= 8
    number_requirement = any(char.isdigit() for char in password)
    lowercase_requirement = any(char.islower() for char in password)
    special_symbol_requirement = any(char.isascii() and not char.isalnum() for char in password)
    uppercase_requirement = any(char.isupper() for char in password)

    return all([length_requirement, number_requirement, lowercase_requirement, special_symbol_requirement, uppercase_requirement])

@app.route('/student/changepassword', methods=['GET', 'POST'])
def student_change_password():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')

        user_id = getCurrentUser()

        if isinstance(user_id, Student):
            user_id = user_id.StudentId

        student = Student.query.get(user_id)

        # Check if the current password matches the one stored in the database
        if not check_password_hash(student.Password, current_password):
            flash('Incorrect current password. Please try again.', category='error')
            return redirect(url_for('student_change_password'))

        # Check if the new and confirm passwords match
        if new_password != confirm_password:
            flash('New and confirm password do not match. Please try again.', category='error')
            return redirect(url_for('student_change_password'))

        # Check if the new password meets the requirements
        if not check_password_requirements(new_password):
            flash('Password must meet the specified requirements. Please try again.', category='error')
            return redirect(url_for('student_change_password'))

        # Update the user's password in the database
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        student.Password = hashed_password
        db.session.commit()

        flash('Password changed successfully!', category='success')
        return redirect(url_for('student_change_password'))

    return render_template('student/change_password.html')


#=====================================================================================================================#
# ALL STUDENT ROUTES HERE
@app.route('/student')
@prevent_authenticated
def studentLogin():
    session.permanent = True
    return render_template("student/login.html")

#foroverload
@app.route('/student/login_for_overload')
@prevent_authenticated
def portal_overload():
    session.permanent = True
    return render_template('student/login_for_overload.html')

#certification
@app.route('/student/login_certification')
@prevent_authenticated
def portal_certification():
    session.permanent = True
    return render_template('student/login_certification.html')

#changesubsched
@app.route('/student/login_changesubsched')
@prevent_authenticated
def portal_changesubsched():
    session.permanent = True
    return render_template('student/login_changesubsched.html')

#enrollment
@app.route('/student/login_manualenroll')
@prevent_authenticated
def portal_enrollment():
    session.permanent = True
    return render_template('student/login_manualenroll.html')

#addsubjects
@app.route('/student/login_addsubjects')
@prevent_authenticated
def portal_addingofsubjects():
    session.permanent = True
    return render_template('student/login_addsubjects.html')


#requestfortutorialofsubjects
@app.route('/student/login_tutorial')
@prevent_authenticated
def portal_tutorial():
    session.permanent = True
    return render_template('student/login_tutorial.html')

#shifting
@app.route('/student/login_shifting')
@prevent_authenticated
def portal_shifting():
    session.permanent = True
    return render_template('student/login_shifting.html')

#petition onlinepetitionofsubject
@app.route('/student/login_petition')
@prevent_authenticated
def portal_petition():
    session.permanent = True
    return render_template('student/login_petition.html')

#gradeentry
@app.route('/student/login_gradeentry')
@prevent_authenticated
def portal_gradeentry():
    session.permanent = True
    return render_template('student/login_gradeentry.html')

#crossenrollment
@app.route('/student/login_crossenrollment')
@prevent_authenticated
def portal_crossenrollment():
    session.permanent = True
    return render_template('student/login_crossenrollment.html')

#=======================================================#

# Function to fetch student details by student ID
def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        return None

#===========================================================#
#Student directly Services

# Overload subjects function for student
@app.route('/student/portal_overload')
def student_portal_overload():
    session.permanent = True
    if is_user_logged_in_overload():
        return render_template('student/overload.html')
    # Overload subjects function for student

def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_overload'))

# Function to check if the user is logged in
def is_user_logged_in_overload():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_overload')
def redirect_based_on_login_overload():
    if is_user_logged_in_overload():
        return redirect(url_for('student_portal_overload'))
    else:
        return redirect(url_for('portal_overload'))

#================================================================
# Certification function for student
@app.route('/student/portal_certification')
def student_portal_certification():
    session.permanent = True
    if is_user_logged_in_certification():
        return render_template('student/certification.html')
    
def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_certification'))

# Function to check if the user is logged in
def is_user_logged_in_certification():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_certification')
def redirect_based_on_login_certification():
    if is_user_logged_in_certification():
        return redirect(url_for('student_portal_certification'))
    else:
        return redirect(url_for('portal_certification'))
#========================================================================
# Change of subject or sched function for student
@app.route('/student/portal_changeofsubject')
def student_portal_changesubsched():
    session.permanent = True

    if is_user_logged_in_changesubsched():
        return render_template('student/changesofsubject.html')
       # Redirect to the login page if not logged in
    return redirect(url_for('portal_changesubsched'))

    
def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_changesubsched'))

# Function to check if the user is logged in
def is_user_logged_in_changesubsched():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_changesubsched')
def redirect_based_on_login_changesubsched():
    if is_user_logged_in_changesubsched():
        return redirect(url_for('student_portal_changesubsched'))
    else:
        return redirect(url_for('portal_changesubsched'))
    
#========================================================================
# Enrollment function for student
@app.route('/student/portal_manualenrollment')
def student_portal_enrollment():
    session.permanent = True
    if is_user_logged_in_enrollment():
        return render_template('student/manual_enrollment.html')

def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_enrollment'))

# Function to check if the user is logged in
def is_user_logged_in_enrollment():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_enrollment')
def redirect_based_on_login_enrollment():
    if is_user_logged_in_enrollment():
        return redirect(url_for('student_portal_enrollment'))
    else:
        return redirect(url_for('portal_enrollment'))

#========================================================================

# addingsubject subjects function for student
@app.route('/student/portal_addingsubject')
def student_portal_addingofsubjects():
    session.permanent = True
    # Use the common login check
    if is_user_logged_in_addingofsubjects():
        return render_template("student/addingsubject.html")
    
    return redirect(url_for('portal_addingofsubjects'))

def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_addingofsubjects'))


# Function to check if the user is logged in
def is_user_logged_in_addingofsubjects():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None


# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_addingofsubjects')
def redirect_based_on_login_addingofsubjects():
    if is_user_logged_in_addingofsubjects():
        return redirect(url_for('student_portal_addingofsubjects'))
    else:
        return redirect(url_for('portal_addingofsubjects'))


#================================================================
# shifting function for student
@app.route('/student/portal_shifting')
def student_portal_shifting():
    session.permanent = True
    if is_user_logged_in_shifting():
        return render_template('student/shifting.html')
    
def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_shifting'))

# Function to check if the user is logged in
def is_user_logged_in_shifting():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_shifting')
def redirect_based_on_login_shifting():
    if is_user_logged_in_shifting():
        return redirect(url_for('student_portal_shifting'))
    else:
        return redirect(url_for('portal_shifting'))


#========================================================================

# tutorial subjects function for student
@app.route('/student/portal_tutorial')
def student_portal_tutorial():
    session.permanent = True
    if is_user_logged_in_tutorial():
        return render_template('student/tutorial.html')
    
def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_tutorial'))

# Function to check if the user is logged in
def is_user_logged_in_tutorial():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_tutorial')
def redirect_based_on_login_tutorial():
    if is_user_logged_in_tutorial():
        return redirect(url_for('student_portal_tutorial'))
    else:
        return redirect(url_for('portal_tutorial'))

#================================================================
# online petition subjects function for student
@app.route('/student/onlinepetitionofsubject')
def student_portal_petition():
    session.permanent = True
    if is_user_logged_in_petition():
        return render_template('student/petition.html')
    
def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_petition'))

# Function to check if the user is logged in
def is_user_logged_in_petition():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_petition')
def redirect_based_on_login_petition():
    if is_user_logged_in_petition():
        return redirect(url_for('student_portal_petition'))
    else:
        return redirect(url_for('portal_petition'))
    
#================================================================
# gradeentry function for student
@app.route('/student/portal_correction')
def student_portal_gradeentry():
    session.permanent = True
    if is_user_logged_in_gradeentry():
        return render_template('student/correction.html')

def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_gradeentry'))

# Function to check if the user is logged in
def is_user_logged_in_gradeentry():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_gradeentry')
def redirect_based_on_login_gradeentry():
    if is_user_logged_in_gradeentry():
        return redirect(url_for('student_portal_gradeentry'))
    else:
        return redirect(url_for('portal_gradeentry'))

#================================================================
# gradeentry function for student
@app.route('/student/portal_crossenrollment')
def student_portal_crossenrollment():
    session.permanent = True
    if is_user_logged_in_crossenrollment():
        return render_template('student/crossenrollment.html')
    # Function to fetch student details by student ID
def get_student_details(StudentId):
    student = Student.query.get(StudentId)

    if student:
        student_details = {
            'StudentNumber': student.StudentNumber,
            'Name': student.Name,
            'Gender': student.Gender,
            'Email': student.Email,
            'address': student.address,
            'DateofBirth': student.DateofBirth,
            'PlaceofBirth': student.PlaceofBirth,
            'MobileNumber': student.MobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_crossenrollment'))

# Function to check if the user is logged in
def is_user_logged_in_crossenrollment():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("StudentId") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_crossenrollment')
def redirect_based_on_login_crossenrollment():
    if is_user_logged_in_gradeentry():
        return redirect(url_for('student_portal_crossenrollment'))
    else:
        return redirect(url_for('portal_crossenrollment'))

# ========================================================================
# Register the API blueprint
"""app.register_blueprint(admin_api, url_prefix='/api/v1/admin')
app.register_blueprint(faculty_api, url_prefix=faculty_api_base_url)"""
app.register_blueprint(student_api, url_prefix=student_api_base_url)

# ========================================================================
# TESTING
@app.route('/student/json', methods=['GET'])
def get_student_json():
    student = Student.query.all()

    student_list = []
    for student in student:
        student_data = {
            'StudentId': student.StudentId,
            'Name': student.Name,
            'Email': student.Email,
            'Password': student.Password
            # Add other fields as needed
        }
        student_list.append(student_data)

    return jsonify(student_list)

@app.route('/page_not_found')  # Define an actual route
def page_not_found():
    return handle_404_error(None)


@app.errorhandler(404)
def handle_404_error(e):
    return render_template('404.html'), 404



# ... other route registrations ...
# ========================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0')


"""if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)
"""
# ... other route registrations ...
# ========================================================================