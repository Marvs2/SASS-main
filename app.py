import io
from flask import Flask, abort, render_template, jsonify, redirect, request, flash, send_file, url_for, session
from flask_login import login_user
"""from models import CertificationRequest, ChangeOfSubjects, CrossEnrollment, Faculty, GradeEntry, ManualEnrollment, Notification, OverloadApplication, PetitionRequest, ShiftingApplication, Subject, TutorialRequest, db, AddSubjects, init_db, Student"""
from models import Student, Faculty, Subject, db, init_db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime, timezone #, timedelta, 
#from models import Services
#from models import init_db
from Api.v1.student.api_routes import create_crossenrollment_form, create_overload_application,  fetchStudentDetails, get_student_number_by_id, getCurrentUser, getCurrentUserStudentNumber, student_api#, update_student_profile #log_form_submission_to_file

"""from Api.v1.student.api_routes import create_addsubjects_application, create_certification_request, create_changesubjects_application, create_crossenrollment_form, create_gradeentry_application, create_manualenrollment_form, create_notification, create_overload_application, create_petitionrequest_form, create_shifting_application, create_tutorial_request, fetchStudentDetails, get_student_number_by_id, getCurrentUser, getCurrentUserStudentNumber, student_api#, update_student_profile #log_form_submission_to_file"""
"""from Api.v1.faculty.api_routes import faculty_api, get_current_faculty_user
from Api.v1.admin.api_routes import admin_api, create_student"""
# Assuming your Flask app is created as 'app'

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

#======================================== STUDENT DASHBOARD ====================================================
@app.route('/student/dashboard') 
@role_required('student')
def student_dashboard():
    session.permanent=True
    return render_template('/student/dashboard.html')

#======================================== STUDENT PROFILE ======================================================

@app.route('/student/profile')
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


#======================================== STUDENT TRANSACTION HISTORY ===================================================
@app.route('/student/history', methods=['GET'])
@role_required('student')
def student_history():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    services_data = {}
"""
if student:
        # Fetch AddSubjects based on the StudentId foreign key
        addsubjects = AddSubjects.query.filter_by(StudentId=student.StudentId).all()
        services_data['addsubjects_list'] = [subject.to_dict() for subject in addsubjects]

        # Fetch ChangeOfSubjects based on the StudentId foreign key
        changesubjects = ChangeOfSubjects.query.filter_by(StudentId=student.StudentId).all()
        services_data['changesubjects_list'] = [subject.to_dict() for subject in changesubjects]

        # Fetch ManualEnrollment based on the StudentId foreign key
        manual_enrollments = ManualEnrollment.query.filter_by(StudentId=student.StudentId).all()
        services_data['manual_enrollments_list'] = [subject.to_dict() for subject in manual_enrollments]

        # Fetch CertificationRequest based on the StudentId foreign key
        certification_request = CertificationRequest.query.filter_by(StudentId=student.StudentId).all()
        services_data['certification_request_list'] = [subject.to_dict() for subject in certification_request]

        # Fetch GradeEntry based on the StudentId foreign key
        grade_entry = GradeEntry.query.filter_by(StudentId=student.StudentId).all()
        services_data['grade_entry_list'] = [subject.to_dict() for subject in grade_entry]

        # Fetch CrossEnrollment based on the StudentId foreign key
        cross_enrollment = CrossEnrollment.query.filter_by(StudentId=student.StudentId).all()
        services_data['cross_enrollment_list'] = [subject.to_dict() for subject in cross_enrollment]

        # Fetch PetitionRequest based on the StudentId foreign key
        petition_requests = PetitionRequest.query.filter_by(StudentId=student.StudentId).all()
        services_data['petition_requests_list'] = [subject.to_dict() for subject in petition_requests]

        # Fetch ShiftingApplication based on the StudentId foreign key
        shifting_applications = ShiftingApplication.query.filter_by(StudentId=student.StudentId).all()
        services_data['shifting_applications_list'] = [subject.to_dict() for subject in shifting_applications]

        # Fetch OverloadApplication based on the StudentId foreign key
        overload_applications = OverloadApplication.query.filter_by(StudentId=student.StudentId).all()
        services_data['overload_applications_list'] = [subject.to_dict() for subject in overload_applications]

        # Fetch TutorialRequest based on the StudentId foreign key
        tutorial_requests = TutorialRequest.query.filter_by(StudentId=student.StudentId).all()
        services_data['tutorial_requests_list'] = [subject.to_dict() for subject in tutorial_requests]

    return render_template("/student/history.html", services_data=services_data)"""
#=======================================For Notification=======================================#

"""@app.route('/student/notifications' , methods=['GET'])
@role_required('student')
def show_notifications():
    user_id = session.get('user_id')

    student = Student.query.get(user_id)
    if student:
        notifications = Notification.query.filter_by(StudentId=student.StudentId).order_by(Notification.created_at.desc()).all()
    else:
        notifications = []

    return render_template("/student/notification.html", notifications=notifications)"""

#=======================================For Setting=======================================#
@app.route('/student/setting')
def studentsetting():
    return render_template('/student/setting.html')
# Assuming you have the role_required decorator implemented

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



"""# Endpoint to Fetch Programs
@app.route('/programs', methods=['GET'])
def get_programs():
    programs = Program.query.all()
    return jsonify([program.to_dict() for program in programs])


# Endpoint to Fetch Year Levels based on ProgramID
@app.route('/year-levels/<int:program_id>', methods=['GET'])
def get_year_levels(program_id):
    year_levels = YearLevel.query.filter_by(programId=program_id).all()
    return jsonify([year_level.to_dict() for year_level in year_levels])


# Endpoint to Fetch Semesters based on YearLevelID
@app.route('/semesters/<int:year_level_id>', methods=['GET'])
def get_semesters(year_level_id):
    semesters = Semester.query.filter_by(yearId=year_level_id).all()
    return jsonify([semester.to_dict() for semester in semesters])


# Endpoint to Fetch Subjects based on YearLevelID and SemesterID
@app.route('/subjects/<int:year_level_id>/<int:semester_id>', methods=['GET'])
def get_subjects(year_level_id, semester_id):
    subjects = CourseSub.query.filter_by(yearId=year_level_id, semesterId=semester_id).all()
    return jsonify([subject.to_dict() for subject in subjects])"""
    
#================================= OVERLOAD OF SUBJECT =============================================================
"""@app.route('/student/overload') 
def studentoverload():
    return render_template("/student/overload.html", student_api_base_url=student_api_base_url)

@app.route('/student/overload/submitted', methods=['POST'])
@role_required('student')
def submit_overload_application():
    try:
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_overload_application = create_overload_application(request.form, request.files, current_StudentId)

        if new_overload_application and current_StudentNumber:
            db.session.add(new_overload_application)
            db.session.commit()

                # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Overload Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your overload application request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()
        
                # Ensure student_api_base_url is defined and accessible
            flash('Overload application submitted successfully!', 'success')
            return redirect(url_for('studentoverload'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/overload.html')
  # Adjust the template as needed

@app.route('/student/viewoverload', methods=['GET'])
@role_required('student')
def viewoverload():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    overload_applications_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        overload_applications = OverloadApplication.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        overload_applications_list = [subject.to_dict() for subject in overload_applications]

    return render_template("/student/viewoverload.html", overload_applications_list=overload_applications_list)"""
#=======================================================================#
#================== ADDING OF SUBJECT ==================================#
"""
@app.route('/student/addingsubject')
def studentaddingsubject():
    subjects = Subject.query.all()
    return render_template("/student/addingsubject.html", student_api_base_url=student_api_base_url, subjects=subjects)

@app.route('/student/addingsubject/added', methods=['POST'])
@role_required('student')
def add_subjects():
    try: 
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_addsubjects_application = create_addsubjects_application(request.form, request.files, current_StudentId)
        
        if new_addsubjects_application and current_StudentNumber:
            db.session.add(new_addsubjects_application)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Adding Subjects Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your add subjects request has been sent.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Add subjects created Successfully!', 'success')
            return redirect(url_for('studentaddingsubject'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/addingsubject.html') 

@app.route('/student/viewaddsubject', methods=['GET'])
@role_required('student')
def viewaddsubject():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    addsubjects_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        addsubjects = AddSubjects.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        addsubjects_list = [subject.to_dict() for subject in addsubjects]

    return render_template("/student/viewaddsubject.html", addsubjects_list=addsubjects_list)

@app.route('/student/view_subject_file/<int:subject_ID>')
def view_subject_file(subject_ID):
    addsubject = AddSubjects.query.get(subject_ID)

    if addsubject and addsubject.file_data:
        file_extension = get_file_extension(addsubject.file_name)
        mimetype = get_mimetype(file_extension)

        return send_file(
            io.BytesIO(addsubject.file_data),
            as_attachment=False,
            mimetype=mimetype
        )
    else:
        abort(404)  # Subject or file not found

def get_file_extension(file_name):
    return file_name.rsplit('.', 1)[1].lower()

def get_mimetype(file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Note: Changed 'docs' to 'docx' for the correct MIME type
        # Add more file types as needed
    }

    return mimetypes.get(file_extension, 'application/octet-stream')"""

#============================== CHANGE OF SCHEDULE/SUBJECT ===============================================#
"""@app.route('/student/changeofsubject')
def studentchange():
    return render_template("/student/changeofsubject.html", student_api_base_url=student_api_base_url)

@app.route('/student/changeofsubject/added', methods=['POST'])
@role_required('student')
def change_of_subjects():
    try: 
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_changesubjects_application = create_changesubjects_application(request.form, request.files, current_StudentId)
        
        if new_changesubjects_application and current_StudentNumber:
            db.session.add(new_changesubjects_application)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Change Subject Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your Change Subject request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Change of subjects created Successfully!', 'success')
            return redirect(url_for('studentchange'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/changeofsubject.html')


@app.route('/student/viewchange', methods=['GET'])
@role_required('student')
def viewchange():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    changesubjects_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        changesubjects = ChangeOfSubjects.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        changesubjects_list = [subject.to_dict() for subject in changesubjects]

    return render_template("/student/viewchange.html", changesubjects_list=changesubjects_list)
#view_change_file
@app.route('/student/view_change_file/<int:Changesubject_ID>')
def view_change_file(Changesubject_ID):
    changesubjects = ChangeOfSubjects.query.get(Changesubject_ID)

    if changesubjects and changesubjects.ace_form_data:
        file_extension = get_file_extension(changesubjects.ace_form_filename)
        mimetype = get_mimetype(file_extension)

        return send_file(
            io.BytesIO(changesubjects.ace_form_data),
            as_attachment=False,
            mimetype=mimetype
        )
    else:
        abort(404)  # Change of subjects application or file not found

def get_file_extension(ace_form_filename):
    return ace_form_filename.rsplit('.', 1)[1].lower()

def get_mimetype(file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Note: Changed 'docs' to 'docx' for the correct MIME type
        # Add more file types as needed
    }

    return mimetypes.get(file_extension, 'application/octet-stream')"""

#========================== CORRECTION OF GRADE ENTRY ================================================#
"""
@app.route('/student/correction')
def studentcorrection():
    return render_template("/student/correction.html", student_api_base_url=student_api_base_url)

@app.route('/student/correction/submit', methods=['POST'])
@role_required('student')
def submit_grade_correction():
    try: 
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_gradeentry_application = create_gradeentry_application(request.form, request.files, current_StudentId)
        
        if new_gradeentry_application and current_StudentNumber:
            db.session.add(new_gradeentry_application)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Grade Correction Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your Grade Correction request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Grade entry sent Successfully!', 'success')
            return redirect(url_for('studentcorrection'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/correction.html')

@app.route('/student/viewcorrection', methods=['GET'])
@role_required('student')
def viewcorrection():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    grade_entry_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        grade_entry = GradeEntry.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        grade_entry_list = [subject.to_dict() for subject in grade_entry]

    return render_template("/student/viewcorrection.html", grade_entry_list=grade_entry_list)"""

#viewfile for correction
"""@app.route('/student/view_completion_form/<int:grade_entry_id>')
def view_completion_form(grade_entry_id):
    grade_entry = GradeEntry.query.get(grade_entry_id)

    if grade_entry and grade_entry.completion_form_data:
        completion_form_extension = get_completion_form_extension(grade_entry.completion_form_filename)
        mimetype = get_mimetype(completion_form_extension)

        return send_file(
            io.BytesIO(grade_entry.completion_form_data),
            as_attachment=False,
            mimetype=mimetype
        )
    else:
        abort(404)  # File not found"""

"""@app.route('/student/view_completion_form/<int:grade_entry_id>')
def view_completion_form(grade_entry_id):
    grade_entry = GradeEntry.query.get(grade_entry_id)

    if grade_entry and grade_entry.completion_form_data:
        completion_form_extension = get_completion_form_extension(grade_entry.completion_form_filename)
        mimetype = get_mimetype(completion_form_extension)

        return send_file(
            io.BytesIO(grade_entry.completion_form_data),
            as_attachment=False,  # Changed to False
            mimetype=mimetype
        )
    else:
        abort(404)  # File not found



@app.route('/student/view_class_record/<int:grade_entry_id>')
def view_class_record(grade_entry_id):
    grade_entry = GradeEntry.query.get(grade_entry_id)

    if grade_entry and grade_entry.class_record_data:
        class_extension = get_class_extension(grade_entry.class_record_filename)
        mimetype = get_mimetype(class_extension)

        return send_file(
            io.BytesIO(grade_entry.class_record_data),
            as_attachment=False,
            mimetype=mimetype
        )
    else:
        abort(404)

@app.route('/student/view_affidavit/<int:grade_entry_id>')
def view_affidavit(grade_entry_id):
    grade_entry = GradeEntry.query.get(grade_entry_id)

    if grade_entry and grade_entry.affidavit_data:
        affidavit_extension = get_affidavit_extension(grade_entry.affidavit_filename)
        mimetype = get_mimetype(affidavit_extension)

        return send_file(
            io.BytesIO(grade_entry.affidavit_data),
            as_attachment=False,
            mimetype=mimetype
        )
    else:
        abort(404)"""

#====================================== CROSS ENROLLMENT =========================================================
"""
@app.route('/student/crossenrollment')
def studentenrollment():
    return render_template("/student/crossenrollment.html", student_api_base_url=student_api_base_url)

@app.route('/student/crossenrollment/submitted', methods=['POST'])
@role_required('student') 
def submit_cross_enrollment():

    try:
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_cross_enrollment = create_crossenrollment_form(request.form, request.files, current_StudentId)
        
        if new_cross_enrollment and current_StudentNumber:
            db.session.add(new_cross_enrollment)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Cross Enrollment Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your Cross Enrollment request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Cross-Enrollment created successfully!', 'success')
            return redirect(url_for('studentenrollment'))  
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/crossenrollment.html')

@app.route('/student/viewcrossenrollment', methods=['GET'])
@role_required('student')
def viewcrossenrollment():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    cross_enrollments_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        cross_enrollments = CrossEnrollment.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        cross_enrollments_list = [subject.to_dict() for subject in cross_enrollments]

    return render_template("/student/viewcrossenrollment.html", cross_enrollments_list=cross_enrollments_list)
"""
#================================== APPLICATION FOR SHIFTING ================================================
"""@app.route('/student/shifting')
def studentshifting():
    return render_template("/student/shifting.html", student_api_base_url=student_api_base_url)

@app.route('/student/shifting/submit', methods=['POST'])
@role_required('student')
def submit_shifting():
    try: 
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_shifting_application = create_shifting_application(request.form, request.files, current_StudentId)
        
        if new_shifting_application and current_StudentNumber:
            db.session.add(new_shifting_application)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Shifting Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your Shifting request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Shifting has been created Successfully!', 'success')
            return redirect(url_for('studentshifting'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/shifting.html')  

#=========================================== MANUAL ENROLLMENT ========================================================
@app.route('/student/manualenrollment')#
def studentmanualenrollment():
    return render_template("/student/manualenrollment.html", student_api_base_url=student_api_base_url)#

# Manual Enrollment Route
@app.route('/student/manualenrollment/submitmanual', methods=['POST'])
@role_required('student')
def submitmanualenrollment():
    try:
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_manual_enrollment = create_manualenrollment_form(request.form, request.files, current_StudentId)

        if new_manual_enrollment and current_StudentNumber:
            db.session.add(new_manual_enrollment)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Manual Enrollment Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your Manual EnrollmentManual Enrollment request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Manual Enrollment created successfully!', 'success')
            return redirect(url_for('studentmanualenrollment'))  # Redirect to the appropriate route
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/manualenrollment.html')

@app.route('/student/viewmanual', methods=['GET'])
@role_required('student')
def viewmanual():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    manual_enrollments_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        manual_enrollments = ManualEnrollment.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        manual_enrollments_list = [subject.to_dict() for subject in manual_enrollments]

    return render_template("/student/viewmanual.html", manual_enrollments_list=manual_enrollments_list)"""
#===================================== ONLINE PETITION OF SUBJECTS =====================================================

"""@app.route('/student/onlinepetitionofsubject')
def studentpetition():
    return render_template("/student/petition.html", student_api_base_url=student_api_base_url)

@app.route('/student/onlinepetitionofsubject/submit_petition', methods=['POST'])
@role_required('student')
def submit_petition():
    try:
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_petition_request = create_petitionrequest_form(request.form, current_StudentId)

        if new_petition_request and current_StudentNumber:
            db.session.add(new_petition_request)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Petition Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your Petition request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Petition Request submitted successfully!', 'success')
            return redirect(url_for('studentpetition'))  # Redirect to the appropriate route
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/petition.html')



@app.route('/student/viewpetition', methods=['GET'])
@role_required('student')
def viewpetition():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    petition_requests_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        petition_requests = PetitionRequest.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        petition_requests_list = [subject.to_dict() for subject in petition_requests]

    return render_template("/student/viewpetition.html", petition_requests_list=petition_requests_list)"""

#================================= ONLINE REQUEST FOR TUTORIAL ===================================================
"""
@app.route('/student/tutorial')#
def studenttutorial():
    return render_template("/student/tutorial.html", student_api_base_url=student_api_base_url)#

@app.route('/student/tutorial/submit', methods=['POST'])
@role_required('student')
def submit_tutorial_request():
    try: 
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId)
        new_tutorial_request = create_tutorial_request(request.form, request.files, current_StudentId)
        
        if new_tutorial_request and current_StudentNumber:
            db.session.add(new_tutorial_request)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Tutorial Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your tutorial request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Tutorial request and notification have been created successfully!', 'success')
            return redirect(url_for('studenttutorial'))
        else:
            flash('Error: Student not found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/tutorial.html')"""

"""@app.route('/student/viewtutorial', methods=['GET'])
@role_required('student')
def viewtutorial():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    tutorial_requests_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        tutorial_requests = TutorialRequest.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        tutorial_requests_list = [subject.to_dict() for subject in tutorial_requests]

    return render_template("/student/viewtutorial.html", tutorial_requests_list=tutorial_requests_list)

@app.route('/student/view_tutorial_file/<int:tutorial_request_id>')
def view_tutorial_file(tutorial_request_id):
    tutorial_requests = TutorialRequest.query.get(tutorial_request_id)

    if tutorial_requests and tutorial_requests.file_data:
        tutorial_extension = get_tutorial_extension(tutorial_requests.file_filename)
        mimetype = get_mimetype(tutorial_extension)

        return send_file(
            io.BytesIO(tutorial_requests.file_data),
            as_attachment=False,
            mimetype=mimetype
        )
    else:
        abort(404)  # File not found
#======================================== REQUEST FOR CERTIFICATION ===========================================================
@app.route('/student/certification')
def studentcertification():
    return render_template("/student/certification.html", student_api_base_url=student_api_base_url)

@app.route('/student/certification/submit_certification_request', methods=['POST'])
@role_required('student')
def submit_certification_request():
    try:
        current_StudentId = session.get('user_id')
        current_StudentNumber = get_student_number_by_id(current_StudentId) 
        new_certification_request = create_certification_request(request.form, request.files, current_StudentId)

        if new_certification_request and current_StudentNumber:
            db.session.add(new_certification_request)
            db.session.commit()

            # Create a notification
            new_notification = create_notification(
                StudentNumber=current_StudentNumber,
                service_type="Certification Request",
                user_responsible=request.form.get('user_responsible'),
                status="Sent",
                message="Your certification request has been submitted.",
                StudentId=current_StudentId
            )
            db.session.add(new_notification)
            db.session.commit()

            flash('Certification Request submitted successfully!', 'success')
            return redirect(url_for('studentcertification')) 
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/certification.html')

    #certification
@app.route('/student/certification/get_certification_request_file/<int:certification_request_id>')
def get_certification_request_file(certification_request_id):
    return redirect(url_for('view_certification_request_file', certification_request_id=certification_request_id))

@app.route('/student/view_certification_request_file/<int:certification_request_id>')
def view_certification_request_file(certification_request_id):
    certification_request = CertificationRequest.query.get(certification_request_id)

    if certification_request and certification_request.request_form_data:
        certification_request_extension = get_certification_request_extension(certification_request.request_form_filename)
        return send_file(
            io.BytesIO(certification_request.request_form_data),
            mimetype=get_mimetype(certification_request_extension),
        )
    else:
        abort(404)  # Certification request or file not found
def get_certification_request_extension(request_form_filename):
    return request_form_filename.rsplit('.', 1)[1].lower()

def get_mimetype(certification_request_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(certification_request_extension, 'application/octet-stream')

# Repeat the above pattern for other file types/routes...
@app.route('/student/certification/view_certification_identification_file/<int:certification_request_id>')
def view_certification_identification_file(certification_request_id):
    certification_request = CertificationRequest.query.get(certification_request_id)

    if certification_request and certification_request.identification_card_data:
        identification_file_extension = get_identification_file_extension(certification_request.identification_card_filename)
        return send_file(
            io.BytesIO(certification_request.identification_card_data),
            mimetype=get_mimetype(identification_file_extension),
        )
    else:
        abort(404)  # Certification request or file not found

def get_identification_file_extension(identification_card_filename):
    return identification_card_filename.rsplit('.', 1)[1].lower()

def get_mimetype(identification_file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(identification_file_extension, 'application/octet-stream')"""

"""@app.route('/student/certification/view_certification_authorization_file/<int:certification_request_id>')
def view_certification_authorization_file(certification_request_id):
    certification_request = CertificationRequest.query.get(certification_request_id)

    if certification_request and certification_request.authorization_letter_data:
        authorization_file_extension = get_authorization_file_extension(certification_request.authorization_letter_filename)
        return send_file(
            io.BytesIO(certification_request.authorization_letter_data),
            mimetype=get_mimetype(authorization_file_extension),
        )
    else:
        abort(404)  # Certification request or file not found

def get_authorization_file_extension(authorization_letter_filename):
    return authorization_letter_filename.rsplit('.', 1)[1].lower()

def get_mimetype(authorization_file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'word': 'application/word',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(authorization_file_extension, 'application/octet-stream')"""
#===========================================================================================================================#

"""# View function to handle operations based on StudentId
@app.route('/students/<int:student_id>/subjects', methods=['GET'])
def get_student_subjects(student_id):
    # Assuming 'student_id' is passed as part of the route
    subjects = AddSubjects.query.filter_by(StudentId=student_id).all()

    if not subjects:
        return jsonify({'message': 'No subjects found for this student.'}), 404

    # Convert the AddSubjects objects to dictionaries
    subjects_list = [subject.to_dict() for subject in subjects]

    return jsonify({'subjects': subjects_list}), 200"""

#============================================================================================================================
"""
@app.route('/refresh_session', methods=['POST'])
def refresh_session():
    # Update the last activity timestamp
    session['last_activity'] = datetime.now(timezone.utc)
    return jsonify(success=True)

#======================View_Compilation=====================#
#===========================================================#

# ========================================================================
#SERVICES
@app.route('/faculty/overload')
def facultyoverload():
    overload_application = OverloadApplication.query.all()
    return render_template("/faculty/overload.html", overload_application=overload_application)  #overload_application in overload_application

@app.route('/faculty/adding')
def facultyadding():
    session['last_activity'] = datetime.now(timezone.utc)
    addsubjects = AddSubjects.query.all()
    return render_template("/faculty/adding.html", addsubjects=addsubjects) # addsubjects in addsubjects

@app.route('/faculty/change')
def facultychange():
    session['last_activity'] = datetime.now(timezone.utc)
    changesubjects = ChangeOfSubjects.query.all()
    return render_template("/faculty/change.html", changesubjects=changesubjects) #changesubjects in changesubjects

#gradeentry table
@app.route('/faculty/correction')
def facultycorrection():
    session['last_activity'] = datetime.now(timezone.utc) # none
    grade_entry = GradeEntry.query.all()
    return render_template("/faculty/correction.html", grade_entry=grade_entry) # for grade_entries in grade_entries

@app.route('/faculty/crossenrollment')
def facultycrossenrollment():
    session['last_activity'] = datetime.now(timezone.utc) # none
    cross_enrollments = CrossEnrollment.query.all()
    return render_template("/faculty/crossenrollment.html", cross_enrollments=cross_enrollments)

@app.route('/faculty/shifting')
def facultyshifting():
    session['last_activity'] = datetime.now(timezone.utc) # none
    shifting_applications = ShiftingApplication.query.all()
    return render_template("/faculty/shifting.html", shifting_applications=shifting_applications)

@app.route('/faculty/manualenrollment')
def facultyenrollment():
    session['last_activity'] = datetime.now(timezone.utc) # none
    manual_enrollments = ManualEnrollment.query.all()
    return render_template("/faculty/enrollment.html", manual_enrollments=manual_enrollments)

@app.route('/faculty/onlinepetitionofsubject')
def facultypetition():
    session['last_activity'] = datetime.now(timezone.utc) #none
    petition_requests = PetitionRequest.query.all()
    return render_template("/faculty/petition.html", petition_requests=petition_requests)

@app.route('/faculty/requestfortutorialofsubjects')
def faculty_view_tutorial():
    session['last_activity'] = datetime.now(timezone.utc) #none
    return render_template("/faculty/view_tutorial.html")

@app.route('/faculty/certification')
def facultycertification():
    session['last_activity'] = datetime.now(timezone.utc) #none
    certification_request = CertificationRequest.query.all()
    return render_template("/faculty/certification.html", certification_request=certification_request)

@app.route('/faculty/tutorial')
def facultytutorial():
    session['last_activity'] = datetime.now(timezone.utc) #none
    tutorial_requests = TutorialRequest.query.all()
    return render_template("/faculty/tutorial.html", tutorial_requests=tutorial_requests)
"""
#=======================================================================#

#===================================================TIMER=============================================================#
# Middleware to check for inactivity and redirect to login if needed
"""@app.before_request
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

#========================================================

@app.route('/student/service_service_form')#
def stud_services():
    return render_template("/student/service_request_form.html")#

"""@app.route('/student/submit_service_form/request', methods=['POST'])
def submit_services_request():
    if request.method == 'POST':
        service_type = request.form.get('serviceType')
        StudentId = request.form.get('StudentId')
        name = request.form.get('name')

        # Add other fields based on your requirements

        # Create a new Services object
        new_service = Services(
            service_type=service_type,
            StudentId=StudentId,
            name=name,
            created_at=datetime.utcnow(),
            # Add other fields based on your requirements
        )

        # Save the new service request to the database
        db.session.add(new_service)
        db.session.commit()

        # Return a response (you can customize this based on your needs)
        flash('Service request submitted successfully')

    return redirect(url_for('stud_services'))"""

#======================View_Compilation_Faculty=====================#
#===========================================================#

#NEEDED !!!!!!!!!!!!!!!!! for change the status of the services put by the student
#SERVICES

#=====================================================================
#=====================================================================
#Adding - Faculty

"""@app.route('/update-adding-service-status/<int:add_subject_id>', methods=['POST'])
def update_adding_service_status(add_subject_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    add_subject = AddSubjects.query.get_or_404(add_subject_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        add_subject.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Add subject status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultyadding'))

# adding.html page
@app.route('/faculty/adding/get_subject_file/<int:subject_ID>')
def get_subject_file(subject_ID):
    return redirect(url_for('download_subject_file', subject_ID=subject_ID))

#download the file in the view page
@app.route('/faculty/download_subject_file/<int:subject_ID>')
def download_subject_file(subject_ID):
    addsubject = AddSubjects.query.get(subject_ID)

    if addsubject and addsubject.file_data:
        file_extension = get_file_extension(addsubject.file_name)
        download_name = f'subject_{subject_ID}.{file_extension}'

        return send_file(
            io.BytesIO(addsubject.file_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(file_extension),
        )
    else:
        abort(404)  # Subject or file not found

def get_file_extension(file_name):
    return file_name.rsplit('.', 1)[1].lower()

def get_mimetype(file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(file_extension, 'application/octet-stream')"""
#=====================================================================
#changesubjects

@app.route('/update-change-service-status/<int:Changesubject_ID>', methods=['POST'])
def update_change_service_status(Changesubject_ID):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
#    changesubjects = ChangeOfSubjects.query.get_or_404(Changesubject_ID)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
  #      changesubjects.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Change status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultychange'))

# Redirect to download change of change.html
@app.route('/faculty/change/get_change_file/<int:Changesubject_ID>')
def get_change_file(Changesubject_ID):
    return redirect(url_for('download_change_file', Changesubject_ID=Changesubject_ID))

# Download change of subjects file
@app.route('/faculty/download_change_file/<int:Changesubject_ID>')
def download_change_file(Changesubject_ID):
 #   changesubjects = ChangeOfSubjects.query.get(Changesubject_ID)

 """   if changesubjects and changesubjects.ace_form_data:
        file_extension = get_file_extension(changesubjects.ace_form_filename)
        download_name = f'change_subject_{Changesubject_ID}.{file_extension}'

        return send_file(
            io.BytesIO(changesubjects.ace_form_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(file_extension),
        )
    else:
        abort(404)  # Change of subjects application or file not found

def get_file_extension(ace_form_filename):
    return ace_form_filename.rsplit('.', 1)[1].lower()

def get_mimetype(file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(file_extension, 'application/octet-stream')"""
#=====================================================================
#gradeentry table
"""@app.route('/update-correction-service-status/<int:grade_entry_id>', methods=['POST'])
def update_correction_service_status(grade_entry_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    grade_entry = GradeEntry.query.get_or_404(grade_entry_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        grade_entry.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Correction status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultycorrection'))

#correction
# Route to handle download requests for grade entry files
@app.route('/faculty/correction/get_completion_file/<int:grade_entry_id>')
def get_completion_file(grade_entry_id):
    return redirect(url_for('download_completion_form', grade_entry_id=grade_entry_id))"""

"""@app.route('/faculty/download_completion_form/<int:grade_entry_id>')
def download_completion_form(grade_entry_id):
    grade_entry = GradeEntry.query.get(grade_entry_id)

    if grade_entry and grade_entry.completion_form_data:
        completion_form_extension = get_completion_form_extension(grade_entry.completion_form_filename)
        download_name = f'completion_form_{grade_entry_id}.{completion_form_extension}'

        return send_file(
            io.BytesIO(grade_entry.completion_form_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(completion_form_extension)
        )
    else:
        abort(404)  # File not found

# Route to download a specific file of a grade entry
def get_completion_form_extension(completion_form_filename):
    return completion_form_filename.rsplit('.', 1)[1].lower()

def get_mimetype(completion_form_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(completion_form_extension, 'application/octet-stream')"""

#class_record
@app.route('/faculty/correction/get_grade_class_file/<int:grade_entry_id>')
def get_grade_class_file(grade_entry_id):
    return redirect(url_for('download_class_record', grade_entry_id=grade_entry_id))

"""@app.route('/faculty/download_class_record/<int:grade_entry_id>')
def download_class_record(grade_entry_id):
    grade_entry = GradeEntry.query.get(grade_entry_id)

    if grade_entry and grade_entry.class_record_data:
        class_extension = get_class_extension(grade_entry.class_record_filename)
        download_name = f'class_record_{grade_entry_id}.{class_extension}'

        return send_file(
            io.BytesIO(grade_entry.class_record_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(class_extension)
        )
    else:
        abort(404)
    
# Route to download a specific file of a grade entry
def get_class_extension(class_record_filename):
    return class_record_filename.rsplit('.', 1)[1].lower()

def get_mimetype(class_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(class_extension, 'application/octet-stream')

#affidavit
@app.route('/faculty/correction/get_grade_affidavit_file/<int:grade_entry_id>')
def get_grade_affidavit_file(grade_entry_id):
    return redirect(url_for('download_affidavit', grade_entry_id=grade_entry_id))

@app.route('/faculty/download_affidavit/<int:grade_entry_id>')
def download_affidavit(grade_entry_id):
    grade_entry = GradeEntry.query.get(grade_entry_id)

    if grade_entry and grade_entry.affidavit_data:
        affidavit_extension = get_affidavit_extension(grade_entry.affidavit_filename)
        download_name = f'affidavit_{grade_entry_id}.{affidavit_extension}'

        return send_file(
            io.BytesIO(grade_entry.affidavit_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(affidavit_extension)
        )
    else:
        abort(404)

# Route to download a specific file of a grade entry
def get_affidavit_extension(affidavit_filename):
    return affidavit_filename.rsplit('.', 1)[1].lower()

def get_mimetype(affidavit_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(affidavit_extension, 'application/octet-stream')"""
#=====================================================================
#crossenrollment
"""@app.route('/update-crossenrollment-service-status/<int:cross_enrollment_id>', methods=['POST'])
def update_crossenrollment_service_status(cross_enrollment_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    cross_enrollments = CrossEnrollment.query.get_or_404(cross_enrollment_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        cross_enrollments.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Cross status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultycrossenrollment'))"""

#crossenrollment
"""@app.route('/faculty/crossenrollment/get_application_letter/<int:cross_enrollment_id>')
def get_application_letter(cross_enrollment_id):
    return redirect(url_for('download_application_letter', cross_enrollment_id=cross_enrollment_id))

@app.route('/faculty/download_application_letter/<int:cross_enrollment_id>')
def download_application_letter(cross_enrollment_id):
    cross_enrollments = CrossEnrollment.query.get(cross_enrollment_id)

    if cross_enrollments and cross_enrollments.application_letter_data:
        application_letter_extension = get_application_letter_extension(cross_enrollments.application_letter_filename)
        download_name = f'application_letter_{cross_enrollment_id}.{application_letter_extension}'

        return send_file(
            io.BytesIO(cross_enrollments.application_letter_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(application_letter_extension),
        )
    else:
        abort(404)
    
def get_application_letter_extension(application_letter_filename):
    return application_letter_filename.rsplit('.', 1)[1].lower()

def get_mimetype(application_letter_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(application_letter_extension, 'application/octet-stream')"""

"""@app.route('/faculty/crossenrollment/get_permit_to_enroll/<int:cross_enrollment_id>')
def get_permit_to_enroll(cross_enrollment_id):
    return redirect(url_for('download_permit_to_enroll', cross_enrollment_id=cross_enrollment_id))

@app.route('/faculty/download_permit_to_enroll/<int:cross_enrollment_id>')
def download_permit_to_enroll(cross_enrollment_id):
    cross_enrollments = CrossEnrollment.query.get(cross_enrollment_id)

    if cross_enrollments and cross_enrollments.permit_to_cross_enroll_data:
        permit_enroll_extension = get_permit_enroll_extension(cross_enrollments.permit_to_cross_enroll_filename)
        download_name = f'permit_to_enroll_{cross_enrollment_id}.{permit_enroll_extension}'

        return send_file(
            io.BytesIO(cross_enrollments.permit_to_cross_enroll_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(permit_enroll_extension),
        )
    else:
        abort(404)

def get_permit_enroll_extension(permit_to_cross_enroll_filename):
    return permit_to_cross_enroll_filename.rsplit('.', 1)[1].lower()

def get_mimetype(permit_enroll_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(permit_enroll_extension, 'application/octet-stream')"""
#=====================================================================
#shifting
"""@app.route('/update-shifting-service-status/<int:shifting_application_id>', methods=['POST'])
def update_shifting_service_status(shifting_application_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    shifting_applications = ShiftingApplication.query.get_or_404(shifting_application_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        shifting_applications.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Shift status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultyshifting'))"""

#shifting
"""@app.route('/faculty/shifting_applications')
def view_shifting_applications():
    shifting_applications = GradeEntry.query.all()
    return render_template('/faculty/shifting.html', shifting_applications=shifting_applications)"""

# Redirect to download change of change.html
@app.route('/faculty/shifting_applications/get_shifting_file/<int:shifting_application_id>')
def get_shifting_file(shifting_application_id):
    return redirect(url_for('download_shifting_file', shifting_application_id=shifting_application_id))

# Download change of subjects file
"""@app.route('/faculty/download_shifting_file/<int:shifting_application_id>')
def download_shifting_file(shifting_application_id):
    shifting_applications = ShiftingApplication.query.get(shifting_application_id)

    if shifting_applications and shifting_applications.file_data:
        shifting_file_extension = get_shifting_file_extension(shifting_applications.file_filename)
        download_name = f'shifting_applications_{shifting_application_id}.{shifting_file_extension}'

        return send_file(
            io.BytesIO(shifting_applications.file_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(shifting_file_extension),
        )
    else:
        abort(404)  # Change of subjects application or file not found

def get_shifting_file_extension(file_filename):
    return file_filename.rsplit('.', 1)[1].lower()

def get_mimetype(shifting_file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(shifting_file_extension, 'application/octet-stream')"""
#=====================================================================
# Overload - Faculty

"""@app.route('/update-overload-service-status/<int:overload_application_id>', methods=['POST'])
def update_overload_service_status(overload_application_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific OverloadApplication record
    overload_application = OverloadApplication.query.get_or_404(overload_application_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        overload_application.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Overload status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultyoverload'))

# Overload HTML page

@app.route('/faculty/overload/get_overload_file/<int:overload_application_id>')
def get_overload_file(overload_application_id):
    return redirect(url_for('download_overload_file', overload_application_id=overload_application_id))"""

# Download overload file

"""@app.route('/faculty/download_overload_file/<int:overload_application_id>')
def download_overload_file(overload_application_id):
    overload_application = OverloadApplication.query.get(overload_application_id)

    if overload_application and overload_application.file_data:
        overload_file_extension = get_overload_file_extension(overload_application.file_filename)
        download_name = f'overload_{overload_application_id}.{overload_file_extension}'

        return send_file(
            io.BytesIO(overload_application.file_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(overload_file_extension),
        )
    else:
        abort(404)  # Overload application or file not found

def get_overload_file_extension(file_filename):
    return file_filename.rsplit('.', 1)[1].lower()

def get_mimetype(overload_file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(overload_file_extension, 'application/octet-stream')
"""
#=====================================================================
#petition
"""@app.route('/update-petition-service-status/<int:petition_request_id>', methods=['POST'])
def update_petition_service_status(petition_request_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    petition_requests = PetitionRequest.query.get_or_404(petition_request_id)
    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        petition_requests.status = new_status
        # Commit the changes to the database
        db.session.commit()
        flash('Service Petition status updated successfully!', 'success')
    else:
        flash('No status provided.', category='danger')

    return redirect(url_for('facultypetition'))"""
#=====================================================================
#enrollement
"""@app.route('/update-manual-service-status/<int:m_enrollment_ID>', methods=['POST'])
def update_manual_service_status(m_enrollment_ID):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    manual_enrollments = ManualEnrollment.query.get_or_404(m_enrollment_ID)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        manual_enrollments.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Enrollment status updated successfully!', category='success')
    else:
        flash('No status provided.', category='danger')

    return redirect(url_for('facultyenrollment'))"""

#enrollment
"""@app.route('/faculty/manualenrollment/get_manual_file/<int:m_enrollments_ID>')
def get_manual_file(m_enrollments_ID):
    return redirect(url_for('download_manual_enrollment_file', m_enrollments_ID=m_enrollments_ID))

@app.route('/faculty/download_manual_enrollment_file/<int:m_enrollments_ID>')
def download_manual_enrollment_file(m_enrollments_ID):
    manual_enrollments = ManualEnrollment.query.get(m_enrollments_ID)

    if manual_enrollments and manual_enrollments.me_file_data:
        me_filename_extension = get_me_filename_extension(manual_enrollments.me_file_filename)
        download_name = f'manual_enrollment_{m_enrollments_ID}.{me_filename_extension}'

        return send_file(
            io.BytesIO(manual_enrollments.me_file_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(me_filename_extension)
        )
    else:
        abort(404)

def get_me_filename_extension(me_file_filename):
    return me_file_filename.rsplit('.', 1)[1].lower()

def get_mimetype(me_filename_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }
    return mimetypes.get(me_filename_extension, 'application/octet-stream')"""
#=====================================================================
#certification
"""@app.route('/update-certification-service-status/<int:certification_request_id>', methods=['POST'])
def update_certification_service_status(certification_request_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    certification_request = CertificationRequest.query.get_or_404(certification_request_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        certification_request.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Certification status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultycertification'))"""
#=====================================================================
#tutorial
"""@app.route('/update-tutorial-service-status/<int:tutorial_request_id>', methods=['POST'])
def update_tutorial_service_status(tutorial_request_id):
    session['last_activity'] = datetime.now(timezone.utc)

    # Find the specific AddSubjects record
    tutorial_requests = TutorialRequest.query.get_or_404(tutorial_request_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    if new_status:
        # Update the status
        tutorial_requests.status = new_status

        # Commit the changes to the database
        db.session.commit()
        flash('Service Tutorial status updated successfully!', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('facultytutorial'))

#tutorial
@app.route('/faculty/tutorial/get_tutorial_file/<int:tutorial_request_id>')
def get_tutorial_file(tutorial_request_id):
    return redirect(url_for('download_tutorial_file', tutorial_request_id=tutorial_request_id))

@app.route('/faculty/download_tutorial_file/<int:tutorial_request_id>')
def download_tutorial_file(tutorial_request_id):
    tutorial_requests = TutorialRequest.query.get(tutorial_request_id)

    if tutorial_requests and tutorial_requests.file_data:
        tutorial_extension = get_tutorial_extension(tutorial_requests.file_filename)
        download_name = f'tutorial_request_{tutorial_request_id}.{tutorial_extension}'

        return send_file(
            io.BytesIO(tutorial_requests.file_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(tutorial_extension)  # Make sure this function is defined as in your previous code
        )
    else:
        abort(404)  # File not found

def get_tutorial_extension(file_filename):
    return file_filename.rsplit('.', 1)[1].lower()

def get_mimetype(tutorial_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(tutorial_extension, 'application/octet-stream')"""

#===================================================TIMER=============================================================#
# Middleware to check for inactivity and redirect to login if needed
"""@app.before_request
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

#================================================================#
# function that is sent for teachers
#================================================================#
# ALL FACULTY ROUTES HERE
"""@app.route('/faculty')
@prevent_authenticated
def faculty_portal():
    session.permanent=True
    return render_template('faculty/login.html') #, api_base_url=faculty_base_api_url

@app.route('/faculty/dashboard')
def faculty_dashboard():
    session.permanent = True
    return render_template('/faculty/dashboard.html')

@app.route('/faculty/profile/updated', methods=['GET', 'POST'])
def faculty_update_profile():
    if request.method == 'POST':
        # Retrieve the current logged-in faculty member
        current_faculty = get_current_faculty_user()

        if not current_faculty:
            flash('No faculty user logged in.', 'danger')
            return redirect(url_for('faculty_login'))

        # Get the updated information from the form
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        address = request.form.get('address')

        # Update the faculty member's details
        current_faculty.email = email
        current_faculty.mobile_number = mobile_number
        current_faculty.address = address

        # Commit the changes to the database
        db.session.commit()
        flash('Profile Updated Successfully!', 'success')

        # Redirect to the faculty profile page
        return redirect(url_for('facultyprofile'))

    # Render the profile update page
    return render_template('/faculty/profile.html')

# Faculty profile route
@app.route('/faculty/profile')
def facultyprofile():
    return render_template('/faculty/profile.html', faculty_api_base_url=faculty_api_base_url)
"""

# ======================Faculty Downloads========================== #
# =======================Downloads File============================ #

#certification
"""@app.route('/faculty/certification/get_certification_request_file/<int:certification_request_id>')
def get_certification_request_file(certification_request_id):
    return redirect(url_for('download_certification_request_file', certification_request_id=certification_request_id))

@app.route('/faculty/download_certification_request_file/<int:certification_request_id>')
def download_certification_request_file(certification_request_id):
    certification_request = CertificationRequest.query.get(certification_request_id)

    if certification_request and certification_request.request_form_data:
        certification_request_extension = get_certification_request_extension(certification_request.request_form_filename)
        download_name = f'certification_request_{certification_request_id}.{certification_request_extension}'

        return send_file(
            io.BytesIO(certification_request.request_form_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(certification_request_extension),
        )
    else:
        abort(404)  # Certification request or file not found

def get_certification_request_extension(request_form_filename):
    return request_form_filename.rsplit('.', 1)[1].lower()

def get_mimetype(certification_request_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(certification_request_extension, 'application/octet-stream')"""
#===================================================================================================================================
"""@app.route('/faculty/certification/get_certification_identification_file/<int:certification_request_id>')
def get_certification_identification_file(certification_request_id):
    return redirect(url_for('download_certification_identification_file', certification_request_id=certification_request_id))

@app.route('/faculty/download_certification_identification_file/<int:certification_request_id>')
def download_certification_identification_file(certification_request_id):
    certification_request = CertificationRequest.query.get(certification_request_id)

    if certification_request and certification_request.identification_card_data:
        identification_file_extension = get_identification_file_extension(certification_request.identification_card_filename)
        download_name = f'certification_identification_{certification_request_id}.{identification_file_extension}'

        return send_file(
            io.BytesIO(certification_request.identification_card_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(identification_file_extension),
        )
    else:
        abort(404)  # Certification request or file not found

def get_identification_file_extension(identification_card_filename):
    return identification_card_filename.rsplit('.', 1)[1].lower()

def get_mimetype(identification_file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(identification_file_extension, 'application/octet-stream')"""
#=========================================================================================================================
"""@app.route('/faculty/certification/get_certification_authorization_file/<int:certification_request_id>')
def get_certification_authorization_file(certification_request_id):
    return redirect(url_for('download_certification_authorization_file', certification_request_id=certification_request_id))

@app.route('/faculty/download_certification_authorization_file/<int:certification_request_id>')
def download_certification_authorization_file(certification_request_id):
    certification_request = CertificationRequest.query.get(certification_request_id)

    if certification_request and certification_request.authorization_letter_data:
        authorization_file_extension = get_authorization_file_extension(certification_request.authorization_letter_filename)
        download_name = f'certification_authorization_{certification_request_id}.{authorization_file_extension}'

        return send_file(
            io.BytesIO(certification_request.authorization_letter_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(authorization_file_extension),
        )
    else:
        abort(404)  # Certification request or file not found

def get_authorization_file_extension(authorization_letter_filename):
    return authorization_letter_filename.rsplit('.', 1)[1].lower()

def get_mimetype(authorization_file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(authorization_file_extension, 'application/octet-stream')"""
#=============================================================================================================================
@app.route('/student/certification/get_representative_file/<int:certification_request_id>')
def get_representative_file(certification_request_id):
    return redirect(url_for('download_representative_file', certification_request_id=certification_request_id))

"""@app.route('/student/download_representative_file/<int:certification_request_id>')
def download_representative_file(certification_request_id):
    certification_request = CertificationRequest.query.get(certification_request_id)

    if certification_request and certification_request.representative_data:
        representative_extension = get_representative_extension(certification_request.representative_filename)
        download_name = f'certification_representative_{certification_request_id}.{representative_extension}'

        return send_file(
            io.BytesIO(certification_request.representative_data),
            as_attachment=False,
            download_name=download_name,
            mimetype=get_mimetype(representative_extension),
        )
    else:
        abort(404)  # Certification request or file not found

def get_representative_extension(representative_filename):
    return representative_filename.rsplit('.', 1)[1].lower()

def get_mimetype(representative_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(representative_extension, 'application/octet-stream')
"""
# The functions get_file_extension and get_mimetype remain the same as in your existing code.
#===========================================================#

# ===================================================================== #
# ======================ALL ADMIN ROUTES HERE========================== #
# ===================================================================== #
@app.route('/admin')
@prevent_authenticated
def admin_login():
    session.permanent = True
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    session.permanent = True
    return render_template('admin/dashboard.html')

# Modify the profile route
@app.route('/admin/profile')
def admin_profile():
    session.update()

    # Retrieve student details from the session
    admin_details = {
        'admin_Number': session.get('admin_Number'),
        'name': session.get('name'),
        'email': session.get('email'),
        'gender': session.get('gender'),
        'dateofBirth': session.get('dateofBirth'),
        'placeofBirth': session.get('placeofBirth'),
        'mobile_number': session.get('mobile_number'),
    }

    # Map gender numerical values to strings
    if admin_details['gender'] == 1:
        admin_details['gender'] = 'Male'
    elif admin_details['gender'] == 2:
        admin_details['gender'] = 'Female'
    else:
        admin_details['gender'] = 'Undefined'  # Handle any other values

    return render_template('admin/profile.html', admin_details=admin_details)

#==========================================================#
@app.route('/admin/createstudent')
def admin_create_stud():
    return render_template("/admin/create_student.html")


# Route for creating a student account
"""@app.route('/admin/createstudent/submit', methods=['GET', 'POST'])
def admin_create_student():
    if request.method == 'POST':
        try:
            form_data = request.form
            files = request.files

            new_student = create_student(form_data, files)

            if isinstance(new_student, str):
                flash(new_student, 'danger')
            else:
                db.session.add(new_student)
                db.session.commit()
                flash('Student created successfully', 'success')
                return redirect(url_for('admin_create_student'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return render_template('/admin/create_student.html')"""


@app.route('/admin/student_list', methods=['GET'])
def student_list():
    # Fetch all student from the database
    student = Student.query.all()

    # Convert the list of student to a list of dictionaries for rendering
    student_data = [
        {
            'StudentId': student.StudentId,
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
        for student in student
    ]

    return render_template("/admin/student_list.html", student=student_data)

#==========================================================#
#Admin Portal
@app.route('/admin')
@prevent_authenticated
def admin_portal():
    session.permanent = True
    return render_template('admin/login.html')
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