from datetime import datetime
from sqlalchemy import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, inspect
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()
    
class Student(db.Model, UserMixin):
    __tablename__ = 'student'

    StudentId = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), unique=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)  
    Email = db.Column(db.String(100), unique=True, nullable=False) 
    address = db.Column(db.String(255), nullable=True) 
    Password = db.Column(db.String(128), nullable=False)
    Gender = db.Column(db.Integer)  
    DateofBirth = db.Column(db.Date)  
    PlaceofBirth = db.Column(db.String(255), nullable=True)
    ResidentialAddress = db.Column(db.String(255), nullable=True)
    MobileNumber = db.Column(db.String(11))
    userImg = db.Column(db.LargeBinary)
   # stud_status = db.Column(db.String(100), nullable=False)

    # Define the 'addsubjects' relationship in the Student model
    notifications = db.relationship('Notification', back_populates='student')
    addsubjects = db.relationship('AddSubjects', back_populates='student')
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
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'Email': self.Email,
            'address': self.address, 
            'Password': self.Password,
            'Gender': self.Gender,           
            'DateofBirth': self.DateofBirth,
            'PlaceofBirth': self.PlaceofBirth,
            'ResidentialAddress': self.ResidentialAddress,
            'MobileNumber': self.MobileNumber,
            'userImg': self.userImg,
            #'stud_status': self.stud_status,
        }
        
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility
    
    def save_image(self, image_data):
    # Method to save image data
        self.userImg = image_data
        db.session.commit()
#======================================================#
#==============Link with the Students==================#
#======================================================#
"""class Programs(db.Model, UserMixin):
    __tablename__ = 'programs'

    programId = db.Column(db.Integer, primary_key=True)
    programCode = db.Column(db.String(150), nullable=False)
    programName = db.Column(db.String(255), nullable=False)

    # Establish a relationship with the YearLevel class
    year = db.relationship('YearLevel', back_populates='programs')

    def to_dict(self):
        return {
            'programId': self.programId,
            'programCode': self.programCode,
            'programName': self.programName,
        }

    def get_programID(self):
        return str(self.programId)

class YearLevel(db.Model, UserMixin):
    __tablename__ = 'yearlevel'

    yearId = db.Column(db.Integer, primary_key=True)
    Level = db.Column(db.String(150), nullable=False)
    programId = db.Column(db.Integer, db.ForeignKey('programs.programId'))

    # Establish relationships with other classes
    programs = db.relationship('Programs', back_populates='yearlevel')
    semesters = db.relationship('Semesters', back_populates='yearlevel')
    courseSub = db.relationship('CourseSub', back_populates='yearlevel')

    def to_dict(self):
        return {
            'yearId': self.yearId,
            'Level': self.Level,
            'programId': self.programId,
        }

    def get_yearId(self):
        return str(self.yearId)

class Semesters(db.Model, UserMixin):
    __tablename__ = 'semesters'

    semesterId = db.Column(db.Integer, primary_key=True)
    semesterName = db.Column(db.String(150), nullable=False)
    yearId = db.Column(db.Integer, db.ForeignKey('year.yearId'))

    # Establish a relationship with YearLevel and CourseSub
    yearlevel = db.relationship('YearLevel', back_populates='semesters')
    courseSubs = db.relationship('CourseSub', back_populates='semesters')

    def to_dict(self):
        return {
            'semesterId': self.semesterId,
            'semesterName': self.semesterName,
            'yearId': self.yearId,
        }

    def get_semesterId(self):
        return str(self.semesterId)

class CourseSub(db.Model, UserMixin):
    __tablename__ = 'courseSub'

    courseSub_Id = db.Column(db.Integer, primary_key=True)
    courseSub_Code = db.Column(db.String(255), nullable=False)
    Sub_Description = db.Column(db.String(255), nullable=False)
    yearId = db.Column(db.Integer, db.ForeignKey('year.yearId'))
    semesterId = db.Column(db.Integer, db.ForeignKey('semesters.semesterId'))

    # Establish relationships with YearLevel and Semester
    yearlevel = db.relationship('YearLevel', back_populates='courseSub')
    semesters = db.relationship('Semesters', back_populates='courseSub')

    def to_dict(self):
        return {
            'courseSub_Id': self.courseSub_Id,
            'courseSub_Code': self.courseSub_Code,
            'Sub_Description': self.Sub_Description,
            'yearId': self.yearId,
            'semesterId': self.semesterId,
        }

    def get_courseSub_Id(self):
        return str(self.courseSub_Id)
"""
#Notification
class Notification(db.Model, UserMixin):
    __tablename__ = 'notifications'

    notifID = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    user_responsible = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))

    # Relationship to the Student model
    student = db.relationship('Student', back_populates='notifications')

    def to_dict(self):
        return {
            'notifID': self.notifID,
            'StudentNumber': self.StudentNumber,
            'service_type': self.service_type,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'StudentId': self.StudentId,
        }

    def get_NotifID(self):
        return str(self.notifID)

#======================================================#       
#Announcements
class Announcement(db.Model, UserMixin):
    __tablename__ = 'announcements'

    announcementId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    content_filename = db.Column(db.String(255))
    content_data = db.Column(db.LargeBinary)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    facultyID = db.Column(db.Integer, db.ForeignKey('student.StudentId'))

    # Relationship to the Faculty model
    faculties = db.relationship('Faculty', back_populates='announcements')
    # Optional: category, visibility, attached files, etc.

    def to_dict(self):
        return {
            'announcementId': self.announcementId,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'facultyID': self.facultyID
        }    
    
    def get_AnnouncementID(self):
        return str(self.announcementId)
#======================================================#       

# ==========Services========== #
# ==========Adding_subject_form========== #
class AddSubjects(db.Model, UserMixin):
    __tablename__ = 'addsubjects'

    subject_ID = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)  
    subject_Names = db.Column(db.String(255), nullable=False)
    enrollment_type = db.Column(db.String(100))  # 'regular50or 'irregular'
    file_data = db.Column(db.LargeBinary)  # Store binary data for the file
    file_name = db.Column(db.String(255))  # Store the filename
    user_responsible = db.Column(db.String(255))  # Add user role attribute
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))

    # Establish a relationship with the Student class
    student = db.relationship('Student', back_populates='addsubjects')

    def to_dict(self):
        return {
            'subject_ID': self.subject_ID,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'subject_Names': self.subject_Names,
            'enrollment_type': self.enrollment_type,
            'file_data': self.file_data,
            'file_name': self.file_name,
            'user_responsible': self.user_responsible,  # Include user role in the dictionary
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_AddSubjectsID(self):
        return str(self.subject_ID)
    
# ==========Services========== #
# ==========Change_of_subjects=========== #
class ChangeOfSubjects(db.Model, UserMixin):
    __tablename__ = 'changesubjects'

    Changesubject_ID = db.Column(db.Integer, primary_key=True)  
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255))
    enrollment_type = db.Column(db.String(100))  # 'regular' or 'irregular'
    ace_form_filename = db.Column(db.String(255))
    ace_form_data = db.Column(db.LargeBinary)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP)
    user_responsible = db.Column(db.String(255))
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))  
 

    # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='changesubjects')

    def to_dict(self):
        return {
            'Changesubject_ID': self.Changesubject_ID,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'enrollment_type': self.enrollment_type,
            'ace_form_filename': self.ace_form_filename,
            'ace_form_data': self.ace_form_data,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_responsible': self.user_responsible,  # Include user role in the dictionary
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_ChangesubjectID(self):
        return str(self.Changesubject_ID)

# ==========Requests========== #
# ========== Reason need pdf file ========== #
class ManualEnrollment(db.Model, UserMixin):
    __tablename__ = 'manual_enrollments'

    m_enrollment_ID = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    enrollment_type = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    me_file_filename = db.Column(db.String(255))
    me_file_data = db.Column(db.LargeBinary)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_responsible = db.Column(db.String(255))  # Add user role attribute
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))


     # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='manual_enrollments')

    def to_dict(self):
        return {
            'm_enrollment_ID': self.m_enrollment_ID,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'enrollment_type': self.enrollment_type,
            'reason': self.reason,
            'me_file_filename': self.me_file_filename,
            'me_file_data': self.me_file_data,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_responsible': self.user_responsible,  # Include user role in the dictionary
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_ManualEnrollmentID(self):
        return str(self.m_enrollment_ID)

# ==========Requests========== #
# ========== Files needed for the Certification ========== #

class CertificationRequest(db.Model, UserMixin):
    __tablename__ = 'certification_requests'

    certification_request_id = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(255), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    certification_type = db.Column(db.String(100), nullable=False)
    request_form_filename = db.Column(db.String(255), nullable=False)
    request_form_data = db.Column(db.LargeBinary)
    identification_card_filename = db.Column(db.String(255), nullable=False)
    identification_card_data = db.Column(db.LargeBinary)
    is_representative = db.Column(db.Boolean, default=False)
    authorization_letter_filename = db.Column(db.String(255))
    authorization_letter_data = db.Column(db.LargeBinary)
    representative_id_filename = db.Column(db.String(255))
    representative_id_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))

     # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='certification_requests')

    def to_dict(self):
        return {
            'certification_request_id': self.certification_request_id,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'certification_type': self.certification_type,
            'request_form_filename': self.request_form_filename,
            'request_form_data': self.request_form_data,
            'identification_card_filename': self.identification_card_filename,
            'identification_card_data': self.identification_card_data,
            'is_representative': self.is_representative,
            'authorization_letter_filename': self.authorization_letter_filename,
            'authorization_letter_data': self.authorization_letter_data,
            'representative_id_filename': self.representative_id_filename,
            'representative_id_data': self.representative_id_data,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_CertificationRequestID(self):
        return str(self.certification_request_id)

# ========== Requests ========== #
class GradeEntry(db.Model, UserMixin):
    __tablename__ = 'grade_entries'

    grade_entry_id = db.Column(db.Integer, primary_key=True)
    StudentNumber =db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    application_type = db.Column(db.String(150), nullable=False)
    completion_form_filename = db.Column(db.String(255), nullable=False)
    completion_form_data = db.Column(db.LargeBinary)  # Add this line
    class_record_filename = db.Column(db.String(255), nullable=False)
    class_record_data = db.Column(db.LargeBinary)  # Add this line
    affidavit_filename = db.Column(db.String(255), nullable=False)
    affidavit_data = db.Column(db.LargeBinary)  # Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(100)) 
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))

     # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='grade_entries')

    def to_dict(self):
        return {
            'grade_entry_id': self.grade_entry_id,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'application_type': self.application_type,
            'completion_form_data': self.completion_form_data,  # Add this line
            'class_record_filename': self.class_record_filename,
            'class_record_data': self.class_record_data,  # Add this line
            'affidavit_filename': self.affidavit_filename,
            'affidavit_data': self.affidavit_data,  # Add this line
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_GradeEntryID(self):
        return str(self.grade_entry_id)
    
# ==========Requests========== #  
# ========== Files needed to the request ========== #
class CrossEnrollment(db.Model, UserMixin):
    __tablename__ = 'cross_enrollments'

    cross_enrollment_id = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    school_for_cross_enrollment = db.Column(db.String(255), nullable=False)
    total_number_of_units = db.Column(db.Integer, nullable=False)
    authorized_subjects_to_take = db.Column(db.Text, nullable=False)
    application_letter_filename = db.Column(db.String(255), nullable=False)
    application_letter_data = db.Column(db.LargeBinary)  # Add this line
    permit_to_cross_enroll_filename = db.Column(db.String(255), nullable=False)
    permit_to_cross_enroll_data = db.Column(db.LargeBinary)  # Add
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId')) 

         # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='cross_enrollments')

    def to_dict(self):
        return {
            'cross_enrollment_id': self.cross_enrollment_id,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
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
            'StudentId': self.StudentId,
        }

    def get_CrossEnrollmentID(self):
        return str(self.cross_enrollment_id)
    
# ==========Requests========== #
class PetitionRequest(db.Model, UserMixin):
    __tablename__ = 'petition_requests'

    petition_request_id = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)#/Student number dpat ito/
    Name = db.Column(db.String(255), nullable=False)
    subject_code = db.Column(db.String(100), nullable=False)
    subject_name = db.Column(db.String(255), nullable=False)
    petition_type = db.Column(db.String(100), nullable=False)
    request_reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))

     # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='petition_requests')

    def to_dict(self):
        return {
            'petition_request_id': self.petition_request_id,
            'StudentNumber':self.StudentNumber,
            'Name': self.Name,
            'subject_code': self.subject_code,
            'subject_name': self.subject_name,
            'petition_type': self.petition_type,
            'request_reason': self.request_reason,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_PetitionRequestID(self):
        return str(self.petition_request_id)
    
# ==========Services========== #  
# ========Accreditation-for-Shiftees-and-Regular========= #  
class ShiftingApplication(db.Model, UserMixin):
    __tablename__ = 'shifting_applications'

    shifting_application_id = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    current_program = db.Column(db.String(255), nullable=False)
    residency_year = db.Column(db.Integer, nullable=False)
    intended_program = db.Column(db.String(255), nullable=False)
    qualifications = db.Column(db.Text)
    file_filename = db.Column(db.String(255))
    file_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255)) 
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))

     # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='shifting_applications')

    def to_dict(self):
        return {
            'shifting_application_id': self.shifting_application_id,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'current_program': self.current_program,
            'residency_year': self.residency_year,
            'intended_program': self.intended_program,
            'qualifications': self.qualifications,
            'file_filename': self.file_filename,
            'file_data': self.file_data,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_ShiftingApplicationID(self):
        return str(self.shifting_application_id)

# ==========Services========== #
# ==========Overload-3-6-units========== #
class OverloadApplication(db.Model, UserMixin):
    __tablename__ = 'overload_applications'

    overload_application_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    StudentNumber = db.Column(db.String(100), nullable=False)
    programcourse = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    subjects_to_add = db.Column(db.String(255), nullable=False)
    justification = db.Column(db.Text, nullable=False)
    file_filename = db.Column(db.String(255))
    file_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255))
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))
 
     # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='overload_applications')

    def to_dict(self):
        return {
            'overload_application_id':  self.overload_application_id,
            'Name': self.Name,
            'StudentNumber': self.StudentNumber,
            'programcourse':self.programcourse,
            'semester': self.semester,
            'subjects_to_add': self.subjects_to_add,
            'justification': self.justification,
            'file_filename': self.file_filename,
            'file_data': self.file_data,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_OverloadApplicationID(self):
        return str(self.overload_application_id)
#Done
# ==========Services========== #
# ==========RO FORM========== #
class TutorialRequest(db.Model, UserMixin):
    __tablename__ = 'tutorial_requests'

    tutorial_request_id = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    subject_code = db.Column(db.String(100), nullable=False)
    subject_name = db.Column(db.String(255), nullable=False)
    file_filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_responsible = db.Column(db.String(255))
    status = db.Column(db.String(100)) #status 
    StudentId = db.Column(db.Integer, db.ForeignKey('student.StudentId'))
     
     # Add a relationship to the 'student' table
    student = db.relationship('Student', back_populates='tutorial_requests')

    def to_dict(self):
        return {
            'tutorial_request_id': self.tutorial_request_id,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'subject_code': self.subject_code,
            'subject_name': self.subject_name,
            'file_filename': self.file_filename,
            'created_at': self.created_at,
            'user_responsible': self.user_responsible,
            'status': self.status,
            'StudentId': self.StudentId,
        }

    def get_TutorialRequestID(self):
        return str(self.tutorial_request_id)


class Faculty(db.Model, UserMixin):
    __tablename__ = 'faculties'

    facultyID = db.Column(db.Integer, primary_key=True)  # UserID
    facultyNumber = db.Column(db.String(255), unique=True, nullable=False) #Faculty_Number
    userType = db.Column(db.String(255))  # e.g., 'Admin', 'Professor', etc.
    name = db.Column(db.String(255), nullable=False)  # Name
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email
    address = db.Column(db.String(255))  # You can use String or TEXT depending on the length
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    dateofBirth = db.Column(db.Date)  # dateofBirth
    placeofBirth = db.Column(db.String(100))  # placeofBirth
    mobile_number = db.Column(db.String(20))  # MobileNumber
    userImg = db.Column(db.LargeBinary)  # Modify the length as needed
    is_active = db.Column(db.Boolean, default=True)

    # Define the 'addsubjects' relationship in the Faculty model
    announcements = db.relationship('Announcement', back_populates='faculty')

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
    
    def save_image(self, image_data):
    # Method to save image data
        self.userImg = image_data
        db.session.commit()

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
      if not inspector.has_table('Student'):
        db.create_all()
    #    create_sample_data()
        
#=====================================================================================================#
# INSERTING DATA
"""def create_sample_data():
    # Create and insert student data
    student_data = [
        {   
            'StudentId':'1',
            'StudentNumber': '2020-00001-CM-0',
            'name': 'student 1',
            'email': 'student1@example.com',
            'address': '301 Don Fabian st. Commonwealth City 1',
            'password': generate_password_hash('password1'),
            'gender': 1,
            'dateofBirth': '2003-01-15',
            'placeofBirth': 'City 1',
            'mobileNumber': '09123123123',
            'userImg': 'default.jpg'
        },
        {
            'StudentId':'2',
            'StudentNumber': '2020-00002-CM-0',
            'name': 'student 2',
            'email': 'student2@example.com',
            'address': '201 Don Juan st. Commonwealth City 2',
            'password': generate_password_hash('password2'),
            'gender': 2,
            'dateofBirth': '2002-05-20',
            'placeofBirth': 'City 2',
            'mobileNumber': '09123123124',
            'userImg': 'pup2.jpg'
        },
        # Add more student data as needed
    ]
    
    for data in student_data:
        student = Student(**data)
        db.session.add(student)
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
