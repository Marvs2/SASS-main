from datetime import datetime
from sqlalchemy import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, inspect
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()
    
class Student(db.Model, UserMixin):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False) 
    address = db.Column(db.String(255), nullable=True) 
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.Integer)  
    dateofBirth = db.Column(db.Date)  
    placeofBirth = db.Column(db.String(255), nullable=True)
    mobileNumber = db.Column(db.String(11))
    userImg = db.Column(db.String, nullable=False) 
   # stud_status = db.Column(db.String(100), nullable=False)

    # Define the 'subjects' relationship in the Student model
    subjects = db.relationship('Add_Subjects', back_populates='student')
    changesubjects = db.relationship('ChangeOfSubjects', back_populates='student')
    manual_enrollments = db.relationship('ManualEnrollment', back_populates='student')
    certification_requests = db.relationship('CertificationRequest', back_populates='student')
    grade_entries = db.relationship('GradeEntry', back_populates='student')
    cross_enrollments = db.relationship('CrossEnrollment', back_populates='student')
    petition_requests = db.relationship('PetitionRequest', back_populates='student')
    shifting_applications = db.relationship('ShiftingApplication', back_populates='student')
    overload_applications = db.relationship('OverloadApplication', back_populates='student')
    tutorial_requests = db.relationship('TutorialRequest', back_populates='student')

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'email': self.email,
            'address': self.address, 
            'password': self.password,
            'gender': self.gender,           
            'dateofBirth': self.dateofBirth,
            'placeofBirth': self.placeofBirth,
            'mobileNo': self.mobileNumber,
            'userImg': self.userImg,
            #'stud_status': self.stud_status,
        }
        
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility
    
    def save_image(self, image_data):
    # Method to save image data
        self.userImg = image_data
        db.session.commit()

class Add_Subjects(db.Model, UserMixin):
    __tablename__ = 'subjects'

    subject_ID = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)  
    subject_Names = db.Column(db.String(255), nullable=False)
    enrollment_type = db.Column(db.String(100))  # 'regular50or 'irregular'
    file_data = db.Column(db.LargeBinary)  # Store binary data for the file
    file_name = db.Column(db.String(255))  # Store the filename
    user_responsible = db.Column(db.String(255))  # Add user role attribute
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

    # Establish a relationship with the Student class
    student = db.relationship('Student', back_populates='subjects')

    def to_dict(self):
        return {
            'subject_ID': self.subject_ID,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'subject_Names': self.subject_Names,
            'enrollment_type': self.enrollment_type,
            'file_data': self.file_data,
            'file_name': self.file_name,
            'user_responsible': self.user_responsible,  # Include user role in the dictionary
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_Add_SubjectsID(self):
        return str(self.subject_ID)
    

class ChangeOfSubjects(db.Model, UserMixin):
    __tablename__ = 'changesubjects'

    Changesubject_ID = db.Column(db.Integer, primary_key=True)  
    studentNumber = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255))
    enrollment_type = db.Column(db.String(100))  # 'regular' or 'irregular'
    ace_form_filename = db.Column(db.String(255))
    ace_form_data = db.Column(db.LargeBinary)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP)
    user_responsible = db.Column(db.String(255))
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))  
 

    # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='changesubjects')

    def to_dict(self):
        return {
            'Changesubject_ID': self.Changesubject_ID,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'enrollment_type': self.enrollment_type,
            'ace_form_filename': self.ace_form_filename,
            'ace_form_data': self.ace_form_data,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_responsible': self.user_responsible,  # Include user role in the dictionary
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_ChangesubjectID(self):
        return str(self.Changesubject_ID)
        
class ManualEnrollment(db.Model, UserMixin):
    __tablename__ = 'manual_enrollments'

    m_enrollment_ID = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    enrollment_type = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    me_file_filename = db.Column(db.String(255))
    me_file_data = db.Column(db.LargeBinary)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_responsible = db.Column(db.String(255))  # Add user role attribute
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))


     # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='manual_enrollments')

    def to_dict(self):
        return {
            'm_enrollment_ID': self.m_enrollment_ID,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'enrollment_type': self.enrollment_type,
            'reason': self.reason,
            'me_file_filename': self.me_file_filename,
            'me_file_data': self.me_file_data,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_responsible': self.user_responsible,  # Include user role in the dictionary
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_ManualEnrollmentID(self):
        return str(self.m_enrollment_ID)
    
class CertificationRequest(db.Model, UserMixin):
    __tablename__ = 'certification_requests'

    certification_request_id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    certification_type = db.Column(db.String(100), nullable=False)
    request_form_filename = db.Column(db.String(255), nullable=False)
    request_form_data = db.Column(db.LargeBinary)
    identification_card_filename = db.Column(db.String(255), nullable=False)
    identification_card_data = db.Column(db.LargeBinary)
    is_representative = db.Column(db.Boolean, default=False)
    authorization_letter_filename = db.Column(db.String(255))
    authorization_letter_data = db.Column(db.LargeBinary)
    representative_id_filename = db.Column(db.String(255))
    representative_id_date = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

     # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='certification_requests')

    def to_dict(self):
        return {
            'certification_request_id': self.certification_request_id,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'certification_type': self.certification_type,
            'request_form_filename': self.request_form_filename,
            'request_form_data': self.request_form_data,
            'identification_card_filename': self.identification_card_filename,
            'identification_card_data': self.identification_card_data,
            'is_representative': self.is_representative,
            'authorization_letter_filename': self.authorization_letter_filename,
            'authorization_letter_data': self.authorization_letter_data,
            'representative_id_filename': self.representative_id_filename,
            'representative_id_date': self.representative_id_date,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_CertificationRequestID(self):
        return str(self.certification_request_id)
    
class GradeEntry(db.Model, UserMixin):
    __tablename__ = 'grade_entries'

    grade_entry_id = db.Column(db.Integer, primary_key=True)
    studentNumber =db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    application_type = db.Column(db.String(150), nullable=False)
    completion_form_filename = db.Column(db.String(255), nullable=False)
    completion_form_data = db.Column(db.LargeBinary, nullable=False)  # Add this line
    class_record_filename = db.Column(db.String(255), nullable=False)
    class_record_data = db.Column(db.LargeBinary, nullable=False)  # Add this line
    affidavit_filename = db.Column(db.String(255), nullable=False)
    affidavit_data = db.Column(db.LargeBinary, nullable=False)  # Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(100)) 
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

     # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='grade_entries')

    def to_dict(self):
        return {
            'grade_entry_id': self.grade_entry_id,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'application_type': self.application_type,
            'completion_form_data': self.completion_form_data,  # Add this line
            'class_record_filename': self.class_record_filename,
            'class_record_data': self.class_record_data,  # Add this line
            'affidavit_filename': self.affidavit_filename,
            'affidavit_data': self.affidavit_data,  # Add this line
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_GradeEntryID(self):
        return str(self.grade_entry_id)
    
class CrossEnrollment(db.Model, UserMixin):
    __tablename__ = 'cross_enrollments'

    cross_enrollment_id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    school_for_cross_enrollment = db.Column(db.String(255), nullable=False)
    total_number_of_units = db.Column(db.Integer, nullable=False)
    authorized_subjects_to_take = db.Column(db.Text, nullable=False)
    application_letter_filename = db.Column(db.String(255), nullable=False)
    application_letter_data = db.Column(db.LargeBinary, nullable=False)  # Add this line
    permit_to_cross_enroll_filename = db.Column(db.String(255), nullable=False)
    permit_to_cross_enroll_data = db.Column(db.LargeBinary, nullable=False)  # Add
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id')) 

         # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='cross_enrollments')

    def to_dict(self):
        return {
            'cross_enrollment_id': self.cross_enrollment_id,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'school_for_cross_enrollment': self.school_for_cross_enrollment,
            'total_number_of_units': self.total_number_of_units,
            'authorized_subjects_to_take': self.authorized_subjects_to_take,
            'application_letter_filename': self.application_letter_filename,
            'application_letter_data': self.application_letter_data,  # Add this line
            'permit_to_cross_enroll_filename': self.permit_to_cross_enroll_filename,
            'permit_to_cross_enroll_data': self.permit_to_cross_enroll_data,  #
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_CrossEnrollmentID(self):
        return str(self.cross_enrollment_id)
    
class PetitionRequest(db.Model, UserMixin):
    __tablename__ = 'petition_requests'

    petition_request_id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100), nullable=False)#/Student number dpat ito/
    name = db.Column(db.String(255), nullable=False)
    subject_code = db.Column(db.String(100), nullable=False)
    subject_name = db.Column(db.String(255), nullable=False)
    petition_type = db.Column(db.String(100), nullable=False)
    request_reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

     # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='petition_requests')

    def to_dict(self):
        return {
            'petition_request_id': self.petition_request_id,
            'studentNumber':self.studentNumber,
            'name': self.name,
            'subject_code': self.subject_code,
            'subject_name': self.subject_name,
            'petition_type': self.petition_type,
            'request_reason': self.request_reason,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_PetitionRequestID(self):
        return str(self.petition_request_id)
    
class ShiftingApplication(db.Model, UserMixin):
    __tablename__ = 'shifting_applications'

    shifting_application_id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    current_program = db.Column(db.String(255), nullable=False)
    residency_year = db.Column(db.Integer, nullable=False)
    intended_program = db.Column(db.String(255), nullable=False)
    qualifications = db.Column(db.Text)
    file_filename = db.Column(db.String(255))
    file_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

     # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='shifting_applications')

    def to_dict(self):
        return {
            'shifting_application_id': self.shifting_application_id,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'current_program': self.current_program,
            'residency_year': self.residency_year,
            'intended_program': self.intended_program,
            'qualifications': self.qualifications,
            'file_filename': self.file_filename,
            'file_data': self.file_data,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_ShiftingApplicationID(self):
        return str(self.shifting_application_id)

class OverloadApplication(db.Model, UserMixin):
    __tablename__ = 'overload_applications'

    overload_application_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    studentNumber = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    subjects_to_add = db.Column(db.String(255), nullable=False)
    justification = db.Column(db.Text, nullable=False)
    file_filename = db.Column(db.String(255))
    file_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255))
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
 
     # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='overload_applications')

    def to_dict(self):
        return {
            'overload_application_id': self.overload_application_id,
            'name': self.name,
            'studentNumber': self.studentNumber,
            'semester': self.semester,
            'subjects_to_add': self.subjects_to_add,
            'justification': self.justification,
            'file_filename': self.file_filename,
            'file_data': self.file_data,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_OverloadApplicationID(self):
        return str(self.overload_application_id)

class TutorialRequest(db.Model, UserMixin):
    __tablename__ = 'tutorial_requests'

    tutorial_request_id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    subject_code = db.Column(db.String(100), nullable=False)
    subject_name = db.Column(db.String(255), nullable=False)
    file_filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255))
    status = db.Column(db.String(100)) #status 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
     
     # Add a relationship to the 'students' table
    student = db.relationship('Student', back_populates='tutorial_requests')

    def to_dict(self):
        return {
            'tutorial_request_id': self.tutorial_request_id,
            'studentNumber': self.studentNumber,
            'name': self.name,
            'subject_code': self.subject_code,
            'subject_name': self.subject_name,
            'file_filename': self.file_filename,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'student_id': self.student_id,
        }

    def get_TutorialRequestID(self):
        return str(self.tutorial_request_id)



"""class Payment(db.Model, UserMixin):
    __tablename__ = 'payments'

    paymentID = db.Column(db.Integer, primary_key=True)
    modeofPayment = db.Column(db.String(100))
    totalPayment = db.Column(db.DECIMAL)  # You can specify precision and scale if needed
    dateofPayment = db.Column(db.Date)
    proofofPayment = db.Column(db.String(255))  # Modify the length as needed
    stud_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)


    def to_dict(self):
        return {
            'paymentID': self.paymentID,
 #           'id': self.id,
            'modeofPayment': self.modeofPayment,
            'totalPayment': float(self.totalPayment),  # Convert DECIMAL to float for JSON serialization
            'dateofPayment': str(self.dateofPayment),  # Convert Date to string for JSON serialization
            'proofofPayment': self.proofofPayment,
            'stud_id': self.stud_id
        }
    # **How to call it
    #payment = Payment.query.get(some_payment_id)
    #payment_data = payment.to_dict()
        def get_paymentID(self):
            return str(self.paymentID)  # Convert to string to ensure compatibility"""

"""class Service(db.Model, UserMixin):
    __tablename__ = 'services'

    serviceID = db.Column(db.Integer, primary_key=True)
    typeofServices = db.Column(db.String(100))
    status = db.Column(db.String(100)) #Modifythelength
    dateofServices = db.Column(db.Date)
    proofofServices = db.Column(db.String(255))
    stud_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)

    def to_dict(self):
        return {
            'serviceID': self.serviceID,
   #         'id': self.id,
            'typeofServices': self.typeofServices,
            'status': self.status,
            'dateofServices': str(self.dateofServices),
            'proofofServices': self.proofofServices,
            'stud_id': self.stud_id
        }
    # **How to call it
    # service = Service.query.get(some_service_id)
    # service_data = service.to_dict()
        def get_serviceID(self):
            return str(self.serviceID)  # Convert to string to ensure compatibility

class Feedback(db.Model, UserMixin):
    __tablename__ = 'feedbacks'
    feedbackID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    emailAddress = db.Column(db.String(100))
    ratings = db.Column(db.Integer)  # Assuming ratings are integers
    feedBacks = db.Column(db.TEXT)  # Modify the data type as needed
    stud_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)

    def to_dict(self):
        return {
            'feedbackID': self.feedbackID,
            'name': self.name,
            'emailAddress': self.emailAddress,
            'ratings': self.ratings,
            'feedBacks': self.feedBacks,
            'stud_id': self.stud_id
        }
    # **How to call it
    # service = Service.query.get(some_service_id)
    # service_data = service.to_dict()
        def get_feedbackID(self):
            return str(self.feddbackID)  # Convert to string to ensure compatibility

class Complaint(db.Model, UserMixin):
    __tablename__ = 'complaints'
    
    complaintID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    emailAddress = db.Column(db.String(100))
    complaintDetails = db.Column(db.TEXT)
    complaintFile = db.Column(db.String(255))  # Modify the length as needed
    dateofComplaint = db.Column(db.Date)
    stud_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)


    def to_dict(self):
        return {
            'complaintID': self.complaintID,
            'name': self.name,
            'emailAddress': self.emailAddress,
            'complaintDetails': self.complaintDetails,
            'complaintFile': self.complaintFile,
            'dateofComplaint': str(self.dateofComplaint),  # Convert Date to string for JSON serialization
            'stud_id': self.stud_id
        }
    # **How to call it
    # complaint = Complaint.query.get(some_complaint_id)
    # complaint_data = complaint.to_dict()
    def get_complaintID(self):
        return str(self.complaintID)  # Convert to string to ensure compatibility

class Announcement(db.Model, UserMixin):
    __tablename__ = 'announcements'

    announcementID = db.Column(db.Integer, primary_key=True)
    announcementType = db.Column(db.String(100))  # e.g., 'General', 'Event', etc.
    announcementDetails = db.Column(db.TEXT)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    facultyID = db.Column(db.Integer, db.ForeignKey('faculties.facultyID'), nullable=False)

    faculty = db.relationship('Faculty', back_populates='faculty')

    def to_dict(self):
        return {
        'announcementID': self.announcementID,
        'announcementType': self.announcementType,
        'announcementDetails': self.announcementDetails,
        'date': str(self.date),   # Convert Date to string for JSON serialization
        'time': str(self.time),  # Convert Time to string for JSON serialization
        'facultyID': self.facultyID
        }
    def get_announcementID(self):
        return str(self.announcementID)  # Convert to string to ensure compatibility"""


class Faculty(db.Model, UserMixin):
    __tablename__ = 'faculties'

    facultyID = db.Column(db.Integer, primary_key=True)  # UserID
    faculty_Number = db.Column(db.String(255), unique=True, nullable=False) #Faculty_Number
    userType = db.Column(db.String(255))  # e.g., 'Admin', 'Professor', etc.
    name = db.Column(db.String(255), nullable=False)  # Name
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email
    address = db.Column(db.String(255))  # You can use String or TEXT depending on the length
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    dateofBirth = db.Column(db.Date)  # dateofBirth
    placeofBirth = db.Column(db.String(100))  # placeofBirth
    mobile_number = db.Column(db.String(20))  # MobileNumber
    userImg = db.Column(db.String(255))  # Modify the length as needed
    is_active = db.Column(db.Boolean, default=True)

    # Define the 'subjects' relationship in the Faculty model
   # subjects = db.relationship('Add_Subjects', back_populates='faculty')

    def to_dict(self):
        return {
            'facultyID': self.facultyID,
            'facultyNumber': self.facultyNumber,
            'userType': self.userType,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'password': self.password,
            'gender': self.gender,
            'dateofBirth': self.dateofBirth,
            'placeofBirth': self.placeofBirth,
            'mobile_number': self.mobile_number,
            'userImg': self.userImg,
            'is_active': self.is_active
        }
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility
    

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    adm_Id = db.Column(db.Integer, primary_key=True)  # UserID
    admin_Number = db.Column(db.String(30), unique=True, nullable=False) #AdminNumber
    name = db.Column(db.String(255), nullable=False)  # Name
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    dateofBirth = db.Column(db.Date)  # dateofBirth
    placeofBirth = db.Column(db.String(100))  # placeofBirth
    mobile_number = db.Column(db.String(11))  # MobileNumber
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'adm_Id': self.adm_Id,
            'admin_Number': self.admin_Number,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'gender': self.gender,
            'dateofBirth': self.dateofBirth,
            'placeofBirth': self.placeofBirth,
            'mobile_number': self.mobile_number,
            'is_active': self.is_active
        }
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility

def init_db(app):
    db.init_app(app)
    with app.app_context():
      inspector = inspect(db.engine)
      if not inspector.has_table('students'):
        db.create_all()
    #    create_sample_data()
        
#=====================================================================================================#
"""class Services(db.Model, UserMixin):
    __tablename__ = 'services'

    service_id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Common fields for all services
    file_filename = db.Column(db.String(255))
    user_role = db.Column(db.String(100))  # Add user role attribute

    # Additional fields for specific service types
    # Subject-related fields
    subject_name = db.Column(db.String(100))
    enrollment_type = db.Column(db.String500))
    file_data = db.Column(db.LargeBinary)
    faculty_number = db.Column(db.String(100))

    # Change of Subjects fields
    ace_form_filename = db.Column(db.String(255))
    ace_form_data = db.Column(db.LargeBinary)
    updated_at = db.Column(db.TIMESTAMP)

    # Manual Enrollment fields
    enrollment_type_manual = db.Column(db.String(100))
    reason = db.Column(db.Text)
    me_file_data = db.Column(db.LargeBinary)

    # Certification Request fields
    certification_type = db.Column(db.String(100))
    request_form_filename = db.Column(db.String(255))
    identification_card_filename = db.Column(db.String(255))
    is_representative = db.Column(db.Boolean, default=False)
    authorization_letter_filename = db.Column(db.String(255))
    representative_id_filename = db.Column(db.String(255))

    # Grade Entry fields
    application_type = db.Column(db.String(100))
    completion_form_filename = db.Column(db.String(255))
    class_record_filename = db.Column(db.String(255))
    affidavit_filename = db.Column(db.String(255))

    # Cross Enrollment fields
    school_for_cross_enrollment = db.Column(db.String(255))
    total_number_of_units = db.Column(db.Integer)
    authorized_subjects_to_take = db.Column(db.Text)
    application_letter_filename_cross = db.Column(db.String(255))
    permit_to_cross_enroll_filename = db.Column(db.String(255))

    # Petition Request fields
    subject_code_petition = db.Column(db.String(100))
    subject_name_petition = db.Column(db.String(255))
    request_reason = db.Column(db.Text)

    # Shifting Application fields
    current_program_shifting = db.Column(db.String(255))
    residency_year_shifting = db.Column(db.Integer)
    intended_program_shifting = db.Column(db.String(255))
    qualifications_shifting = db.Column(db.Text)
    file_filename_shifting = db.Column(db.String(255))

    # Overload Application fields
    semester_overload = db.Column(db.String(20))
    subjects_to_add_overload = db.Column(db.String(255))
    justification_overload = db.Column(db.Text)
    file_filename_overload = db.Column(db.String(255))

    # Tutorial Request fields
    subject_code_tutorial = db.Column(db.String(100))
    subject_name_tutorial = db.Column(db.String(255))
    online_petition_link_tutorial = db.Column(db.String(255))

    def to_dict(self):
        service_dict = {
            'service_id': self.service_id,
            'service_type': self.service_type,
            'student_id': self.student_id,
            'name': self.name,
            'created_at': self.created_at,
            'file_filename': self.file_filename,
            'user_role': self.user_role
        }

        # Add specific fields based on service type
        if self.service_type == 'subject':
            service_dict.update({
                'subject_name': self.subject_name,
                'enrollment_type': self.enrollment_type,
                'file_data': self.file_data,
                'faculty_number': self.faculty_number
            })
        elif self.service_type == 'change_of_subjects':
            service_dict.update({
                'ace_form_filename': self.ace_form_filename,
                'ace_form_data': self.ace_form_data,
                'updated_at': self.updated_at
            })
        elif self.service_type == 'manual_enrollment':
            service_dict.update({
                'enrollment_type_manual': self.enrollment_type_manual,
                'reason': self.reason,
                'me_file_data': self.me_file_data
            })
        elif self.service_type == 'certification_request':
            service_dict.update({
                'certification_type': self.certification_type,
                'request_form_filename': self.request_form_filename,
                'identification_card_filename': self.identification_card_filename,
                'is_representative': self.is_representative,
                'authorization_letter_filename': self.authorization_letter_filename,
                'representative_id_filename': self.representative_id_filename
            })
        elif self.service_type == 'grade_entry':
            service_dict.update({
                'application_type': self.application_type,
                'completion_form_filename': self.completion_form_filename,
                'class_record_filename': self.class_record_filename,
                'affidavit_filename': self.affidavit_filename
            })
        elif self.service_type == 'cross_enrollment':
            service_dict.update({
                'school_for_cross_enrollment': self.school_for_cross_enrollment,
                'total_number_of_units': self.total_number_of_units,
                'authorized_subjects_to_take': self.authorized_subjects_to_take,
                'application_letter_filename_cross': self.application_letter_filename_cross,
                'permit_to_cross_enroll_filename': self.permit_to_cross_enroll_filename
            })
        elif self.service_type == 'petition_request':
            service_dict.update({
                'subject_code_petition': self.subject_code_petition,
                'subject_name_petition': self.subject_name_petition,
                'request_reason': self.request_reason
            })
        elif self.service_type == 'shifting_application':
            service_dict.update({
                'current_program_shifting': self.current_program_shifting,
                'residency_year_shifting': self.residency_year_shifting,
                'intended_program_shifting': self.intended_program_shifting,
                'qualifications_shifting': self.qualifications_shifting,
                'file_filename_shifting': self.file_filename_shifting
            })
        elif self.service_type == 'overload_application':
            service_dict.update({
                'semester_overload': self.semester_overload,
                'subjects_to_add_overload': self.subjects_to_add_overload,
                'justification_overload': self.justification_overload,
                'file_filename_overload': self.file_filename_overload
            })
        elif self.service_type == 'tutorial_request':
            service_dict.update({
                'subject_code_tutorial': self.subject_code_tutorial,
                'subject_name_tutorial': self.subject_name_tutorial,
                'online_petition_link_tutorial': self.online_petition_link_tutorial
            })

        return service_dict

    def get_ServiceID(self):
        return str(self.service_id)"""
#=====================================================================================================#
# INSERTING DATA
"""def create_sample_data():
    # Create and insert students data
    students_data = [
        {   
            'student_id':'1',
            'studentNumber': '2020-00001-CM-0',
            'name': 'Students 1',
            'email': 'students1@example.com',
            'address': '301 Don Fabian st. Commonwealth City 1',
            'password': generate_password_hash('password1'),
            'gender': 1,
            'dateofBirth': '2003-01-15',
            'placeofBirth': 'City 1',
            'mobileNumber': '09123123123',
            'userImg': 'default.jpg'
        },
        {
            'student_id':'2',
            'studentNumber': '2020-00002-CM-0',
            'name': 'Students 2',
            'email': 'students2@example.com',
            'address': '201 Don Juan st. Commonwealth City 2',
            'password': generate_password_hash('password2'),
            'gender': 2,
            'dateofBirth': '2002-05-20',
            'placeofBirth': 'City 2',
            'mobileNumber': '09123123124',
            'userImg': 'pup2.jpg'
        },
        # Add more students data as needed
    ]
    
    for data in students_data:
        students = Student(**data)
        db.session.add(students)
        db.session.flush()

    # Create and insert faculty data
    faculty_data = [
        {
            'facultyID':'1',
            'facultyNumber': '2020-00001-TC-0',
            'userType': 'Director',
            'name': 'Faculty 1',
            'email': 'faculty1@example.com',
            'address': '100 Galaxy st. City 2',
            'password': generate_password_hash('director'),
            'gender': 1,
            'dateofBirth': '1988-07-20',
            'placeofBirth': 'City 2',
            'mobile_number': '09123123111',
            'userImg': 'default.jpg',
            'is_active': True
        },
        {
            'facultyID': '2',
            'facultyNumber': '2020-00002-TC-0',
            'userType': 'Head Academic Program',
            'name': 'Faculty 2',
            'email': 'faculty2@example.com',
            'address': '101 Mercury st. City 3',
            'password': generate_password_hash('headacademicprogram'),
            'gender': 2,
            'dateofBirth': '1975-12-05',
            'placeofBirth': 'City 3',
            'mobile_number': '09123123125',
            'userImg': 'default.jpg',
            'is_active': False
        },
        # Add more faculty data as needed
    ]
    
    for data in faculty_data:
        faculty = Faculty(**data)
        db.session.add(faculty)
        db.session.flush()
        
    # Create and insert admin data
    admin_data = [
        {
            'adm_Id': 1,
            'admin_Number': '2020-00001-AD-0',
            'name': 'Admin 1',
            'email': 'admin1@example.com',
            'password': generate_password_hash('password1'),
            'gender': 2,
            'dateofBirth': '1995-03-10',
            'placeofBirth': 'City 3',
            'mobile_number': '09123123222',
            'is_active': True
        },
        {
            'adm_Id': 2,
            'admin_Number': '2020-00002-AD-0',
            'name': 'Admin 2',
            'email': 'admin2@example.com',
            'password': generate_password_hash('password2'),
            'gender': 1,
            'dateofBirth': '1980-09-18',
            'placeofBirth': 'City 4',
            'mobile_number': '09123123223',
            'is_active': True
        },
        # Add more admin data as needed
    ]
    
    for data in admin_data:
        admin = Admin(**data)
        db.session.add(admin)
        db.session.flush()

db.session.commit()
db.session.close()"""
