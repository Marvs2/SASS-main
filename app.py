from multiprocessing import connection
from flask import Flask, render_template, jsonify, redirect, request, flash, send_file, url_for, session
from models import db
from werkzeug.utils import secure_filename
import psycopg2
from sqlalchemy import Connection

from Api.v1.student.api_routes import student_api  
from Api.v1.faculty.api_routes import faculty_api
from Api.v1.admin.api_routes import admin_api

import os
from dotenv import load_dotenv


from models import Add_Subjects, init_db, Student

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
#Downloadable files
@app.route('/download/pdf_file')
def download_AddingSubs():
    pdf_path = "static/pdf_files/Adding_subject_form.pdf"  # Replace with the actual path to your PDF file
    return send_file(pdf_path, as_attachment=True, download_name="Adding_subject_form.pdf")



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

@app.route('/student/foroverloadofsubject')
def stud_overload():
    return render_template("/student/subject_overload.html")

@app.route('/student/addingofsubject')
def stud_adding():
    return render_template("/student/adding_of_subject.html")

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

@app.route('/student/changeofsubject/schedule')
def stud_change():
    return render_template("/student/change_of_subject.html")

@app.route('/student/gradeentry')
def stud_correction():
    return render_template("/student/grade_entry.html")

@app.route('/student/crossenrollment')
def stud_cross_enrollment():
    return render_template("/student/cross_enrollment.html")

@app.route('/student/shifting')
def stud_shifting():
    return render_template("/student/shifting.html")

@app.route('/student/manualenrollment')
def stud_enrollment():
    return render_template("/student/manual_enrollment.html")

@app.route('/student/onlinepetitionofsubject')
def stud_petition():
    return render_template("/student/petition.html")

@app.route('/student/requestfortutorialofsubjects')
def stud_tutorial():
    return render_template("/student/tutorial.html")

@app.route('/student/certification')
def stud_certification():
    return render_template("/student/certification.html")

# ================================================================

# ALL STUDENT ROUTES HERE
@app.route('/student')
@prevent_authenticated
def student_portal():
    session.permanent = True
    return render_template('student/login.html')

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