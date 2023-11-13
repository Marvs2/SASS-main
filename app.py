from datetime import datetime
from multiprocessing import connection
from flask import Flask, render_template, jsonify, redirect, request, flash, send_file, url_for, session
from models import CertificationRequest, ChangeOfSubjects, CrossEnrollment, GradeEntry, ManualEnrollment, OverloadApplication, PetitionRequest, ShiftingApplication, TutorialRequest, db, Add_Subjects, init_db, Student
from werkzeug.utils import secure_filename
import psycopg2
from sqlalchemy import Connection
from models import Services

from Api.v1.student.api_routes import student_api  
from Api.v1.faculty.api_routes import faculty_api
from Api.v1.admin.api_routes import admin_api

import os
from dotenv import load_dotenv

from flask_jwt_extended import JWTManager

from decorators.auth_decorators import student_required, faculty_required, prevent_authenticated, admin_required

faculty_base_api_url = os.getenv('FACULTY_BASE_URL')

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
# SETUP YOUR POSTGRE DATABASE HERE
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour (in seconds)
app.secret_key = os.getenv('SECRET_KEY')  # Replace 'your-secret-key' with an actual secret key

jwt = JWTManager(app)
init_db(app)

@app.context_processor
def custom_context_processor():
    authenticated = False
    if 'user_role' in session:
        authenticated = True
    return {'authenticated': authenticated}


#=========================================================================
# TESTING AREA
"""# Login function for students
@app.route('/student/foroverloadofsubject')
def student_overload():
    session.permanent = True
    # Check if the user is logged in
    if is_user_logged_in():
        # If logged in, render the overload subject page
        return render_template('student/subject_overload.html')
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('student_portal'))
# Login function for students
@app.route('/student/foroverloadofsubject')
def student_portal_overload():
    session.permanent = True
    return render_template('student/login/subject_overload.html')
# Link for overload of subject
@app.route('/student/foroverloadofsubject')
def stud_overload():
    return render_template("/student/subject_overload.html")

# Function to check if the user is logged in
def is_user_logged_in():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login')
def redirect_based_on_login():
    if is_user_logged_in():
        return redirect(url_for('stud_overload'))
    else:
        return redirect(url_for('student_portal'))
"""

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
    return redirect(url_for('student_portal'))  # Redirect to home or appropriate route

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
def stud_dashboard():
    return render_template('/student/dashboard.html')

@app.route('/student/foroverloadofsubject') #
def stud_overload():
    return render_template("/student/subject_overload.html")# 

# Assuming your route for this page is '/submit_overload_application'
@app.route('/submit_overload_application', methods=['POST'])
def submit_overload_application():
    if request.method == 'POST':
        student_id = request.form['studentID']
        student_name = request.form['studentName']
        semester = request.form['semester']
        subjects_to_add = request.form['subjectsToAdd']
        justification = request.form['justification']
        
        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('your_overload_page'))  # Replace 'your_overload_page' with the actual route

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('your_overload_page'))  # Replace 'your_overload_page' with the actual route

        file_data = file.read()  # Read the file data
        file_filename = secure_filename(file.filename)

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not student_id or not student_name or not semester or not subjects_to_add or not justification:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('stud_overload'))  # Replace 'your_overload_page' with the actual route

        try:
            new_overload_application = OverloadApplication(
                student_id=student_id,
                student_name=student_name,
                semester=semester,
                subjects_to_add=subjects_to_add,
                justification=justification,
                file_filename=file_filename,
                file_data=file_data
            )

            db.session.add(new_overload_application)
            db.session.commit()
            flash('Overload application submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('stud_overload'))

@app.route('/student/addingofsubject')#
def stud_adding():
    return render_template("/student/adding_of_subject.html")#

@app.route('/student/addingofsubject/add_subjects', methods=['POST'])
def add_subjects():
    if request.method == 'POST':
        student_number = request.form['student_number']
        student_name = request.form['student_name']
        subject_names = request.form['subject_Names']  # Get the subject names as a single string
        enrollment_type = request.form['enrollment_type']

        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        file_data = file.read()  # Read the file data
        file_name = secure_filename(file.filename)

        try:
            new_subject = Add_Subjects(
                student_number=student_number,
                student_name=student_name,
                subject_Names=subject_names,  # Assign the whole string to subject_Names
                enrollment_type=enrollment_type,
                file_data=file_data,
                file_name=file_name
            )

            db.session.add(new_subject)
            db.session.commit()
            flash('Subject Added successfully')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
        finally:
            db.session.close()

    return redirect(url_for('stud_adding'))


@app.route('/student/service_service_form')#
def stud_services():
    return render_template("/student/service_request_form.html")#

"""@app.route('/student/submit_service_form/request', methods=['POST'])
def submit_services_request():
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
@app.route('/student/submit_service_form/request', methods=['POST'])
def submit_services_request():
    if request.method == 'POST':
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
        flash('Service request submitted successfully')

    return redirect(url_for('stud_services'))

@app.route('/student/changeofsubject/schedule')#
def stud_change():
    return render_template("/student/change_of_subject.html")#


@app.route('/student/changeofsubject/schedule/changeofsuborsched', methods=['POST'])
def change_of_subjects():
    if request.method == 'POST':
        student_number = request.form['student_number']
        student_name = request.form['student_name']
        enrollment_type = request.form['enrollment_type']

        # Check if ACE Form file is provided
        if 'aceForm' not in request.files:
            flash('No ACE Form file provided')
            return redirect(request.url)

        ace_form_file = request.files['aceForm']
        # Check if the ACE Form file field is empty
        if ace_form_file.filename == '':
            flash('No ACE Form file selected')
            return redirect(request.url)

        ace_form_data = ace_form_file.read()  # Read the ACE Form file data
        ace_form_filename = secure_filename(ace_form_file.filename)

        try:
            new_change_of_subjects = ChangeOfSubjects(
                student_number=student_number,
                student_name=student_name,
                enrollment_type=enrollment_type,
                ace_form_filename=ace_form_filename,
                ace_form_data=ace_form_data
            )

            db.session.add(new_change_of_subjects)
            db.session.commit()
            flash('Change of Subjects Added successfully')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
        finally:
            db.session.close()

    return redirect(url_for('stud_change'))


@app.route('/student/gradeentry')#
def stud_correction():
    return render_template("/student/grade_entry.html")#

@app.route('/student/submit_grade_correction', methods=['POST'])
def submit_grade_correction():
    student_id = request.form['studentID']
    student_name = request.form['studentName']
    application_type = request.form['applicationType']

    # Additional validation logic can be added here

    if not student_id or not student_name or not application_type:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return render_template('student/grade_correction.html')  # Replace with the actual template name

    # Check if Completion Form file is provided
    if 'completionForm' not in request.files:
        flash('No Completion Form file provided')
        return redirect(request.url)

    completion_form_file = request.files['completionForm']
    # Check if the Completion Form file field is empty
    if completion_form_file.filename == '':
        flash('No Completion Form file selected')
        return redirect(request.url)

    completion_form_data = completion_form_file.read()  # Read the Completion Form file data
    completion_form_filename = secure_filename(completion_form_file.filename)

    # Check if Class Record file is provided
    if 'classRecord' not in request.files:
        flash('No Class Record file provided')
        return redirect(request.url)

    class_record_file = request.files['classRecord']
    # Check if the Class Record file field is empty
    if class_record_file.filename == '':
        flash('No Class Record file selected')
        return redirect(request.url)

    class_record_data = class_record_file.read()  # Read the Class Record file data
    class_record_filename = secure_filename(class_record_file.filename)

    # Check if Affidavit file is provided
    if 'affidavit' not in request.files:
        flash('No Affidavit file provided')
        return redirect(request.url)

    affidavit_file = request.files['affidavit']
    # Check if the Affidavit file field is empty
    if affidavit_file.filename == '':
        flash('No Affidavit file selected')
        return redirect(request.url)

    affidavit_data = affidavit_file.read()  # Read the Affidavit file data
    affidavit_filename = secure_filename(affidavit_file.filename)

    try:
        new_application = GradeEntry(
            student_id=student_id,
            student_name=student_name,
            application_type=application_type,
            completion_form_filename=completion_form_filename,
            completion_form_data=completion_form_data,
            class_record_filename=class_record_filename,
            class_record_data=class_record_data,
            affidavit_filename=affidavit_filename,
            affidavit_data=affidavit_data
        )

        db.session.add(new_application)
        db.session.commit()
        flash('Grade correction application submitted successfully!', 'success')
        return redirect(url_for('stud_correction'))  # Replace with the actual route name for grade correction
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/grade_entry.html') 

@app.route('/student/crossenrollment')#
def stud_cross_enrollment():
    return render_template("/student/cross_enrollment.html")#

@app.route('/student/submit_cross_enrollment', methods=['POST'])
def submit_cross_enrollment():
    student_id = request.form['studentID']
    student_name = request.form['studentName']
    school_for_cross_enrollment = request.form['crossEnrollmentSchool']
    total_units = int(request.form['crossEnrollmentUnits'])
    authorized_subjects = request.form['authorizedSubjects']

    # Additional validation logic can be added here

    if not student_id or not student_name or not school_for_cross_enrollment or total_units <= 0 or not authorized_subjects:
        flash('Please fill out all fields and provide valid values.', 'danger')
        return render_template('student/cross_enrollment.html')  # Replace with the actual template name

    # Check if ACE Form file is provided
    if 'applicationLetter' not in request.files:
        flash('No Application Letter file provided')
        return redirect(request.url)

    application_letter_file = request.files['applicationLetter']
    # Check if the Application Letter file field is empty
    if application_letter_file.filename == '':
        flash('No Application Letter file selected')
        return redirect(request.url)

    application_letter_data = application_letter_file.read()  # Read the Application Letter file data
    application_letter_filename = secure_filename(application_letter_file.filename)

    # Check if Permit to Cross-Enroll file is provided
    if 'permitToCrossEnroll' not in request.files:
        flash('No Permit to Cross-Enroll file provided')
        return redirect(request.url)

    permit_to_cross_enroll_file = request.files['permitToCrossEnroll']
    # Check if the Permit to Cross-Enroll file field is empty
    if permit_to_cross_enroll_file.filename == '':
        flash('No Permit to Cross-Enroll file selected')
        return redirect(request.url)

    permit_to_cross_enroll_data = permit_to_cross_enroll_file.read()  # Read the Permit to Cross-Enroll file data
    permit_to_cross_enroll_filename = secure_filename(permit_to_cross_enroll_file.filename)

    try:
        new_cross_enrollment = CrossEnrollment(
            student_id=student_id,
            student_name=student_name,
            school_for_cross_enrollment=school_for_cross_enrollment,
            total_number_of_units=total_units,
            authorized_subjects_to_take=authorized_subjects,
            application_letter_filename=application_letter_filename,
            permit_to_cross_enroll_filename=permit_to_cross_enroll_filename,
        )

        db.session.add(new_cross_enrollment)
        db.session.commit()
        flash('Cross-Enrollment application submitted successfully!', 'success')
        return redirect(url_for('stud_cross_enrollment'))  # Replace with the actual route name for cross-enrollment
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return render_template('student/cross_enrollment.html')  # Replace with the actual template name

#==================================================================================================================================
#==================================================================================================================================
#===================Shifting===================#
@app.route('/student/shifting')#
def stud_shifting():
    return render_template("/student/shifting.html")#

# Assuming your route for this page is '/submit_shifting_application'
@app.route('/submit_shifting_application', methods=['POST'])
def submit_shifting_application():
    if request.method == 'POST':
        student_id = request.form['studentID']
        student_name = request.form['studentName']
        current_program = request.form['currentProgram']
        residency_year = int(request.form['residencyYear'])
        intended_program = request.form['intendedProgram']
        qualifications = request.form['qualifications']
        
        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('your_shifting_page'))  # Replace 'your_shifting_page' with the actual route

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('your_shifting_page'))  # Replace 'your_shifting_page' with the actual route

        file_data = file.read()  # Read the file data
        file_filename = secure_filename(file.filename)

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not student_id or not student_name or not current_program or not residency_year or not intended_program:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('your_shifting_page'))  # Replace 'your_shifting_page' with the actual route

        try:
            new_shifting_application = ShiftingApplication(
                student_id=student_id,
                student_name=student_name,
                current_program=current_program,
                residency_year=residency_year,
                intended_program=intended_program,
                qualifications=qualifications,
                file_filename=file_filename,
                file_data=file_data
            )

            db.session.add(new_shifting_application)
            db.session.commit()
            flash('Shifting application submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('stud_shifting'))
#========================================================================================================================================
#================ManualEnrollment=================#
@app.route('/student/manualenrollment')#
def stud_enrollment():
    return render_template("/student/manual_enrollment.html")#

@app.route('/submit_manual_enrollment', methods=['POST'])
def submit_manual_enrollment():
    student_number = request.form['studentNumber']
    student_name = request.form['studentName']
    enrollment_type = request.form['enrollmentType']
    reason = request.form['reason']

    # Check if the file is provided
    if 'meFile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['meFile']
    # Check if the file field is empty
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    file_data = file.read()  # Read the file data
    file_name = secure_filename(file.filename)

    try:
        new_manual_enrollment = ManualEnrollment(
            student_number=student_number,
            student_name=student_name,
            enrollment_type=enrollment_type,
            reason=reason,
            me_file_filename=file_name,
            me_file_data=file_data,
            user_role='student'  # Set the user role (you can adjust this based on your authentication logic)
        )

        db.session.add(new_manual_enrollment)
        db.session.commit()
        flash('Manual Enrollment submitted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.session.close()

    return redirect(url_for('stud_enrollment'))

#====================================================================================================================================

@app.route('/student/onlinepetitionofsubject')#
def stud_petition():
    return render_template("/student/petition.html")#

# Assuming your route for this page is '/submit_petition'
@app.route('/student/onlinepetitionofsubject/submit_petition', methods=['POST'])
def submit_petition():
    if request.method == 'POST':
        student_id = request.form['studentID']
        student_name = request.form['studentName']
        subject_code = request.form['subjectCode']
        subject_name = request.form['subjectName']
        petition_type = request.form['petitionType']  # Assuming you added a dropdown with name 'petitionType' in your HTML form
        request_reason = request.form['requestReason']

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not student_id or not student_name or not subject_code or not subject_name or not petition_type or not request_reason:
            flash('Please fill out all fields.', 'danger')
            return redirect(url_for('stud_petition'))  # Replace 'your_petition_page' with the actual route

        try:
            new_petition = PetitionRequest(
                student_id=student_id,
                student_name=student_name,
                subject_code=subject_code,
                subject_name=subject_name,
                petition_type=petition_type,
                request_reason=request_reason
            )

            db.session.add(new_petition)
            db.session.commit()
            flash('Petition submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('stud_petition'))
#====================================================================================================================================

@app.route('/student/requestfortutorialofsubjects')#
def stud_tutorial():
    return render_template("/student/tutorial.html")#

# Assuming your route for this page is '/submit_tutorial_request'
@app.route('/submit_tutorial_request', methods=['POST'])
def submit_tutorial_request():
    if request.method == 'POST':
        student_id = request.form['studentID']
        student_name = request.form['studentName']
        subject_code = request.form['subjectCode']
        subject_name = request.form['subjectName']
        
        # Check if a file is provided
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('stude_tutorial'))  # Replace 'stude_tutorial' with the actual route

        file = request.files['file']
        # Check if the file field is empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('stude_tutorial'))  # Replace 'stude_tutorial' with the actual route

        file_data = file.read()  # Read the file data
        file_filename = secure_filename(file.filename)

        # Additional validation logic can be added here

        # Check if any of the required fields is empty
        if not student_id or not student_name or not subject_code or not subject_name:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('stude_tutorial'))  # Replace 'stude_tutorial' with the actual route

        try:
            new_tutorial_request = TutorialRequest(
                student_id=student_id,
                student_name=student_name,
                subject_code=subject_code,
                subject_name=subject_name,
                file_filename=file_filename,
                file_data=file_data
            )

            db.session.add(new_tutorial_request)
            db.session.commit()
            flash('Tutorial request submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('stude_tutorial'))  # Redirect to the tutorial request page after submission


@app.route('/student/certification')#
def stud_certification():
    return render_template("/student/certification.html")#

@app.route('/student/submit_certification_request', methods=['POST'])
def submit_certification_request():
    if request.method == 'POST':
        student_id = request.form.get('studentID')
        student_name = request.form.get('studentName')
        certification_type = request.form.get('certificationType')

        # Check if a file is provided
        if 'requestForm' not in request.files or 'identificationCard' not in request.files:
            flash('Please provide both Request Form and Identification Card files')
            return redirect(request.url)

        request_form_file = request.files['requestForm']
        identification_card_file = request.files['identificationCard']

        # Check if the file fields are empty
        if request_form_file.filename == '' or identification_card_file.filename == '':
            flash('Please select files for both Request Form and Identification Card')
            return redirect(request.url)

        request_form_data = request_form_file.read()
        identification_card_data = identification_card_file.read()

        is_representative = request.form.get('isRepresentative') == 'on'

        if is_representative:
            # If there is a representative, handle the representative files
            authorization_letter_file = request.files['authorizationLetter']
            representative_id_file = request.files['representativeID']

            # Check if the representative files are provided
            if 'authorizationLetter' not in request.files or 'representativeID' not in request.files:
                flash('Please provide both Authorization Letter and Representative ID files for the representative')
                return redirect(request.url)

            authorization_letter_data = authorization_letter_file.read()
            representative_id_data = representative_id_file.read()

            try:
                new_request = CertificationRequest(
                    student_id=student_id,
                    student_name=student_name,
                    certification_type=certification_type,
                    request_form_filename=secure_filename(request_form_file.filename),
                    identification_card_filename=secure_filename(identification_card_file.filename),
                    is_representative=is_representative,
                    authorization_letter_filename=secure_filename(authorization_letter_file.filename),
                    representative_id_filename=secure_filename(representative_id_file.filename),
                    created_at=datetime.utcnow()
                )

                db.session.add(new_request)
                db.session.commit()
                flash('Certification request submitted successfully')
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}')
            finally:
                db.session.close()

        else:
            # If there is no representative, handle the request without representative files
            try:
                new_request = CertificationRequest(
                    student_id=student_id,
                    student_name=student_name,
                    certification_type=certification_type,
                    request_form_filename=secure_filename(request_form_file.filename),
                    identification_card_filename=secure_filename(identification_card_file.filename),
                    created_at=datetime.utcnow()
                )

                db.session.add(new_request)
                db.session.commit()
                flash('Certification request submitted successfully')
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}')
            finally:
                db.session.close()

    return redirect(url_for('stud_certification'))

"""@app.route('/student/submit_service_request', methods=['GET'])
def submit_service_request():
    return render_template('service_request_form.html')"""


@app.route('/student/submit_service_request/request', methods=['POST'], endpoint='submit_services_request_form')
def submit_services_request():
    if request.method == 'POST':
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
        flash('Service request submitted successfully')

    return redirect(url_for('stud_services'))


# ================================================================
#routes for the redirection to the portal of the login in different routes
# ====================================================================================================================#
#===================================================== PORTALS =======================================================#
#=====================================================================================================================#
# ALL STUDENT ROUTES HERE
@app.route('/student')
@prevent_authenticated
def student_portal():
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
@app.route('/student/login_addsubjects')
@prevent_authenticated
def portal_addingofsubject():
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

#for the home
@app.route('/student/home')
@student_required
def student_home():
    session.permanent = True
    return render_template('student/home.html')

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
@student_required
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

# Modify the profile route
@app.route('/student/home/profile')
@student_required
def profile():
    session.update()

    # Retrieve student details from the session
    student_details = {
        'studentNumber': session.get('studentNumber'),
        'name': session.get('name'),
        'gender': session.get('gender'),
        'email': session.get('email'),
        'address': session.get('address'),
        'dateofBirth': session.get('dateofBirth'),
        'placeofBirth': session.get('placeofBirth'),
        'mobileNumber': session.get('mobileNumber'),
        'userImg': session.get('userImg'),
    }

    return render_template('student/profile.html', student_details=student_details)


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
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_certification'))

# Function to check if the user is logged in
def is_user_logged_in_certification():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_changesubsched'))

# Function to check if the user is logged in
def is_user_logged_in_changesubsched():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_enrollment'))

# Function to check if the user is logged in
def is_user_logged_in_enrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    if is_user_logged_in_addingofsubject():
        return render_template('student/adding_of_subject.html')
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_addingofsubject'))

# Function to check if the user is logged in
def is_user_logged_in_addingofsubject():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_addingofsubject')
def redirect_based_on_login_addingofsubject():
    if is_user_logged_in_addingofsubject():
        return redirect(url_for('student_portal_addingofsubject'))
    else:
        return redirect(url_for('portal_addingofsubject'))

#================================================================
# shifting function for students
@app.route('/student/shifting')
def student_portal_shifting():
    session.permanent = True
    if is_user_logged_in_shifting():
        return render_template('student/shifting.html')
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_shifting'))

# Function to check if the user is logged in
def is_user_logged_in_shifting():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_tutorial'))

# Function to check if the user is logged in
def is_user_logged_in_tutorial():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_petition'))

# Function to check if the user is logged in
def is_user_logged_in_petition():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_gradeentry'))

# Function to check if the user is logged in
def is_user_logged_in_gradeentry():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

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
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('portal_crossenrollment'))

# Function to check if the user is logged in
def is_user_logged_in_crossenrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return session.get("user_id") is not None

# Main function to handle redirection based on user login status
@app.route('/student/redirect_based_on_login_crossenrollment')
def redirect_based_on_login_crossenrollment():
    if is_user_logged_in_gradeentry():
        return redirect(url_for('student_portal_crossenrollment'))
    else:
        return redirect(url_for('portal_crossenrollment'))

#================================================================#





#================================================================#
# ALL FACULTY ROUTES HERE
@app.route('/faculty')
@prevent_authenticated
def faculty_portal():
    session.permanent=True
    return render_template('faculty/login.html', api_base_url=faculty_base_api_url)

@app.route('/faculty/home')
@faculty_required
def faculty_home():
    session.permanent = True

    # Retrieve the user's name from the session (you should set it during login)
    user_name = session.get('user_name')
     # Check if the name is in the session
     
    if user_name:
        return render_template('faculty/home.html', user_name=user_name)
    else:
        return render_template('faculty/home.html', user_name="Guest")  # Provide a default if the name is not in the session


# ========================================================================
# ALL ADMIN ROUTES HERE
@app.route('/admin')
@prevent_authenticated
def admin_login():
    session.permanent = True
    return render_template('admin/login.html')

@app.route('/admin/home')
@admin_required
def admin_home():
    session.permanent = True
    return render_template('admin/home.html')

# ========================================================================
# Register the API blueprint
app.register_blueprint(admin_api, url_prefix='/api/v1/admin')
app.register_blueprint(faculty_api, url_prefix=faculty_base_api_url)
app.register_blueprint(student_api, url_prefix='/api/v1/student')

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

# ... other route registrations ...
# ========================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0')




# ... other route registrations ...
# ========================================================================