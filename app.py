import io
from flask import Flask, abort, render_template, jsonify, redirect, request, flash, send_file, url_for, session
from flask_login import login_user
from models import CertificationRequest, ChangeOfSubjects, CrossEnrollment, GradeEntry, ManualEnrollment, OverloadApplication, PetitionRequest, ShiftingApplication, TutorialRequest, db, AddSubjects, init_db, Student
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash 
<<<<<<< HEAD
=======

 
>>>>>>> b9682b3c4a4c28573c2e295236a14441d306f7ae
from datetime import datetime, timezone #, timedelta, 
#from models import Services
#from models import init_db
from Api.v1.student.api_routes import create_addsubjects_application, create_certification_request, create_changesubjects_application, create_crossenrollment_form, create_gradeentry_application, create_manualenrollment_form, create_overload_application, create_petitionrequest_form, create_shifting_application, create_tutorial_request, fetchStudentDetails, getCurrentUser, getCurrentUserStudentNumber, student_api#, update_student_profile #log_form_submission_to_file
from Api.v1.faculty.api_routes import faculty_api
from Api.v1.admin.api_routes import admin_api, create_student
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
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour (in seconds)
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

# ===================================================================================
#Downloadable files for Adding Subjects
@app.route('/download/pdf_file/Adding_subject_form')
def download_AddingSubs():
    pdf_path = "static/pdf_files/Adding_subject_form.pdf"  # Replace with the actual path to your PDF file
    return send_file(pdf_path, as_attachment=True, download_name="Adding_subject_form.pdf")

#Downloadable files for Change of Schedule and Subjects
@app.route('/download/pdf_file/Change_of_subjects')
def download_Change_Sched_Subs():
    pdf_path = "static/pdf_files/Change_of_subjects.pdf"  # Replace with the actual path to your PDF file
    return send_file(pdf_path, as_attachment=True, download_name="Change_of_subjects.pdf")

#Downloadable files for Accreditation
@app.route('/download/pdf_file/Accreditation-for-Shiftees-and-Regular')
def download_Accreditation():
    pdf_path = "static/pdf_files/Accreditation-for-Shiftees-and-Regular.pdf"  # Replace with the actual path to your PDF file
    return send_file(pdf_path, as_attachment=True, download_name="Accreditation-for-Shiftees-and-Regular.pdf")

#Downloadable files for OverLoads
@app.route('/download/pdf_file/Overload-3-6-units')
def download_Overload_Subs():
    pdf_path = "static/pdf_files/Overload-3-6-units.pdf"  # Replace with the actual path to your PDF file
    return send_file(pdf_path, as_attachment=True, download_name="Overload-3-6-units.pdf")

#Downloadable files for RO Form
@app.route('/download/pdf_file/RO-Form')
def download_RO_form():
    pdf_path = "static/pdf_files/RO-Form.pdf"  # Replace with the actual path to your PDF file
    return send_file(pdf_path, as_attachment=True, download_name="RO-Form.pdf")

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


#========================================= STUDENT SERVICES ====================================================

#======================================== STUDENT DASHBOARD ====================================================
@app.route('/student/dashboard') 
@role_required('student')
def student_dashboard():
    session.permanent=True
    return render_template('/student/dashboard.html')

#======================================== STUDENT PROFILE ======================================================

@app.route('/student/profile') 
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
            student.Email = email
            student.MobileNumber = mobile_number
            student.address = address

            db.session.commit()
            flash('Profile Updated Successfully!', 'success')
            return redirect(url_for('studentprofile'))

    return render_template('/student/profile.html')


@app.route('/student/setting')
def studentsetting():
    return render_template('/student/setting.html')
# Assuming you have the role_required decorator implemented
@app.route('/student/history', methods=['GET'])
@role_required('student')
def student_history():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    services_data = {}

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
        certification_requests = CertificationRequest.query.filter_by(StudentId=student.StudentId).all()
        services_data['certification_requests_list'] = [subject.to_dict() for subject in certification_requests]

        # Fetch GradeEntry based on the StudentId foreign key
        grade_entries = GradeEntry.query.filter_by(StudentId=student.StudentId).all()
        services_data['grade_entries_list'] = [subject.to_dict() for subject in grade_entries]

        # Fetch CrossEnrollment based on the StudentId foreign key
        cross_enrollments = CrossEnrollment.query.filter_by(StudentId=student.StudentId).all()
        services_data['cross_enrollments_list'] = [subject.to_dict() for subject in cross_enrollments]

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

    return render_template("/student/history.html", services_data=services_data)


#==================================== STUDENT CHANGE PASSWORD ===========================================================

@app.route('/student/changepassword')
def studentpassword():
    return render_template('/student/changepassword.html')


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
            flash('Incorrect current password. Please try again.', 'error')
            return redirect(url_for('student_change_password'))

        # Check if the new and confirm passwords match
        if new_password != confirm_password:
            flash('New password and confirm password do not match. Please try again.', 'error')
            return redirect(url_for('student_change_password'))

        # Update the user's password in the database
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        student.Password = hashed_password
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('student_change_password'))

    return render_template('student/change_password.html')
#====================================  ==================================================================================

"""# Usage in your Flask route:
@app.route('/update_profile/<int:student_id>', methods=['POST'])
def update_profile(student_id):
    if request.method == 'POST':
        form_data = request.form.to_dict()
        success = update_student_profile(form_data, student_id)
        if success:
            return 'Profile updated successfully'
        else:
            return 'Failed to update profile'
    else:
        return 'Invalid request method'"""

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
@app.route('/student/overload') 
def studentoverload():
    return render_template("/student/overload.html", student_api_base_url=student_api_base_url)

@app.route('/student/overload/submitted', methods=['POST'])
@role_required('student')
def submit_overload_application():
    try:
        current_StudentId = session.get('user_id')
        new_overload_application = create_overload_application(request.form, request.files, current_StudentId)

        if new_overload_application:
                db.session.add(new_overload_application)
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



#=============================================================================================================

# View function to retrieve and display the overload application details
@app.route('/student/foroverloadofsubject/edit_overload/<int:overload_application_id>', methods=['GET', 'POST'])
def edit_overload(overload_application_id):
    overload_application = OverloadApplication.query.get(overload_application_id)
    if not overload_application:
        flash('Overload application not found.', 'danger')
        return redirect(url_for('stud_overload'))

    if request.method == 'GET':
        return render_template('edit_overload.html', overload_application=overload_application)

    if request.method == 'POST':
        if 'submit' in request.form: 
            Name = request.form['Name']
            StudentNumber = request.form['StudentNumber']
            semester = request.form['semester']
            subjects_to_add = request.form['subjectsToAdd']
            justification = request.form['justification']
            user_responsible = request.form['user_responsible']
            status = request.form['status']

            file = request.files.get('file')

            if file:
                file_data = file.read()
                file_filename = secure_filename(file.filename)
            else:
                file_data = overload_application.file_data
                file_filename = overload_application.file_filename

            overload_application.Name = Name
            overload_application.StudentNumber = StudentNumber
            overload_application.semester = semester
            overload_application.subjects_to_add = subjects_to_add
            overload_application.justification = justification
            overload_application.file_filename = file_filename
            overload_application.file_data = file_data
            overload_application.user_responsible = user_responsible
            overload_application.status = status

            db.session.commit()
            flash('Overload application updated successfully!', 'success')
            return redirect(url_for('stud_overload'))
        else:  
            return redirect(url_for('stud_overload'))



#==================================== ADDING OF SUBJECT =========================================================

@app.route('/student/addingsubject')
def studentaddingsubject():
    return render_template("/student/addingsubject.html", student_api_base_url=student_api_base_url)


@app.route('/student/addingsubject/added', methods=['POST'])
@role_required('student')
def add_subjects():
    try: 
        current_StudentId = session.get('user_id')

        new_addsubjects_application = create_addsubjects_application(request.form, request.files, current_StudentId)
        
        if new_addsubjects_application:
            db.session.add(new_addsubjects_application)
            db.session.commit()
            flash('Add subjects created Successfully!', 'success')
            return redirect(url_for('studentaddingsubject'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/adding_of_subject.html') 

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

# take 8 pls be good ===  its good for one calling of addsubjects
"""# Assuming you have the role_required decorator implemented
@app.route('/student/history', methods=['GET'])
@role_required('student')
def student_history():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    addsubjects_list = []  # Initialize an empty list

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        addsubjects = AddSubjects.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        addsubjects_list = [subject.to_dict() for subject in addsubjects]

    return render_template("/student/history.html", addsubjects_list=addsubjects_list)"""

# take 7 huhuhuhuhuu always odd number 
"""# Assuming you have the role_required decorator implemented
@app.route('/student/history', methods=['GET'])
@role_required('student')
def student_history():
    user_id = session.get('user_id')

    # Fetch the student based on the user_id
    student = Student.query.get(user_id)

    if student:
        # Fetch AddSubjects based on the StudentId foreign key
        addsubjects = AddSubjects.query.filter_by(StudentId=student.StudentId).all()

        # Convert AddSubjects data to a list of dictionaries
        addsubjects_list = [subject.to_dict() for subject in addsubjects]

    return render_template("/student/history.html", addsubjects_list)"""

# take 5 na huhuhuhhhhuhuhhu
"""# View function to handle adding subjects for the current student
@app.route('/student/history', methods=['GET'])
@role_required('student')
def studentadding():
    current_student_number = getCurrentUserStudentNumber()
    
    # Fetch the current student's data based on the student number
    current_student = Student.query.filter_by(StudentNumber=current_student_number).first()

    if not current_student:
        return render_template("/student/history.html")  # You can render an error page or handle as per your need

    # Fetch subjects based on the student's number
    addsubjects = AddSubjects.query.filter_by(StudentNumber=current_student_number).all()

    return render_template("/student/history.html", addsubjects=addsubjects)"""

# take 3 huhuhuhuuuuhuhu
"""# View function to handle operations based on the current user's ID
@app.route('/student/viewaddsubject', methods=['GET'])
def viewaddsubject():
    current_user_id = getCurrentUser()
    
    # Fetch the current user's data based on the ID
    current_student = Student.query.get(current_user_id)

    if not current_student:
        return render_template("/student/viewaddsubject.html", message='Student not found.')

    # Fetch subjects based on the student's ID
    subjects = AddSubjects.query.filter_by(StudentId=current_student.StudentId).all()

    if not subjects:
        return render_template("/student/viewaddsubject.html", message='No subjects found for this student.')

    subjects_list = [subject.to_dict() for subject in subjects]

    return render_template("/student/viewaddsubject.html", subjects=subjects_list)"""

# View function to handle operations based on StudentId
"""@app.route('/student/viewaddsubject/<int:student_id>', methods=['GET'])
def get_student_subjects(student_id):
    # Assuming 'student_id' is passed as part of the route
    subjects = AddSubjects.query.filter_by(StudentId=student_id).all()

    if not subjects:
        return render_template("/student/viewaddsubject.html", message='No subjects found for this student.')

    # Convert the AddSubjects objects to dictionaries
    subjects_list = [subject.to_dict() for subject in subjects]

    return render_template("/student/viewaddsubject.html", subjects=subjects_list)"""

"""@app.route('/log_form_submission', methods=['POST'])
def log_form_submission():
    form_data = request.form.to_dict()
    log_form_submission_to_file(form_data)
    return jsonify({'message': 'Form submission logged successfully'})"""

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

#============================== CHANGE OF SCHEDULE/SUBJECT ===============================================#
@app.route('/student/changeofsubject')
def studentchange():
    return render_template("/student/changeofsubject.html", student_api_base_url=student_api_base_url)

@app.route('/student/changeofsubject/added', methods=['POST'])
@role_required('student')
def change_of_subjects():
    try: 
        current_StudentId = session.get('user_id')

        new_changesubjects_application = create_changesubjects_application(request.form, request.files, current_StudentId)
        
        if new_changesubjects_application:
            db.session.add(new_changesubjects_application)
            db.session.commit()
            flash('Change of subjects created Successfully!', 'success')
            return redirect(url_for('studentchange'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/changeofsubject.html')

#========================== CORRECTION OF GRADE ENTRY ================================================#

@app.route('/student/gradeentry')
def studentcorrection():
    return render_template("/student/gradeentry.html", student_api_base_url=student_api_base_url)

@app.route('/student/gradeentry/submit', methods=['POST'])
@role_required('student')
def submit_grade_correction():
    try: 
        current_StudentId = session.get('user_id')

        new_gradeentry_application = create_gradeentry_application(request.form, request.files, current_StudentId)
        
        if new_gradeentry_application:
            db.session.add(new_gradeentry_application)
            db.session.commit()
            flash('Grade entry Submitted Successfully!', 'success')
            return redirect(url_for('studentcorrection'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/gradeentry.html')

#====================================== CROSS ENROLLMENT =========================================================

@app.route('/student/crossenrollment')
def studentenrollment():
    return render_template("/student/crossenrollment.html", student_api_base_url=student_api_base_url)

@app.route('/student/crossenrollment/submitted', methods=['POST'])
@role_required('student') 
def submit_cross_enrollment():

    try:
        current_StudentId = session.get('user_id')
        new_cross_enrollment = create_crossenrollment_form(request.form, request.files, current_StudentId)
        
        if new_cross_enrollment:
            db.session.add(new_cross_enrollment)
            db.session.commit()
            flash('Cross-Enrollment created successfully!', 'success')
            return redirect(url_for('studentenrollment'))  
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/crossenrollment.html')


#================================== APPLICATION FOR SHIFTING ================================================
@app.route('/student/shifting')
def studentshifting():
    return render_template("/student/shifting.html", student_api_base_url=student_api_base_url)

@app.route('/student/shifting/submit', methods=['POST'])
@role_required('student')
def submit_shifting():
    try: 
        current_StudentId = session.get('user_id')

        new_shifting_application = create_shifting_application(request.form, request.files, current_StudentId)
        
        if new_shifting_application:
            db.session.add(new_shifting_application)
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
        new_manual_enrollment = create_manualenrollment_form(request.form, request.files, current_StudentId)

        if new_manual_enrollment:
            db.session.add(new_manual_enrollment)
            db.session.commit()
            flash('Manual Enrollment created successfully!', 'success')
            return redirect(url_for('studentmanualenrollment'))  # Redirect to the appropriate route
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/manualenrollment.html')


#===================================== ONLINE PETITION OF SUBJECTS =====================================================

@app.route('/student/onlinepetitionofsubject')
def studentpetition():
    return render_template("/student/petition.html", student_api_base_url=student_api_base_url)

@app.route('/submit_petition_request', methods=['POST'])
@role_required('student')
def submit_petition():
    try:
        current_StudentId = session.get('user_id')
        new_petition_request = create_petitionrequest_form(request.form, current_StudentId)

        if new_petition_request:
            db.session.add(new_petition_request)
            db.session.commit()
            flash('Petition Request submitted successfully!', 'success')
            return redirect(url_for('studentpetition'))  # Redirect to the appropriate route
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/petition.html')


@app.route('/student/onlinepetitionofsubject/<int:StudentId>', methods=['GET'])
def view_student_petition(StudentId):
    # Fetching the petitions based on the StudentId
    petitions = PetitionRequest.query.filter_by(StudentId=StudentId).all()

    return render_template('view_petition_data.html', petitions=petitions)

#================================= ONLINE REQUEST FOR TUTORIAL ===================================================

@app.route('/student/tutorial')#
def studenttutorial():
    return render_template("/student/tutorial.html", student_api_base_url=student_api_base_url)#

@app.route('/student/tutorial/submit', methods=['POST'])
@role_required('student')
def submit_tutorial_request():
    try: 
        current_StudentId = session.get('user_id')

        new_tutorial_request = create_tutorial_request(request.form, request.files, current_StudentId)
        
        if new_tutorial_request:
            db.session.add(new_tutorial_request)
            db.session.commit()
            flash('Tutorial request has been created successfully!', 'success')
            return redirect(url_for('studenttutorial'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/tutorial.html')

#======================================== REQUEST FOR CERTIFICATION ===========================================================
@app.route('/student/certification')
def studentcertification():
    return render_template("/student/certification.html", student_api_base_url=student_api_base_url)

@app.route('/submit_certification_request', methods=['POST'])
@role_required('student')
def submit_certification_request():
    try:
        current_StudentId = session.get('user_id') 
        new_certification_request = create_certification_request(request.form, request.files, current_StudentId)

        if new_certification_request:
            db.session.add(new_certification_request)
            db.session.commit()
            flash('Certification Request submitted successfully!', 'success')
            return redirect(url_for('studentcertification')) 
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/certification.html')

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
"""@app.route('/student/submit_service_request', methods=['GET'])
def submit_service_request():
    return render_template('service_request_form.html')"""


"""@app.route('/student/submit_service_request/request', methods=['POST'], endpoint='submit_services_request_form')
def submit_services_request():
    if request.method == 'POST':
        service_type = request.form.get('serviceType')
        StudentId = request.form.get('studentID')
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

#===========================================================#
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
    overload_applications = OverloadApplication.query.all()
    return render_template("/faculty/overload.html", overload_applications=overload_applications)  #overload_applications in overload_applications

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

@app.route('/faculty/correction')
def facultycorrection():
    grade_entries = GradeEntry.query.all()
    return render_template("/faculty/correction.html", grade_entry=grade_entries) # for grade_entry in grade_entries

@app.route('/faculty/crossenrollment')
def facultycrossenrollment():
    return render_template("/faculty/crossenrollment.html")

@app.route('/faculty/shifting')
def facultyshifting():
    shifting_applications = ShiftingApplication.query.all()
    return render_template("/faculty/shifting.html", shifting_applications=shifting_applications)

@app.route('/faculty/manualenrollment')
def facultyenrollment():
    return render_template("/faculty/enrollment.html")

@app.route('/faculty/onlinepetitionofsubject')
def facultypetition():
    return render_template("/faculty/petition.html")

@app.route('/faculty/requestfortutorialofsubjects')
def faculty_view_tutorial():
    return render_template("/faculty/view_tutorial.html")

@app.route('/faculty/certification')
def facultycertification():
    return render_template("/faculty/certification.html")

@app.route('/faculty/tutorial')
def facultytutorial():
    return render_template("/faculty/tutorial.html")

#========================================================================
# ================================================================
#routes for the redirection to the portal of the login in different routes
# ====================================================================================================================#
#===================================================== PORTALS =======================================================#
#=====================================================================================================================#

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
#================List of the Service based on StudentNumber==========================#

"""@app.route('/get_addsubjects_by_student_number/<StudentNumber>', methods=['GET'])
def get_addsubjects_by_student_number(StudentNumber):
    # Assuming you have a Student model with an 'addsubjects' relationship
    student = Student.query.filter_by(StudentNumber=StudentNumber).first()

    if student:
        addsubjects = AddSubjects.query.filter_by(StudentId=student.StudentId).all()

        # Convert addsubjects to a list of dictionaries
        addsubjects_data = [
            {
                'subject_ID': subject.subject_ID,
                'studentNumber': subject.StudentNumber,
                'name': subject.Name,
                'subject_Names': subject.subject_Names,
                'enrollment_type': subject.enrollment_type,
                'file_data': subject.file_data,
                'file_name': subject.file_name,
                'user_responsible': subject.user_responsible,
                'status': subject.status,
                'StudentId': subject.StudentId,
            }
            for subject in addsubjects
        ]

        return jsonify(addsubjects_data)
    else:
        return jsonify({'error': 'Student not found'})
"""













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
@app.route('/student/overload')
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
@app.route('/student/certification')
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
@app.route('/student/changeofsubject')
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
@app.route('/student/manualenrollment')
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
@app.route('/student/addingsubject')
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
@app.route('/student/shifting')
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
@app.route('/student/tutorial')
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
@app.route('/student/gradeentry')
def student_portal_gradeentry():
    session.permanent = True
    if is_user_logged_in_gradeentry():
        return render_template('student/gradeentry.html')

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
@app.route('/student/crossenrollment')
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

#================================================================#
# function that is sent for teachers
#================================================================#
# ALL FACULTY ROUTES HERE
@app.route('/faculty')
@prevent_authenticated
def faculty_portal():
    session.permanent=True
    return render_template('faculty/login.html') #, api_base_url=faculty_base_api_url

@app.route('/faculty/dashboard')
def faculty_dashboard():
    session.permanent = True

    # Retrieve the user's name from the session (you should set it during login)
    user_name = session.get('user_name')
     # Check if the name is in the session
     
    if user_name:
        return render_template('faculty/dashboard.html', user_name=user_name)
    else:
        return render_template('faculty/dashboard.html', user_name="Guest")  # Provide a default if the name is not in the session


@app.route('/faculty/profile')
def facultyprofile():
    return render_template("/faculty/profile.html", faculty_api_base_url=faculty_api_base_url)
# Modify the  faculty profile route

# ====================Faculty Services============================= #

"""# Updated view function
@app.route('/faculty/view_adding_subject')
def view_adding_subject():
    addsubjects = AddSubjects.query.all()
    return render_template("/faculty/view_adding.html", addsubject=addsubjects)"""
# adding.html page
@app.route('/faculty/view_adding_subject/get_subject_file/<int:subject_ID>')
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

    return mimetypes.get(file_extension, 'application/octet-stream')
#===========================================================#

"""# for overload applications
@app.route('/faculty/view_overload')
def view_overload():
    overload_applications = OverloadApplication.query.all()
    return render_template('/faculty/view_overload.html', overload_applications=overload_applications)
"""
# Redirect to download overload.html page
@app.route('/faculty/view_overload/get_overload_file/<int:overload_application_id>')
def get_overload_file(overload_application_id):
    return redirect(url_for('download_overload_file', overload_application_id=overload_application_id))

# Download overload file
@app.route('/faculty/download_overload_file/<int:overload_application_id>')
def download_overload_file(overload_application_id):
    overload_application = OverloadApplication.query.get(overload_application_id)

    if overload_application and overload_application.file_data:
        file_extension = get_file_extension(overload_application.file_filename)
        download_name = f'overload_{overload_application_id}.{file_extension}'

        return send_file(
            io.BytesIO(overload_application.file_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(file_extension),
        )
    else:
        abort(404)  # Overload application or file not found

def get_file_extension(file_filename):
    return file_filename.rsplit('.', 1)[1].lower()

def get_mimetype(file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(file_extension, 'application/octet-stream')

#=========================================================#

# for change of subjects and sched
"""@app.route('/faculty/view_change_of_subjects_sched')
def view_change_of_subjects_sched():
    changesubjects = ChangeOfSubjects.query.all()
    return render_template('/faculty/view_change.html', changesubjects=changesubjects)"""

# Redirect to download change of change.html
@app.route('/faculty/view_change_of_subjects_sched/get_change_file/<int:Changesubject_ID>')
def get_change_file(Changesubject_ID):
    return redirect(url_for('download_change_file', Changesubject_ID=Changesubject_ID))

# Download change of subjects file
@app.route('/faculty/download_change_file/<int:Changesubject_ID>')
def download_change_file(Changesubject_ID):
    changesubjects = ChangeOfSubjects.query.get(Changesubject_ID)

    if changesubjects and changesubjects.ace_form_data:
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

    return mimetypes.get(file_extension, 'application/octet-stream')

#===========================================================#
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
@app.route('/faculty/download_shifting_file/<int:shifting_application_id>')
def download_shifting_file(shifting_application_id):
    shifting_applications = ShiftingApplication.query.get(shifting_application_id)

    if shifting_applications and shifting_applications.file_data:
        file_extension = get_file_extension(shifting_applications.file_filename)
        download_name = f'shifting_applications_{shifting_application_id}.{file_extension}'

        return send_file(
            io.BytesIO(shifting_applications.file_data),
            as_attachment=True,
            download_name=download_name,
            mimetype=get_mimetype(file_extension),
        )
    else:
        abort(404)  # Change of subjects application or file not found

def get_file_extension(file_filename):
    return file_filename.rsplit('.', 1)[1].lower()

def get_mimetype(file_extension):
    mimetypes = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Add more file types as needed
    }

    return mimetypes.get(file_extension, 'application/octet-stream')
#===========================================================#
#certification
#===========================================================#
#correction
#===========================================================#
#crossenrollment
#===========================================================#
#enrollment
# ====================================================================== #petition
#===========================================================#
#tutorial
#===========================================================#

# ====================== ALL ADMIN ROUTES HERE========================== #
# ====================================================================== #
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
@app.route('/admin/createstudent/submit', methods=['GET', 'POST'])
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

    return render_template('/admin/create_student.html')


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
app.register_blueprint(admin_api, url_prefix='/api/v1/admin')
app.register_blueprint(faculty_api, url_prefix=faculty_api_base_url)
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