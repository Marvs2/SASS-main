# api/api_routes.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from models import Student
#from models import Services
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  login_user
from flask_cors import CORS 

import os

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

# Function to authenticate the user (usually happens during login)
def authenticate_user(username, password):
    # Your authentication logic goes here
    # Check if the provided username and password match a user in your database
    # If authenticated, retrieve the user ID and set it in the session
    user = User.query.filter_by(username=username).first()  # Replace User with your actual model
    if user and user.check_password(password):  # Replace check_password with your validation logic
        session['user_id'] = user.id  # Assuming user.id is the ID of the authenticated user
        return True
    return False

# Api/v1/student/api_routes.py
#================================================================
# Function to check if the user is logged in
def is_user_logged_in_overload():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_overload
@student_api.route('/login-Overload', methods=['GET', 'POST'])
def login_Overload():
    if is_user_logged_in_overload():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_overload'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_overload'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#========================================================

def is_user_logged_in_certification():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

# Login function for students to goto certification
@student_api.route('/login-Certification', methods=['GET', 'POST'])
def login_Certification():
    if is_user_logged_in_certification():
        # If the user is already logged in, redirect to the certifications page
        return redirect(url_for('student_portal_certification'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_certification', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
def is_user_logged_in_changesubsched():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None

# Login function for students to goto changesubsched
@student_api.route('/login-Changesubsched', methods=['GET', 'POST'])
def login_Changesubsched():
    if is_user_logged_in_changesubsched():
        # If the user is already logged in, redirect to the changesubsched page
        return redirect(url_for('student_portal_changesubsched'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_changesubsched', student_detailss=session))

        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in
def is_user_logged_in_enrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Enrollment', methods=['GET', 'POST'])
def login_Enrollment():
    if is_user_logged_in_enrollment():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_enrollment'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_enrollment', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in addingofsubject
def is_user_logged_in_addingofsubject():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-AddingofSubjects', methods=['GET', 'POST'])
def login_Addingofsubject():
    if is_user_logged_in_addingofsubject():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_addingsubject'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_addingsubject', student_details=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in tutorial of subjects
def is_user_logged_in_tutorial():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Tutorial', methods=['GET', 'POST'])
def login_Tutorial():
    if is_user_logged_in_tutorial():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_tutorial'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_tutorial', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in shifting
def is_user_logged_in_shifting():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Shifting', methods=['GET', 'POST'])
def login_Shifting():
    if is_user_logged_in_shifting():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_shifting'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_shifting', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in shifting
def is_user_logged_in_petition():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Petition', methods=['GET', 'POST'])
def login_Petition():
    if is_user_logged_in_petition():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_petition'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_petition', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================
# Function to check if the user is logged in gradeentry
def is_user_logged_in_gradeentry():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Gradeentry', methods=['GET', 'POST'])
def login_Gradeentry():
    if is_user_logged_in_gradeentry():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_gradeentry'))
    
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg
            return redirect(url_for('student_portal_gradeentry', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')

#=============================================================

# Function to check if the user is logged in shifting
def is_user_logged_in_crossenrollment():
    # Replace this condition with your actual logic for checking if the user is logged in
    return 'access_token' in session and session['access_token'] is not None


# Login function for students to goto student_enrollment
@student_api.route('/login-Crossenrollment', methods=['GET', 'POST'])
def login_Crossenrollment():
    if is_user_logged_in_crossenrollment():
        # If the user is already logged in, redirect to the overload subjects page
        return redirect(url_for('student_portal_crossenrollment'))

    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return redirect(url_for('student_portal_crossenrollment', student_detailss=session))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('student/login.html')


#====================================================================#
#================The real login in the true manners==================#
#====================================================================#
#for All Students
@student_api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        studentNumber = request.form['studentNumber']
        password = request.form['password']
        
        student = Student.query.filter_by(studentNumber=studentNumber).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.student_id)
            session['access_token'] = access_token
            session['user_role'] = 'student'

            # Store additional student details in the session
            session['user_id'] = student.student_id
            session['studentNumber'] = student.studentNumber
            session['name'] = student.name
            session['gender'] = student.gender
            session['email'] = student.email
            session['address'] = student.address
            session['dateofBirth'] = student.dateofBirth
            session['placeofBirth'] = student.placeofBirth
            session['mobileNumber'] = student.mobileNumber
            session['userImg'] = student.userImg

            return render_template('student/home.html', student_detailss=session)

        else:
            flash('Invalid email or password', 'danger')

    return redirect(url_for('student_portal'))
#===================================================
"""@app.route('/api/submit_service_request', methods=['POST'])
def api_submit_service_request():
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


#===================================================
# TESTING AREA
@student_api.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    print("CURRENT USER ID: ", current_user_id)
    # Debug print statement
    student = Student.query.get(current_user_id)
    if student:
        return jsonify(student.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('student_api.login'))

@student_api.route('/addingofsubjects', methods=['GET'])
@jwt_required()
def add_subjects():
    current_user_id = get_jwt_identity()
    print("CURRENT USER ID: ", current_user_id)
    # Debug print statement
    student = Student.query.get(current_user_id)
    if student:
        return jsonify(student.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('student_api.login'))
    
@student_api.route('/certification', methods=['GET'])
@jwt_required()
def certification():
    current_user_id = get_jwt_identity()
    print("CURRENT USER ID: ", current_user_id)
    # Debug print statement
    student = Student.query.get(current_user_id)
    if student:
        return jsonify(student.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('student_api.login'))


#adding subjects
"""@student_api.route('/student/addingofsubject', methods=['GET', ['POST']])
@jwt_required()
def add_subjects():"""
#changeofsubjectorschedule
"""@student_api.route('/student/changeofsubject/schedule', methods=['GET', 'POST'])
@jwt_required()
def changeschedorsub():"""
#overloadunits
"""@student_api.route('/student/foroverloadofsubject', methods=['GET', 'POST'])
@jwt_required()
def overload():"""
#shifting from other school or in pup
"""@student_api.route('/student/shifting', methods=['GET', 'POST'])
@jwt_required()
def shiftees():"""
#RO - For tutorial
"""@student_api.route('/student/requestfortutorialofsubjects', methods=['GET', 'POST'])
@jwt_required()
def tutorial():"""

    
@student_api.route('/all/student', methods=['GET'])
def allstudent():
    api_key = request.headers.get('X-Api-Key')  # Get the API key from the request header

    if api_key in API_KEYS.values():
        return jsonify(message="You got API data")
    else:
        return jsonify(message="Invalid key you cant have an access")


# ...

#@student_api.route('/update/<int:student_id>', methods=['POST','PUT', 'DELETE'])
#@jwt_required()
#def update_student(student_id):
#    current_user_id = get_jwt_identity()
#    student = Student.query.get(student_id)

#    if not student:
#        return jsonify(message="Student not found"), 404

#    if student.id != current_user_id:
#        return jsonify(message="Unauthorized"), 401

#    if request.method == 'POST':
        # Update student information based on the form data
#        student.name = request.form.get('name', student.name)
#        student.email = request.form.get('email', student.email)
#        student.address = request.form.get('address', student.address)
#        student.dateofBirth = request.form.get('dateofBirth', student.dateofBirth)
#        student.placeofBirth = request.form.get('placeofBirth', student.placeofBirth)
#        student.mobileNumber = request.form.get('mobileNumber', student.mobileNumber)
#        student.userImg = request.form.get('userImg', student.userImg)
#        db.session.commit()
#        return jsonify(message="Student information updated successfully")

