from datetime import datetime
import io
from multiprocessing import connection
from flask import Flask, abort, render_template, app, jsonify, redirect, request, flash, send_file, url_for, session
from flask_login import login_user
import requests
from models import CertificationRequest, ChangeOfSubjects, CrossEnrollment, Faculty, GradeEntry, ManualEnrollment, OverloadApplication, PetitionRequest, ShiftingApplication, TutorialRequest, db, Add_Subjects, init_db, Student
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import psycopg2
from sqlalchemy import Connection
#from models import Services
#from models import init_db

from Api.v1.student.api_routes import API_KEYS, student_api
from Api.v1.faculty.api_routes import faculty_api
from Api.v1.admin.api_routes import admin_api
# Assuming your Flask app is created as 'app'

import os
from dotenv import load_dotenv

from flask_jwt_extended import JWTManager

from decorators.auth_decorators import student_required, faculty_required, prevent_authenticated, admin_required, role_required



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


#=========================================================================
# TESTING AREA

#===========================================================================

@app.route('/')
def index():
    session.permanent = True
    return render_template('main/home.html')

#===========================================================================
# ROUTING FOR YOUR APPLICATION (http:localhost:3000)
@app.route('/')
@prevent_authenticated
def home():
    session.permanent = True
    return render_template('main/home.html')

@app.route('/logout')
def logout():
    # Clear session data including JWT token and user role
    session.clear()
    return redirect(url_for('studentLogin'))  # Redirect to home or appropriate route

# =======================================================================
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

#=======================================================================#

def upload_image():
    studentNumber = request.form['studentNumber']
    student = Student.query.filter_by(studentNumber=studentNumber).first()

    if student:
        image_file = request.files['image']
        if image_file:
            image_data = image_file.read()
            student.save_image(image_data)
            return 'Image uploaded successfully'
    
    return 'Error uploading image'
#=======================================================================#
# ========================================================================
#SERVICES
@app.route('/services/foroverloadofsubject')
def overload():
    return render_template("/services/subject_overload.html")

@app.route('/services/addingofsubject')
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

#========================================================================
# Define your allowed file function (you can customize it)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}
#========================================================================
# STUDENT
@app.route('/student/dashboard')
@role_required('student')
def student_dashboard():
    session.permanent=True
    return render_template('student/dashboard.html')

@app.route('/student/practice')
def student_practice():
    return render_template('/student/practice.html')

#==============================================================================================#
@app.route('/student/overload') #
def studentoverload():
    return render_template("/student/overload.html")# 


# Assuming your route for this page is '/submit_overload_application'
@app.route('/student/overload/submit_overload_application', methods=['POST'])
def submit_overload_application():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        # Fetch additional data for the given studentNumber
        student = Student.query.filter_by(studentNumber=studentNumber).first()

        if not student:
            flash('Student not found', 'danger')
            return redirect(url_for('stud_overload'))  # Replace 'stud_overload' with the actual route

        name = student.name  # Retrieve the name from the fetched student

        semester = request.form['semester']
        subjects_to_add = request.form['subjectsToAdd']
        justification = request.form['justification']
        user_responsible = request.form['user_responsible']
        status = request.form['status']

        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('stud_overload'))  # Replace 'stud_overload' with the actual route

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('stud_overload'))  # Replace 'stud_overload' with the actual route

        file_data = file.read()  # Read the file data
        file_filename = secure_filename(file.filename)

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not studentNumber or not semester or not subjects_to_add or not justification:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('stud_overload'))  # Replace 'stud_overload' with the actual route

        try:
            new_overload_application = OverloadApplication(
                name=name,
                studentNumber=studentNumber,
                semester=semester,
                subjects_to_add=subjects_to_add,
                justification=justification,
                file_filename=file_filename,
                file_data=file_data,
                user_responsible=user_responsible,
                status=status
            )

            db.session.add(new_overload_application)
            db.session.commit()
            flash('Overload application submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('studentoverload'))



#=============================================================================================================

# View function to retrieve and display the overload application details
"""@app.route('/student/foroverloadofsubject/view_overload/<int:overload_application_id>', methods=['GET'])
def view_overload(overload_application_id):
    overload_application = OverloadApplication.query.get(overload_application_id)
    if not overload_application:
        flash('Overload application not found.', 'danger')
        return redirect(url_for('stud_overload'))

    return render_template('view_overload.html', overload_application=overload_application)"""


@app.route('/student/foroverloadofsubject/edit_overload/<int:overload_application_id>', methods=['GET', 'POST'])
def edit_overload(overload_application_id):
    overload_application = OverloadApplication.query.get(overload_application_id)
    if not overload_application:
        flash('Overload application not found.', 'danger')
        return redirect(url_for('stud_overload'))

    if request.method == 'GET':
        return render_template('edit_overload.html', overload_application=overload_application)

    if request.method == 'POST':
        if 'submit' in request.form:  # Check if the "Submit" button was clicked
            name = request.form['name']
            studentNumber = request.form['studentNumber']
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

            overload_application.name = name
            overload_application.studentNumber = studentNumber
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
        else:  # Check if the "Cancel" button was clicked
            return redirect(url_for('stud_overload'))



#=============================================================================================================

@app.route('/student/subject')#
def studentaddingsubject():
    return render_template("/student/adding_of_subject.html")#

@app.route('/student/subject/added', methods=['POST'])
def add_subjects():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        name = request.form['name']
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student:
            name = student.name
        else:
            flash('Invalid student number.', 'danger')
            return redirect(url_for('add_subjects'))
        
        subject_Names = request.form['subject_Names']
        enrollment_type = request.form['enrollment_type']
        user_responsible = request.form['user_responsible']
        status = request.form['status']

        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('studentaddingsubject'))  # Replace 'add_subjects' with the actual route

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('studentaddingsubject'))  # Replace 'add_subjects' with the actual route

        file_data = file.read()  # Read the file data
        file_name = secure_filename(file.filename)

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not studentNumber or not name or not enrollment_type or not subject_Names:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('studentaddingsubject'))  # Replace 'add_subjects' with the actual route

        try:
            new_subject_application = Add_Subjects(
                studentNumber=studentNumber,
                name=name,
                subject_Names=subject_Names,
                enrollment_type=enrollment_type,
                file_name=file_name,
                file_data=file_data,
                user_responsible=user_responsible,
                status=status
            )

            db.session.add(new_subject_application)
            db.session.commit()
            flash('Subject application submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('studentaddingsubject')) 

#========================================================

@app.route('/student/service_service_form')#
def stud_services():
    return render_template("/student/service_request_form.html")#

"""@app.route('/student/submit_service_form/request', methods=['POST'])
def submit_services_request():
    # Retrieve form data and create a new Services object
    service_type = request.form.get('serviceType')
    student_id = request.form.get('studentID')
    name = request.form.get('name')

    # Add other fields based on your requirements

    # Create a new Services object
    new_service = Services(
        service_type=service_type,
        student_id=student_id,
        name=name,
        created_at=datetime.utcnow(),
        # Add other fields based on your requirements
    )

    # Save the new service request to the database
    db.session.add(new_service)
    db.session.commit()

    # Return a response (you can customize this based on your needs)
    return jsonify({'message': 'Service request submitted successfully!'})"""

@app.route('/student/submit_service_form/request', methods=['POST'])
def submit_services_request():
    if request.method == 'POST':
        service_type = request.form.get('serviceType')
        student_id = request.form.get('studentID')
        name = request.form.get('name')

        # Add other fields based on your requirements

        # Create a new Services object
        new_service = Services(
            service_type=service_type,
            student_id=student_id,
            name=name,
            created_at=datetime.utcnow(),
            # Add other fields based on your requirements
        )

        # Save the new service request to the database
        db.session.add(new_service)
        db.session.commit()

        # Return a response (you can customize this based on your needs)
        flash('Service request submitted successfully')

    return redirect(url_for('stud_services'))

#========================================================================#
@app.route('/student/changeofsubject')#
def studentchange():
    return render_template("/student/changeofsubject.html")#


@app.route('/student/changeofsubject/subject', methods=['POST'])
def change_of_subjects():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        name = request.form['name']
        enrollment_type = request.form['enrollment_type']
        user_responsible = request.form['user_responsible']
        status = request.form['status']

        # Check if ACE Form file is provided
        if 'ace_form_file' not in request.files:
            flash('No ACE Form file provided', 'danger')
            return redirect(request.url)

        ace_form_file = request.files['ace_form_file']
        # Check if the ACE Form file field is empty
        if ace_form_file.filename == '':
            flash('No ACE Form file selected', 'danger')
            return redirect(request.url)

        ace_form_data = ace_form_file.read()  # Read the ACE Form file data
        ace_form_filename = secure_filename(ace_form_file.filename)

        try:
            # Create a new change of subjects record with the retrieved student
            new_change_of_subjects = ChangeOfSubjects(
                studentNumber=studentNumber,
                name=name,
                enrollment_type=enrollment_type,
                ace_form_filename=ace_form_filename,
                ace_form_data=ace_form_data,
                created_at=datetime.utcnow(),
                updated_at=None,
                user_responsible=user_responsible,
                status=status
            )

            db.session.add(new_change_of_subjects)
            db.session.commit()
            flash('Change of Subjects Added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('studentchange'))

#==========================================================================================================================#

@app.route('/student/gradeentry')#
def studentcorrection():
    return render_template("/student/gradeentry.html")#

@app.route('/student/gradeentry/submit', methods=['POST'])
def submit_grade_correction():
    # Assuming you have the student ID stored in the session during login
    student_id = session.get('student_id')
    studentNumber = request.form['studentNumber']    
    name = request.form['name']
    application_type = request.form['application_type']

    # Additional logic here
    if not studentNumber or not name or not application_type:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return render_template('student/grade_entry.html')  # Replace with the actual template name

    files = {
        'completion_form': 'Completion Form',
        'class_record': 'Class Record',
        'affidavit': 'Affidavit'
    }

    for field, display_name in files.items():
        if field not in request.files:
            flash(f'No {display_name} file provided', 'danger')
            return redirect(request.url)

        file = request.files[field]
        if file.filename == '':
            flash(f'No {display_name} file selected', 'danger')
            return redirect(request.url)

        data = file.read()
        setattr(request, f'{field}_filename', secure_filename(file.filename))
        setattr(request, f'{field}_data', data)

    try:
        new_application = GradeEntry(
            student_id=student_id,  # Use the stored student 
            studentNumber=studentNumber,
            name=name,
            application_type=application_type,
            completion_form_filename=request.completion_form_filename,
            completion_form_data=request.completion_form_data,
            class_record_filename=request.class_record_filename,
            class_record_data=request.class_record_data,
            affidavit_filename=request.affidavit_filename,
            affidavit_data=request.affidavit_data,
            user_responsible=request.form.get('user_responsible'),  # Added user_responsible
            status=request.form.get('status'),  # Added status
            created_at=datetime.utcnow()
        )

        db.session.add(new_application)
        db.session.commit()
        flash('Grade correction application submitted successfully!', 'success')
        return redirect(url_for('studentcorrection'))  # Replace with the actual route name for grade correction
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/gradeentry.html')


#==============================================================================================================

@app.route('/student/crossenrollment')#
def studentenrollment():
    return render_template("/student/crossenrollment.html")#

@app.route('/student/crossenrollment/submitted', methods=['POST'])
@student_required  # Add any required authentication decorator
def submit_cross_enrollment():
    if request.method == 'POST':
        # Handle form submission
        try:
            # Process and save the form data
            new_cross_enrollment = create_cross_enrollment_from_form(request.form_data, request.files)
            db.session.add(new_cross_enrollment)
            db.session.commit()
            flash('Cross-Enrollment created successfully!', 'success')
            return redirect(url_for('studentenrollment'))  # Redirect to the appropriate route
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return render_template('student/crossenrollment.html')

def create_cross_enrollment_from_form(form_data, files):
    # Process form data and create a new CrossEnrollment instance
    studentNumber = form_data['studentNumber']
    name = form_data['name']
    school_for_cross_enrollment = form_data['school_for_cross_enrollment']
    total_number_of_units = int(form_data['total_number_of_units'])
    authorized_subjects_to_take = form_data['authorized_subjects_to_take']
    user_responsible = form_data.get('user_responsible')
    status = form_data.get('status')
    student_id = int(form_data.get('student_id'))  # Assuming you have a student_id in your form

    # Validate the form data as needed

    application_letter_file = files.get('application_letter_file')
    permit_to_cross_enroll_file = files.get('permit_to_cross_enroll_file')

    if not studentNumber or not name or not total_number_of_units <= 0 or not authorized_subjects_to_take:
        flash('Please fill out all fields and provide valid values.', 'danger')
        # Redirect or render the form again with an error message
        return redirect(url_for('studentenrollment'))

    if not application_letter_file or not permit_to_cross_enroll_file:
        flash('Please provide both application letter and permit to cross-enroll files.', 'danger')
        # Redirect or render the form again with an error message
        return redirect(url_for('studentenrollment'))

    # Process and save the file data
    application_letter_filename = secure_filename(application_letter_file.filename)
    application_letter_data = application_letter_file.read()

    permit_to_cross_enroll_filename = secure_filename(permit_to_cross_enroll_file.filename)
    permit_to_cross_enroll_data = permit_to_cross_enroll_file.read()

    # Create a new CrossEnrollment instance
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
        student_id=student_id,
    )

    return new_cross_enrollment

#==================================================================================================================================
#==================================================================================================================================
#===================Shifting===================#
@app.route('/student/shifting')#
def studentshifting():
    return render_template("/student/shifting.html")#

# Assuming your route for this page is '/submit_shifting_application'
@app.route('/student/shifting/submit', methods=['POST'])
def submit_shifting():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        name = request.form['name']
        current_program = request.form['currentProgram']
        residency_year = int(request.form['residencyYear'])
        intended_program = request.form['intendedProgram']
        qualifications = request.form['qualifications']
        user_responsible = request.form['user_responsible']
        status = request.form['status']

        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('studentshifting'))  # Replace 'your_shifting_page' with the actual route

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('studentshifting'))  # Replace 'your_shifting_page' with the actual route

        file_data = file.read()  # Read the file data
        file_filename = secure_filename(file.filename)

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not studentNumber or not name or not current_program or not residency_year or not intended_program:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('studentshifting'))  # Replace 'your_shifting_page' with the actual route

        try:
            new_shifting_application = ShiftingApplication(
                studentNumber=studentNumber,
                name=name,
                current_program=current_program,
                residency_year=residency_year,
                intended_program=intended_program,
                qualifications=qualifications,
                file_filename=file_filename,
                file_data=file_data,
                user_responsible=user_responsible,
                status=status,
            )

            db.session.add(new_shifting_application)
            db.session.commit()
            flash('Shifting application submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('studentshifting'))

#========================================================================================================================================
#================ManualEnrollment=================#
@app.route('/student/manualenrollment')#
def studentmanualenrollment():
    return render_template("/student/manualenrollment.html")#

@app.route('/student/manualenrollment/submit', methods=['POST'])
def submitmanualenrollment():
    studentNumber = request.form['studentNumber']
    name = request.form['name']
    enrollment_type = request.form['enrollment_type']
    reason = request.form['reason']

    # Check if the file is provided
    if 'me_file_data' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['me_file_data']
    # Check if the file field is empty
    if file.me_file_filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)

    file_data = file.read()  # Read the file data
    file_name = secure_filename(file.me_file_filename)

    try:
        new_manual_enrollment = ManualEnrollment(
            studentNumber=studentNumber,
            name=name,
            enrollment_type=enrollment_type,
            reason=reason,
            me_file_filename=file_name,
            me_file_data=file_data,
            user_responsible=request.form['user_responsible'],  # Adjust based on your form
            status=request.form['status']  # Adjust based on your form
        )

        db.session.add(new_manual_enrollment)
        db.session.commit()
        flash('Manual Enrollment submitted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return redirect(url_for('studentmanualenrollment'))


#====================================================================================================================================

@app.route('/student/onlinepetitionofsubject')
def studentpetition():  # Include the student_id parameter
    return render_template("/student/petition.html")

@app.route('/student/onlinepetitionofsubject/submit', methods=['GET', 'POST'])
def submitpetition():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        name = request.form['name']
        subject_code = request.form['subject_code']
        subject_name = request.form['subject_name']
        petition_type = request.form['petition_type']
        request_reason = request.form['request_reason']
        user_responsible = request.form['user_responsible']
        status = request.form['status']

        # Check if any of the required fields is empty
        if not studentNumber or not name or not subject_code or not subject_name or not petition_type or not request_reason or not user_responsible or not status:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('stud_petition', student_id=session['user_id']))
  # Replace 'stud_petition' with the actual route

        try:
            new_petition_request = PetitionRequest(
                studentNumber=studentNumber,
                name=name,
                subject_code=subject_code,
                subject_name=subject_name,
                petition_type=petition_type,
                request_reason=request_reason,
                user_responsible=user_responsible,
                status=status
            )

            db.session.add(new_petition_request)
            db.session.commit()
            flash('Petition submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return render_template("/student/petition.html")

#===============================================

@app.route('/student/onlinepetitionofsubject/<int:student_id>', methods=['GET'])
def view_student_petition(student_id):
    # Fetching the petitions based on the student_id
    petitions = PetitionRequest.query.filter_by(student_id=student_id).all()

    return render_template('view_petition_data.html', petitions=petitions)

#===================================================================================================================================#

@app.route('/student/tutorial')#
def studenttutorial():
    return render_template("/student/tutorial.html")#

#done
# Assuming your route for this page is '/submit_tutorial'
@app.route('/student/tutorial/submit', methods=['POST'])
def submittutorialrequest():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        name = request.form['name']
        subject_code = request.form['subject_code']
        subject_name = request.form['subject_name']
        
        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('stude_tutorial'))  # Replace 'stude_tutorial' with the actual route

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('studenttutorial'))  # Replace 'stude_tutorial' with the actual route

        file_data = file.read()  # Read the file data
        file_filename = secure_filename(file.filename)

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not studentNumber or not name or not subject_code or not subject_name:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('studenttutorial'))  # Replace 'stude_tutorial' with the actual route

        try:
            new_tutorial_request = TutorialRequest(
                studentNumber=studentNumber,
                name=name,
                subject_code=subject_code,
                subject_name=subject_name,
                file_filename=file_filename,
                file_data=file_data,
                user_responsible=request.form.get('user_responsible'),
                status=request.form.get('status')
            )

            db.session.add(new_tutorial_request)
            db.session.commit()
            flash('Tutorial request submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('studenttutorial'))
  # Redirect to the tutorial request page after submission

#====================================================================================================================
@app.route('/student/certification')#
def studentcertification():
    return render_template("/student/certification.html")#

@app.route('/student/profile')
def studentprofile():
    return render_template("/student/profile.html", student_api_base_url=student_api_base_url)

@app.route('/student/submitcertificationrequest', methods=['POST'])
def submitcertification():
    if request.method == 'POST':
        # Retrieve form data
        studentNumber = request.form.get('studentNumber')
        name = request.form.get('name')
        certification_type = request.form.get('certification_type')

        # Check file uploads
        request_form_file = request.files['requestForm']
        identification_card_file = request.files['identificationCard']

        if request_form_file.filename == '' or identification_card_file.filename == '':
            flash('Please select files for Request Form and Identification Card')
            return redirect(request.url)

        # Read file data
        request_form_data = request_form_file.read()
        identification_card_data = identification_card_file.read()

        is_representative = request.form.get('is_representative') == 'on'

        try:
            new_request = CertificationRequest(
                studentNumber=studentNumber,
                name=name,
                certification_type=certification_type,
                request_form_filename=secure_filename(request_form_file.filename),
                request_form_data=request_form_data,
                identification_card_filename=secure_filename(identification_card_file.filename),
                identification_card_data=identification_card_data,
                is_representative=is_representative,
                created_at=datetime.utcnow()
            )

            if is_representative:
                # Handle representative files
                authorization_letter_file = request.files['authorizationLetter']
                representative_id_file = request.files['representativeID']

                if authorization_letter_file.filename == '' or representative_id_file.filename == '':
                    flash('Please select files for Authorization Letter and Representative ID')
                    return redirect(request.url)

                authorization_letter_data = authorization_letter_file.read()
                representative_id_data = representative_id_file.read()

                new_request.authorization_letter_filename = secure_filename(authorization_letter_file.filename)
                new_request.authorization_letter_data = authorization_letter_data
                new_request.representative_id_filename = secure_filename(representative_id_file.filename)
                new_request.representative_id_data = representative_id_data

            new_request.user_responsible = request.form.get('user_responsible')
            new_request.status = request.form.get('status')

            db.session.add(new_request)
            db.session.commit()
            flash('Certification request submitted successfully')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
        finally:
            db.session.close()

    return redirect(url_for('studentcertification'))

#============================================================================================================================
"""@app.route('/student/submit_service_request', methods=['GET'])
def submit_service_request():
    return render_template('service_request_form.html')"""


@app.route('/student/submit_service_request/request', methods=['POST'], endpoint='submit_services_request_form')
def submit_services_request():
    if request.method == 'POST':
        service_type = request.form.get('serviceType')
        student_id = request.form.get('studentID')
        name = request.form.get('name')

        # Add other fields based on your requirements

        # Create a new Services object
        new_service = Services(
            service_type=service_type,
            student_id=student_id,
            name=name,
            created_at=datetime.utcnow(),
            # Add other fields based on your requirements
        )

        # Save the new service request to the database
        db.session.add(new_service)
        db.session.commit()

        # Return a response (you can customize this based on your needs)
        flash('Service request submitted successfully')

    return redirect(url_for('stud_services'))

#===========================================================#
#======================View_Compilation=====================#
#===========================================================#

# ========================================================================
#SERVICES
@app.route('/faculty/overload')
def facultyoverload():
    return render_template("/faculty/overload.html")

@app.route('/faculty/adding')
def facultyadding():
    return render_template("/faculty/adding.html")

@app.route('/faculty/change')
def facultychange():
    return render_template("/faculty/change.html")

@app.route('/faculty/correction')
def facultycorrection():
    return render_template("/faculty/correction.html")

@app.route('/faculty/crossenrollment')
def facultycrossenrollment():
    return render_template("/faculty/crossenrollment.html")

@app.route('/faculty/shifting')
def facultyshifting():
    return render_template("/faculty/shifting.html")

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
# ALL STUDENT ROUTES HERE
@app.route('/student')
@prevent_authenticated
def studentLogin():
    session.permanent = True
    return render_template('student/login.html')

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
@app.route('/student/login_addsubjects', methods=['GET', 'POST'])
@prevent_authenticated
def portal_addingofsubject():
    session.permanent = True

    # If the request method is POST, attempt to log in
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        # Use the common login function
        return login_user(studentNumber, password, 'student_portal_addingsubject', 'portal_addingofsubject')

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



# Function to fetch student details by student ID
def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
            'userImg': student.userImg,
        }
        return student_details
    else:
        return None

"""# Modify the profile route
@app.route('/student/home/profile')
def profile():
    session.update()

    # Replace the static student_id with the actual student ID you want to retrieve
    student_id = session.get("user_id")
    student = Student.query.get(student_id)

    if student:
        # Fetch additional student details
        student_details = get_student_details(student_id)

        if student_details:
            return render_template('student/profile.html', student_details=student_details)
        else:
            # Handle the case where student details are not found
            return "Student details not found", 404

    else:
        # Handle the case where the student is not found
        return "Student not found", 404"""
#def store_user_details_in_session(student):
    # Store user details in the session
#    session['user_id'] = student.student_id
#    session['studentNumber'] = student.studentNumber
#    session['name'] = student.name
#    session['gender'] = student.gender
#    session['email'] = student.email
#    session['address'] = student.address
#    session['dateofBirth'] = student.dateofBirth
#    session['placeofBirth'] = student.placeofBirth
#    session['mobileNumber'] = student.mobileNumber
#    session['userImg'] = student.userImg





# ========================================================================
#Student directly Services

# Overload subjects function for students
@app.route('/student/foroverloadofsubject')
def student_portal_overload():
    session.permanent = True
    if is_user_logged_in_overload():
        return render_template('student/subject_overload.html')
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_overload'))

# Function to check if the user is logged in
def is_user_logged_in_overload():
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_overload')
def redirect_based_on_login_overload():
    if is_user_logged_in_overload():
        return redirect(url_for('student_portal_overload'))
    else:
        return redirect(url_for('portal_overload'))

#================================================================
# Certification function for students
@app.route('/student/certification')
def student_portal_certification():
    session.permanent = True
    if is_user_logged_in_certification():
        return render_template('student/certification.html')
    
def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_certification')
def redirect_based_on_login_certification():
    if is_user_logged_in_certification():
        return redirect(url_for('student_portal_certification'))
    else:
        return redirect(url_for('portal_certification'))
#========================================================================
# Change of subject or sched function for students
@app.route('/student/changeofsubject/schedule')
def student_portal_changesubsched():
    session.permanent = True
    if is_user_logged_in_changesubsched():
        return render_template('student/change_of_subject.html')
    
def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_changesubsched')
def redirect_based_on_login_changesubsched():
    if is_user_logged_in_certification():
        return redirect(url_for('student_portal_changesubsched'))
    else:
        return redirect(url_for('portal_changesubsched'))
#========================================================================
# Enrollment function for students
@app.route('/student/manualenrollment')
def student_portal_enrollment():
    session.permanent = True
    if is_user_logged_in_enrollment():
        return render_template('student/manual_enrollment.html')

def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_enrollment')
def redirect_based_on_login_enrollment():
    if is_user_logged_in_enrollment():
        return redirect(url_for('student_portal_enrollment'))
    else:
        return redirect(url_for('portal_enrollment'))

#========================================================================

# addingsubject subjects function for students
@app.route('/student/addingofsubject')
def student_portal_addingsubject():
    session.permanent = True
    service_redirect = 'student_portal_addingsubject'
    service_portal = 'portal_addingofsubject'

    # Use the common login check
    if is_user_logged_in_addingofsubject(service_redirect):
        return render_template('student/adding_of_subject.html', student_details=session)

    # Redirect to the login page if not logged in
    return redirect(url_for('redirect_based_on_login', service_redirect=service_redirect, service_portal=service_portal))


# Function to check if the user is logged in
def is_user_logged_in_addingofsubject(service_redirect):
    session.permanent = True
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("student_id") is not None


# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_addingofsubject')
def redirect_based_on_login_addingofsubject():
    service_redirect = 'student_portal_addingsubject'
    service_portal = 'portal_addingofsubject'

    # Use the common login redirection
    if is_user_logged_in_addingofsubject(service_redirect):
        return redirect(url_for(service_portal, student_details=session))
    else:
        return redirect(url_for('portal_addingofsubject'))


#================================================================
# shifting function for students
@app.route('/student/shifting')
def student_portal_shifting():
    session.permanent = True
    if is_user_logged_in_shifting():
        return render_template('student/shifting.html')
    
def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_shifting')
def redirect_based_on_login_shifting():
    if is_user_logged_in_shifting():
        return redirect(url_for('student_portal_shifting'))
    else:
        return redirect(url_for('portal_shifting'))


#========================================================================

# tutorial subjects function for students
@app.route('/student/requestfortutorialofsubjects')
def student_portal_tutorial():
    session.permanent = True
    if is_user_logged_in_tutorial():
        return render_template('student/tutorial.html')
    
def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_tutorial')
def redirect_based_on_login_tutorial():
    if is_user_logged_in_tutorial():
        return redirect(url_for('student_portal_tutorial'))
    else:
        return redirect(url_for('portal_tutorial'))

#================================================================
# online petition subjects function for students
@app.route('/student/onlinepetitionofsubject')
def student_portal_petition():
    session.permanent = True
    if is_user_logged_in_petition():
        return render_template('student/petition.html')
    
def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_petition')
def redirect_based_on_login_petition():
    if is_user_logged_in_petition():
        return redirect(url_for('student_portal_petition'))
    else:
        return redirect(url_for('portal_petition'))
    
#================================================================
# gradeentry function for students
@app.route('/student/gradeentry')
def student_portal_gradeentry():
    session.permanent = True
    if is_user_logged_in_gradeentry():
        return render_template('student/grade_entry.html')

def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_gradeentry')
def redirect_based_on_login_gradeentry():
    if is_user_logged_in_gradeentry():
        return redirect(url_for('student_portal_gradeentry'))
    else:
        return redirect(url_for('portal_gradeentry'))

#================================================================
# gradeentry function for students
@app.route('/student/crossenrollment')
def student_portal_crossenrollment():
    session.permanent = True
    if is_user_logged_in_crossenrollment():
        return render_template('student/cross_enrollment.html')
    # Function to fetch student details by student ID
def get_student_details(student_id):
    student = Student.query.get(student_id)

    if student:
        student_details = {
            'studentNumber': student.studentNumber,
            'name': student.name,
            'gender': student.gender,
            'email': student.email,
            'address': student.address,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
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
    return session.get("student_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_crossenrollment')
def redirect_based_on_login_crossenrollment():
    if is_user_logged_in_gradeentry():
        return redirect(url_for('student_portal_crossenrollment'))
    else:
        return redirect(url_for('portal_crossenrollment'))

#================================================================#
# crossenrollment function for teachers
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

# Updated view function
@app.route('/faculty/view_adding_subject')
def view_adding_subject():
    subjects = Add_Subjects.query.all()
    return render_template("/faculty/view_adding.html", subjects=subjects)

@app.route('/faculty/view_adding_subject/get_subject_file/<int:subject_ID>')
def get_subject_file(subject_ID):
    return redirect(url_for('download_subject_file', subject_ID=subject_ID))

#download the file in the view page
@app.route('/student/download_subject_file/<int:subject_ID>')
def download_subject_file(subject_ID):
    subject = Add_Subjects.query.get(subject_ID)

    if subject and subject.file_data:
        file_extension = get_file_extension(subject.file_name)
        download_name = f'subject_{subject_ID}.{file_extension}'

        return send_file(
            io.BytesIO(subject.file_data),
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

# for overload applications
@app.route('/faculty/view_overload')
def view_overload():
    overload_applications = OverloadApplication.query.all()
    return render_template('/faculty/view_overload.html', overload_applications=overload_applications)

# Redirect to download overload file
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
@app.route('/faculty/view_change_of_subjects_sched')
def view_change_of_subjects_sched():
    changesubjects = ChangeOfSubjects.query.all()
    return render_template('/faculty/view_change.html', changesubjects=changesubjects)

# Redirect to download change of subjects file
@app.route('/faculty/view_change_of_subjects_sched/get_change_file/<int:Changesubject_ID>')
def get_change_file(Changesubject_ID):
    return redirect(url_for('download_change_file', Changesubject_ID=Changesubject_ID))

# Download change of subjects file
@app.route('/faculty/download_change_file/<int:Changesubject_ID>')
def download_change_file(Changesubject_ID):
    changesubject = ChangeOfSubjects.query.get(Changesubject_ID)

    if changesubject and changesubject.ace_form_data:
        file_extension = get_file_extension(changesubject.ace_form_filename)
        download_name = f'change_subject_{Changesubject_ID}.{file_extension}'

        return send_file(
            io.BytesIO(changesubject.ace_form_data),
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

# ====================================================================== #
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


# Route to handle student creation with image upload
@app.route('/admin/create_student', methods=['GET', 'POST'])
def admin_create_student():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        gender = request.form['gender']
        date_of_birth = request.form['dateOfBirth']
        place_of_birth = request.form['placeOfBirth']
        mobile_number = request.form['mobileNumber']

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the student already exists
        existing_student = Student.query.filter_by(studentNumber=studentNumber).first()
        if existing_student:
            return 'Student with this student number already exists'

        # Handle image upload
        image_file = request.files['image']
        image_data = image_file.read() if image_file else None

        # Create a new student
        new_student = Student(
            studentNumber=studentNumber,
            name=name,
            email=email,
            password=hashed_password,
            address=address,
            gender=gender,
            dateofBirth=date_of_birth,
            placeofBirth=place_of_birth,
            mobileNumber=mobile_number,
        )

        # Save the image data
        if image_data:
            new_student.save_image(image_data)

        db.session.add(new_student)
        db.session.commit()

        return 'Student created successfully'

    return render_template("/admin/create_student.html")

@app.route('/admin/student_list', methods=['GET'])
def student_list():
    # Fetch all students from the database
    students = Student.query.all()

    # Convert the list of students to a list of dictionaries for rendering
    students_data = [
        {
            'student_id': student.student_id,
            'studentNumber': student.studentNumber,
            'name': student.name,
            'email': student.email,
            'address': student.address,
            'gender': student.gender,
            'dateofBirth': student.dateofBirth,
            'placeofBirth': student.placeofBirth,
            'mobileNumber': student.mobileNumber,
            'userImg': student.userImg
        }
        for student in students
    ]

    return render_template("/admin/student_list.html", students=students_data)

"""@app.route('/admin/student_list')
def student_list():
    api_key = request.headers.get('X-Api-Key')  # Get the API key from the request header

    if not api_key or api_key not in API_KEYS.values():
        return render_template("/admin/student_list.html", students=[], message="Invalid API key")

    try:
        # Fetch all students from the database
        students = Student.query.all()

        # Render the template with the student data from the database
        return render_template("/admin/student_list.html", students=students, message="You got data from the database")

    except Exception as e:
        print("Exception during database query:", e)
        return render_template("/admin/student_list.html", students=[], message="Error fetching data from the database")"""

"""# Route to display the list of students in HTML
@app.route('/admin/student_list')
def student_list():
    api_key = request.headers.get('X-Api-Key')  # Get the API key from the request header

    if not api_key or api_key not in API_KEYS.values():
        return render_template("/admin/student_list.html", students=[], message="Invalid API key")

    try:
        # Fetch data from the API endpoint
        response = requests.get('http://your-api-url/student_list', headers={'X-Api-Key': api_key})
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        api_data = response.json()

        if response.status_code == 200 and api_data.get('message') == 'You got API data':
            # Render the template with the student data from the API
            return render_template("/admin/student_list.html", students=api_data.get('students'))
        else:
            return render_template("/admin/student_list.html", students=[], message="Error: {}".format(api_data.get('message')))

    except requests.exceptions.RequestException as e:
        print("Exception during API request:", e)
        return render_template("/admin/student_list.html", students=[], message="Error fetching data from API")"""



"""@app.route('/admin/view_student/<int:student_id>')
def view_student(student_id):
    # Assuming you have a function to get student details from the database
    student = get_student_details(student_id)

    # Replace 'path_to_your_image.jpg' with the actual path to the student's profile image
    image_path = 'path_to_your_image.jpg'

    return render_template("path_to_your_template.html", student=student, image_path=image_path)"""#for single profile needed 
                                                                                                   #html is in the view_student naka comment


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
    students = Student.query.all()

    student_list = []
    for student in students:
        student_data = {
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'password': student.password
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