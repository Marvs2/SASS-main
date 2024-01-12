from datetime import datetime
from sqlalchemy import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, inspect
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import os
import time


db = SQLAlchemy()

# Student Users
class Student(db.Model): # (class SPSStudent) In DJANGO you must set the name directly here 
    __tablename__ = 'SPSStudent' # Set the name of table in database (Available for FLASK framework)

    StudentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentNumber = db.Column(db.String(30), unique=True, nullable=False)  # UserID
    FirstName = db.Column(db.String(50), nullable=False)  # First Name
    LastName = db.Column(db.String(50), nullable=False)  # Last Name
    MiddleName = db.Column(db.String(50))  # Middle Name
    Email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    Password = db.Column(db.String(256), nullable=False)  # Password
    Gender = db.Column(db.Integer, nullable=True)  # Gender
    DateOfBirth = db.Column(db.Date)  # DateOfBirth
    PlaceOfBirth = db.Column(db.String(50))  # PlaceOfBirth
    ResidentialAddress = db.Column(db.String(50))  # ResidentialAddress
    MobileNumber = db.Column(db.String(11))  # MobileNumber
    IsOfficer = db.Column(db.Boolean, default=False)
    Token = db.Column(db.String(256))  # This is for handling reset password 
    TokenExpiration = db.Column(db.DateTime) # This is for handling reset password 
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # IsBridging
    
    def to_dict(self):
        return {
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'MiddleName': self.MiddleName,
            'Email': self.Email,
            'Password': self.Password,
            'Gender': self.Gender,
            'DateOfBirth': self.DateOfBirth,
            'PlaceOfBirth': self.PlaceOfBirth,
            'ResidentialAddress': self.ResidentialAddress,
            'MobileNumber': self.MobileNumber,
            'IsOfficer': self.IsOfficer
        }

    def get_id(self):
        return str(self.StudentId)  # Convert to string to ensure compatibility

    def get_user_id(self):
        return self.StudentId

# Faculty Users
class Faculty(db.Model):
    __tablename__ = 'FISFaculty' # Set the name of table in database
    FacultyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FacultyType = db.Column(db.String(50), nullable=False)  # Faculty Type
    Rank = db.Column(db.String(50))  # Faculty Rank
    Units = db.Column(db.Numeric, nullable=False)  # Faculty Unit
    Name = db.Column(db.String(50), nullable=False)  # Name
    FirstName = db.Column(db.String(50), nullable=False)  # First Name
    LastName = db.Column(db.String(50), nullable=False)  # Last Name
    MiddleName = db.Column(db.String(50))  # Middle Name
    MiddleInitial = db.Column(db.String(50))  # Middle Initial
    NameExtension = db.Column(db.String(50))  # Name Extension
    BirthDate = db.Column(db.Date, nullable=False)  # Birthdate
    DateHired = db.Column(db.Date, nullable=False)  # Date Hired
    Degree = db.Column(db.String)  # Degree
    Remarks = db.Column(db.String)  # Remarks
    FacultyCode = db.Column(db.Integer, nullable=False)  # Faculty Code
    Honorific = db.Column(db.String(50))  # Honorific
    Age = db.Column(db.Numeric, nullable=False)  # Age
    
    Email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    ResidentialAddress = db.Column(db.String(50))  # ResidentialAddress
    MobileNumber = db.Column(db.String(11))  # MobileNumber
    Gender = db.Column(db.Integer) # Gender # 1 if Male 2 if Female
    
    Password = db.Column(db.String(256), nullable=False)  # Password
    ProfilePic= db.Column(db.String(50),default="14wkc8rPgd8NcrqFoRFO_CNyrJ7nhmU08")  # Profile Pic
    IsActive = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # FOREIGN TABLES
    

    def to_dict(self):
        return {
            'FacultyId': self.FacultyId,
            'FacultyType': self.FacultyType,
            'Rank': self.Rank,
            'Units': self.Units,
            'Name': self.Name,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'MiddleName': self.MiddleName,
            'MiddleInitial': self.MiddleInitial,
            'NameExtension': self.NameExtension,
            'BirthDate': self.BirthDate,
            'DateHired': self.DateHired,
            'Degree': self.Degree,
            'Remarks': self.Remarks,
            'FacultyCode': self.FacultyCode,
            'honorific': self.Honorific,
            'Age': self.Age,
            'Email': self.Email,
            # 'password': self.password,
            'ProfilePic': self.ProfilePic,
            'IsActive': self.IsActive,
        }
        
    def get_id(self):
        return str(self.FacultyId)  # Convert to string to ensure compatibility



# System Admins Users
class SystemAdmin(db.Model):
    __tablename__ = 'SPSSystemAdmin'

    SysAdminId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FacultyId = db.Column(db.Integer, db.ForeignKey('FISFaculty.FacultyId', ondelete="CASCADE"), primary_key=True) # Students Reference
    SysAdminNumber = db.Column(db.String(30), unique=True)  # UserID
    Name = db.Column(db.String(50), nullable=False)  # Name
    Email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    Password = db.Column(db.String(256), nullable=False)  # Password
    Gender = db.Column(db.Integer)  # Gender
    DateOfBirth = db.Column(db.Date)  # DateOfBirth
    PlaceOfBirth = db.Column(db.String(50))  # PlaceOfBirth
    ResidentialAddress = db.Column(db.String(50))  # ResidentialAddress
    MobileNumber = db.Column(db.String(11))  # MobileNumber
    IsActive = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'SysAdminId': self.SysAdminId,
            'FacultyId': self.FacultyId,
            'SysAdminNumber': self.SysAdminNumber,
            'Name': self.Name,
            'Email': self.Email,
            'Password': self.Password,
            'Gender': self.Gender,
            'DateOfBirth': self.DateOfBirth,
            'PlaceOfBirth': self.PlaceOfBirth,
            'ResidentialAddress': self.ResidentialAddress,
            'MobileNumber': self.MobileNumber,
            'IsActive': self.IsActive
        }

    def get_user_id(self):
        return self.SysAdminId

   
# Course List
class Course(db.Model):
    __tablename__ = 'SPSCourse'

    CourseId = db.Column(db.Integer, primary_key=True, autoincrement=True) # Unique Identifier
    CourseCode = db.Column(db.String(10), unique=True) # Course Code - (BSIT, BSHM, BSCS)
    Name = db.Column(db.String(200)) # (Name of Course (Bachelor of Science in Information Technology)
    Description = db.Column(db.String(200)) # Description of course
    IsValidPUPQCCourses = db.Column(db.Boolean, default=True) # APMS are handling different courses so there are specific courses available in QC Only
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'CourseId': self.CourseId,
            'CourseCode': self.CourseCode,
            'Name': self.Name,
            'Description': self.Description,
            'IsValidPUPQCCourses': self.IsValidPUPQCCourses
        }

# Student Enrolled in the courses
class CourseEnrolled(db.Model):
    __tablename__ = 'SPSCourseEnrolled'

    CourseId = db.Column(db.Integer, db.ForeignKey('SPSCourse.CourseId', ondelete="CASCADE"), primary_key=True)  # Unique Identifier
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) # Students Reference
    DateEnrolled = db.Column(db.Date) # Date they enrolled
    Status = db.Column(db.Integer, nullable=False)  # (0 - Not Graduated ||  1 - Graduated  ||  2 - Drop  ||  3 - Transfer Course || 4 - Transfer School)
    CurriculumYear = db.Column(db.Integer, nullable=False)  # (2019, 2020, 2021) - For checking what the subjects they should taken
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    def to_dict(self):
        return {
            'CourseId': self.CourseId,
            'StudentId': self.StudentId,
            'DateEnrolled': self.DateEnrolled,
        }

# Metadata containing the details of class such as Year, Semester, Batch and Course
class Metadata(db.Model):
    __tablename__ = 'SPSMetadata'

    MetadataId = db.Column(db.Integer, primary_key=True, autoincrement=True) # Unique Identifier
    CourseId = db.Column(db.Integer, db.ForeignKey('SPSCourse.CourseId', ondelete="CASCADE")) # Course References
    Year = db.Column(db.Integer, nullable=False) # (1, 2, 3, 4) - Current year of the class 
    Semester = db.Column(db.Integer, nullable=False) # (1, 2, 3) - Current semester of class
    Batch = db.Column(db.Integer, nullable=False) # (2019, 2020, 2021, ...) - Batch of the class
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# Class Details 
class Class(db.Model):
    __tablename__ = 'SPSClass'

    ClassId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MetadataId = db.Column(db.Integer, db.ForeignKey('SPSMetadata.MetadataId', ondelete="CASCADE")) # Metadata containing details of class year, semester, batch, course
    Section = db.Column(db.Integer) # Section of the class
    IsGradeFinalized = db.Column(db.Boolean, default=False) # Checker if the grade is Finalized
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    __table_args__ = (db.UniqueConstraint('MetadataId', 'Section', name='uq_metadata_section'),)

    def to_dict(self):
        return {
            'ClassId': self.ClassId,
            'Section': self.Section,
            'IsGradeFinalized': self.IsGradeFinalized,
            'MetadataId': self.MetadataId
        }
    
    # Adding a unique constraint
   
# Subject List
class Subject(db.Model):
    __tablename__ = 'SPSSubject'

    SubjectId = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    SubjectCode = db.Column(db.String(20), unique=True) # Subject Code (COMP 20333, GEED 10013, ...)
    Name = db.Column(db.String(200)) # Subject Name
    Description = db.Column(db.String(200)) # Description of Subject
    Units = db.Column(db.Float) # Units of Subjects
    IsNSTP = db.Column(db.Boolean, default=False) # NSTP Cheker
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # ForBridging

    def to_dict(self):
        return {
            'SubjectId': self.SubjectId,
            'SubjectCode': self.SubjectCode,
            'Name': self.Name,
            'Description': self.Description,
            'Units': self.Units,
            'IsNSTP': self.IsNSTP,
        }

# Class Subject contains the list of all subjects in the class
class ClassSubject(db.Model):
    __tablename__ = 'SPSClassSubject'

    ClassSubjectId = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    ClassId = db.Column(db.Integer, db.ForeignKey('SPSClass.ClassId', ondelete="CASCADE")) # Referencing to the Class
    SubjectId = db.Column(db.Integer, db.ForeignKey('SPSSubject.SubjectId', ondelete="CASCADE")) # Referencing to the Subject 
    FacultyId = db.Column(db.Integer, db.ForeignKey('FISFaculty.FacultyId', ondelete="CASCADE"), nullable=True) # Referencing to the Faculty
    Schedule = db.Column(db.String(100), nullable=True) # Schedule of Subjects
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Adding a unique constraint on the combination of ClassId, SubjectId, and FacultyId
    __table_args__ = (db.UniqueConstraint(
        'ClassId', 'SubjectId', 'FacultyId', name='_unique_class_subject_teacher'),)

    def to_dict(self):
        return {
            'ClassSubjectId': self.ClassSubjectId,
            'ClassId': self.ClassId,
            'SubjectId': self.SubjectId,
            'FacultyId': self.FacultyId,
            'Schedule': self.Schedule,
        }

# Student Class Subject Grade contains the student Class subject that they currently taking in
class StudentClassSubjectGrade(db.Model):
    __tablename__ = 'SPSStudentClassSubjectGrade'

    # StudentClassSubjectGradeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClassSubjectId = db.Column(db.Integer, db.ForeignKey('SPSClassSubject.ClassSubjectId', ondelete="CASCADE"), primary_key=True) # Reference to the class subject
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) # Referencing to the student in subject taken
    Grade = db.Column(db.Float) # Students Grade
    DateEnrolled = db.Column(db.Date) # Date enrolled in the subject
    AcademicStatus = db.Column(db.Integer) # (1 - Passed, 2 - Failed, 3 - Incomplete or INC,  4 - Withdrawn )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'ClassSubjectId': self.ClassSubjectId,
            'StudentId': self.StudentId,
            'Grade': self.Grade,
            'DateEnrolled': self.DateEnrolled,
            'AcademicStatus': self.AcademicStatus,
        }

# Curriculum is the list of subject that must taken of specific Course, Year, Semester and Batch. Subject automatically added in class when there is a curriculum
class Curriculum(db.Model):
    __tablename__ = 'SPSCurriculum'

    CurriculumId = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    SubjectId = db.Column(db.Integer, db.ForeignKey('SPSSubject.SubjectId', ondelete="CASCADE")) # Subejct that can be added in the classes if the same year, semester, course and batch
    MetadataId = db.Column(db.Integer, db.ForeignKey('SPSMetadata.MetadataId', ondelete="CASCADE"), nullable=False) # Metadata contains the year, semester, course and batch
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'CurriculumId': self.CurriculumId,
            'SubjectId': self.SubjectId,
            'MetadataId': self.MetadataId
            # Add other attributes if needed
        }

class Services(db.Model):
    __tablename__ = 'SASSServices'
    
    ServiceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId =db.Column(db. Integer, db.ForeignKey('SPSStudent.StudentId'))
    ServiceType = db.Column(db.String(20))
    Status = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'ServiceId': self.ServiceId,
            'StudentId': self.StudentId,
            'ServiceType': self.ServiceType,
            'Status': self.Status,
            # Add other attributes if needed
        }

class SubjectList(db.Model):
    __tablename__ = 'SASSClassSubjectList'
    
    SubjectListId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId'))
    SubjectId = db.Column(db.Integer, db.ForeignKey('SPSSubject.SubjectId'))
    ServiceId = db.Column(db.Integer, db.ForeignKey('SASSServices.ServiceId'))
    Status = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'SubjectListId': self.SubjectListId,
            'StudentId': self.StudentId,
            'SubjectId': self.SubjectId,
            # Add other attributes if needed
        }

    
    

"""class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('SPSSystemAdmin.SysAdminId', ondelete='CASCADE'))
    user = db.relationship('SystemAdmin')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)



class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('SPSSystemAdmin.SysAdminId', ondelete='CASCADE'))
    user = db.relationship('SystemAdmin')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete='CASCADE'))
    user = db.relationship('Student')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def is_refresh_token_active(self):
        print("REFRESH IS ACTIVE")
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()
    
    def to_token_response(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_type': self.token_type,
            'expires_in': self.expires_in,
            'access_token_revoked_at': int(self.access_token_revoked_at),
            'refresh_token_revoked_at': int(self.refresh_token_revoked_at),
            'scope': self.scope,
            'user_id': self.user_id
        }
"""

# ------------------------------------------------
        
# config_mode = 'os.getenv("CONFIG_MODE")'
# add_data = os.getenv("ADD_DATA")
config_mode = 'development'
add_data = 'True'

# print('/'+config_mode+'/')
# print('/'+add_data+'/')

def init_db(app):
    db.init_app(app)
    
    if add_data=='True':
        print("Adding data")
        # from data.student import student_data
        # from data.faculty import faculty_data
        # from data.universityadmin import university_admin_data
        # from data.systemadmin import system_admin_data
        # from data.course import course_data
        # from data.courseEnrolled import course_enrolled_data
        # from data.subject import subject_data
        # from data.classes import class_data
        # from data.classSubject import class_subject_data
        # from data.studentClassSubjectGrade import student_class_subject_grade_data
        # from data.studentClassGrade import student_class_grade_data
        # from data.classSubjectGrade import class_subject_grade_data
        # from data.classGrade import class_grade_data
        # from data.courseGrade import course_grade_data

        # from data.curriculum import curriculum_data
        # from data.metadata import metadata_data

    def create_sample_data():
        # for data in student_data:
        #     student = Student(**data)
        #     db.session.add(student)

        # for data in faculty_data:
        #     faculty = Faculty(**data) # done
        #     db.session.add(faculty)

        # for data in system_admin_data:
        #     system_admin = SystemAdmin(**data) # done
        #     db.session.add(system_admin)

        # for data in course_data:
        #     course = Course(**data)
        #     db.session.add(course) # done
        #     db.session.flush()
            
        # for data in subject_data:
        #     subject = Subject(**data) # done
        #     db.session.add(subject)
        #     db.session.flush()

        # for data in metadata_data:
        #     metadata = Metadata(**data) # done
        #     db.session.add(metadata)
        #     db.session.flush()

        # for data in curriculum_data:
        #     curriculum = Curriculum(**data) # done
        #     db.session.add(curriculum)
        #     db.session.flush()
            
        # for data in course_enrolled_data:
        #     course_enrolled = CourseEnrolled(**data) # done
        #     db.session.add(course_enrolled)
        #     db.session.flush()

        
        # for data in class_data:
        #     class_ = Class(**data) # done
        #     db.session.add(class_)
        #     db.session.flush()

        # for data in class_subject_data:
        #     class_subject = ClassSubject(**data) # done
        #     db.session.add(class_subject)
        #     db.session.flush()

        # for data in student_class_subject_grade_data:
        #     student_class_subject_grade = StudentClassSubjectGrade(**data) # done
        #     db.session.add(student_class_subject_grade)
        #     db.session.flush()

        # for data in course_grade_data:
        #     course_grade = CourseGrade(**data) # walang data model
        #     db.session.add(course_grade)
        #     db.session.flush()

        
        db.session.commit()
        db.session.close()

    
    # if config_mode == 'development' :
    #     with app.app_context():
    #         inspector = inspect(db.engine)
    #         db.create_all()

    #         if add_data=='True':
    #             print("DEVELOPMENT AND ADDING DATA")
    #             create_sample_data()

    print(config_mode)
    print(add_data)

    
    if config_mode == 'development' and add_data=='True':
        print("DEVELOPMENT AND ADDING DATA")
        with app.app_context():
            inspector = inspect(db.engine)
            # if not inspector.has_table('SPSStudent'):
            db.create_all()
            create_sample_data()