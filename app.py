from multiprocessing import connection
from flask import Flask, render_template, jsonify, redirect, request, flash, send_file, url_for, session
from models import ChangeOfSubjects, db, Add_Subjects, init_db, Student
from werkzeug.utils import secure_filename
import psycopg2
from sqlalchemy import Connection

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

@app.route('/student/crossenrollment')#
def stud_cross_enrollment():
    return render_template("/student/cross_enrollment.html")#

@app.route('/student/shifting')#
def stud_shifting():
    return render_template("/student/shifting.html")#

@app.route('/student/manualenrollment')#
def stud_enrollment():
    return render_template("/student/manual_enrollment.html")#

@app.route('/student/onlinepetitionofsubject')#
def stud_petition():
    return render_template("/student/petition.html")#

@app.route('/student/requestfortutorialofsubjects')#
def stud_tutorial():
    return render_template("/student/tutorial.html")#

@app.route('/student/certification')#
def stud_certification():
    return render_template("/student/certification.html")#

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

@app.route('/student/home/profile')
@student_required
def profile():
    session.update()
    student_id = 1  # Replace with the actual student ID you want to retrieve
    student = Student.query.get(student_id)

    if student:
        return render_template('student/profile.html', student=student)
    else:
        # Handle the case where the student is not found
        return "Student not found", 404


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





#================================================================
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
    app.run(debug=True)



# ... other route registrations ...
# ========================================================================