from datetime import datetime
import uuid
from sqlalchemy import DateTime, text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, inspect
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import os
import time
import sys
print(sys.path)



db = SQLAlchemy()

# Student Users
class Student(db.Model):
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
            'IsOfficer': self.IsOfficer,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
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
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        
    def get_id(self):
        return str(self.FacultyId)  # Convert to string to ensure compatibility



# System Admins Users
class SystemAdmin(db.Model):
    __tablename__ = 'SPSSystemAdmin'

    SysAdminId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FacultyId = db.Column(db.Integer, db.ForeignKey('FISFaculty.FacultyId', ondelete="CASCADE")) # Students Reference
    SysAdminNumber = db.Column(db.String(30), unique=True)  # UserID
    FirstName = db.Column(db.String(50), nullable=False)  # First Name
    LastName = db.Column(db.String(50), nullable=False)  # Last Name
    MiddleName = db.Column(db.String(50))  # Middle Name
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
            'IsActive': self.IsActive,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def get_user_id(self):
        return self.SysAdminId

# class Admin(db.Model, UserMixin):
#     __tablename__ = 'admins'

#     adm_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # UserID
#     admin_Number = db.Column(db.String(30), unique=True, nullable=False) #AdminNumber
#     name = db.Column(db.String(255), nullable=False)  # Name
#     email = db.Column(db.String(100), unique=True, nullable=False)  # Email
#     password = db.Column(db.String(128), nullable=False)  # Password
#     gender = db.Column(db.Integer)  # Gender
#     dateofBirth = db.Column(db.Date)  # dateofBirth
#     placeofBirth = db.Column(db.String(100))  # placeofBirth
#     mobile_number = db.Column(db.String(11))  # MobileNumber
#     is_active = db.Column(db.Boolean, default=True)

#     def to_dict(self):
#         return {
#             'adm_Id': self.adm_Id,
#             'admin_Number': self.admin_Number,
#             'name': self.name,
#             'email': self.email,
#             'password': self.password,
#             'gender': self.gender,
#             'dateofBirth': self.dateofBirth,
#             'placeofBirth': self.placeofBirth,
#             'mobile_number': self.mobile_number,
#             'is_active': self.is_active
#         }
#     def get_id(self):
#         return str(self.id)  # Convert to string to ensure compatibility
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
            'IsValidPUPQCCourses': self.IsValidPUPQCCourses,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

# Student Enrolled in the courses
class CourseEnrolled(db.Model):
    __tablename__ = 'SPSCourseEnrolled'

    CourseId = db.Column(db.Integer, db.ForeignKey('SPSCourse.CourseId', ondelete="CASCADE"), primary_key=True)  # Unique Identifier
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True)# Students Reference
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
            'Status': self.Status,
            'CurriculumYear': self.CurriculumYear,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

# Metadata containing the details of class such as Year, Semester, Batch and Course
class Metadata(db.Model):
    __tablename__ = 'SPSMetadata'

    MetadataId = db.Column(db.Integer, primary_key=True, autoincrement=True) # Unique Identifier
    CourseId = db.Column(db.Integer, db.ForeignKey('SPSCourse.CourseId', ondelete="CASCADE")) # Course References
    Year = db.Column(db.Integer, nullable=False) # (1, 2, 3, 4) - Current year of the class 
    Semester = db.Column(db.Integer, nullable=False) # (1, 2, 3) - Current Semester of class
    Batch = db.Column(db.Integer, nullable=False) # (2019, 2020, 2021, ...) - Batch of the class
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'MetadataId': self.MetadataId,
            'CourseId': self.CourseId,
            'Year': self.Year,
            'Semester': self.Semester,
            'Batch': self.Batch,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

# Class Details 
class Class(db.Model):
    __tablename__ = 'SPSClass'

    ClassId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MetadataId = db.Column(db.Integer, db.ForeignKey('SPSMetadata.MetadataId', ondelete="CASCADE")) # Metadata containing details of class year, Semester, batch, course
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
            'MetadataId': self.MetadataId,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
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
            'created_at': self.created_at,
            'updated_at': self.updated_at,
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
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        
class StudentClassGrade(db.Model):
    __tablename__ = 'SPSStudentClassGrade'
    
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) # Referencing to Student
    ClassId = db.Column(db.Integer, db.ForeignKey('SPSClass.ClassId', ondelete="CASCADE"), primary_key=True) # Referencing to the Class
    Grade = db.Column(db.Float) # Average Grade
    Lister = db.Column(db.Integer, default=0) # 1 - President, 2 - Dean, 0 - Not Lister
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'StudentId': self.StudentId,
            'ClassId': self.ClassId,
            'Grade': self.Grade,
            'Lister': self.Lister,  
            'created_at': self.created_at,
            'updated_at': self.updated_at, 
        }

# Student Class Subject Grade contains the student Class subject that they currently taking in

class StudentClassSubjectGrade(db.Model):
    __tablename__ = 'SPSStudentClassSubjectGrade'

    StudentClassSubjectGradeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClassSubjectId = db.Column(db.Integer, db.ForeignKey('SPSClassSubject.ClassSubjectId', ondelete="CASCADE"), primary_key=True) # Reference to the class subject
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True)# Referencing to the student in subject taken
    Grade = db.Column(db.Float) # Students Gradec
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
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

# Curriculum is the list of subject that must taken of specific Course, Year, Semester and Batch. Subject automatically added in class when there is a curriculum
class Curriculum(db.Model):
    __tablename__ = 'SPSCurriculum'

    CurriculumId = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    SubjectId = db.Column(db.Integer, db.ForeignKey('SPSSubject.SubjectId', ondelete="CASCADE")) # Subejct that can be added in the classes if the same year, Semester, course and batch
    MetadataId = db.Column(db.Integer, db.ForeignKey('SPSMetadata.MetadataId', ondelete="CASCADE"), nullable=False) # Metadata contains the year, Semester, course and batch
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'CurriculumId': self.CurriculumId,
            'SubjectId': self.SubjectId,
            'MetadataId': self.MetadataId,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            # Add other attributes if needed
        }

# class Services(db.Model):
#     __tablename__ = 'SASSServices'
    
#     ServiceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     StudentId = db.Column(db. Integer, db.ForeignKey('SPSStudent.StudentId'))
#     FacultyId = db.Column(db. Integer, db.ForeignKey('FISFaculty.FacultyId'), nullable=False)
#     ServiceType = db.Column(db.String(100))
#     ServiceDetails = db.Column(db.String(255))
#     ServicesImg = db.Column(db.LargeBinary)
#     Servicesdata = db.Column(db.LargeBinary)  # Store binary data for the file
#     Status = db.Column(db.String(20))
    
#     def to_dict(self):
#         return {
#             'ServiceId': self.ServiceId,
#             'StudentId': self.StudentId,
#             'FacultyId': self.FacultyId,
#             'ServiceType': self.ServiceType,
#             'ServiceDetails': self.ServiceDetails,
#             'ServicesImg': self.ServicesImg,
#             'Servicesdata': self.Servicesdata,
#             'Status': self.Status,

#         }
        
# This table will trigger everytime there is addded new batch Semester
class LatestBatchSemester(db.Model):
    __tablename__ = 'SPSLatestBatchSemester'

    LatestBatchSemesterId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Batch = db.Column(db.Integer, nullable=False) # (2019, 2020, 2021, ...) - Batch course grades
    Semester = db.Column(db.Integer, nullable=False) # (1, 2, 3) - Semester
    IsEnrollmentStarted = db.Column(db.Boolean, default=False)
    IsGradeFinalized = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'LatestBatchSemesterId': self.LatestBatchSemesterId,
            'Batch': self.Batch,
            'Semester': self.Semester,
            'IsEnrollmentStarted': self.IsEnrollmentStarted,
            'IsGradeFinalized': self.IsGradeFinalized
            # Add other attributes if needed
        }
    
# Average Grade of Class
class ClassGrade(db.Model):
    __tablename__ = 'SPSClassGrade'

    ClassGradeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClassId = db.Column(db.Integer, db.ForeignKey('SPSClass.ClassId', ondelete="CASCADE"), unique=True) # Class reference
    DeansLister = db.Column(db.Integer) # Amount of DeansLister
    PresidentsLister = db.Column(db.Integer) # Amount of PresidentsLister
    Grade = db.Column(db.Float) # Average Grade of the class
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'ClassGradeId': self.ClassGradeId,
            'ClassId': self.ClassId,
            'DeanLister': self.DeanLister,
            'PresidentLister': self.PresidentLister,
            'Grade': self.Grade
        }

    
# Average Grade of Course in specific year and Semester
class CourseGrade(db.Model):
    __tablename__ = 'SPSCourseGrade'

    CourseGradeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseId = db.Column(db.Integer, db.ForeignKey('SPSCourse.CourseId', ondelete="CASCADE")) # Referenccing to specific course
    Batch = db.Column(db.Integer, primary_key=True) # (2019, 2020, 2021, ...) - Batch course grades
    Semester = db.Column(db.Integer, primary_key=True, nullable=False) # (1, 2, 3) - Semester
    Grade = db.Column(db.Float) # Average grade of course
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'CourseGradeId': self.CourseGradeId,
            'CourseId': self.CourseId,
            'Year': self.Year,
            'Grade': self.Grade,
        }

# class SubjectList(db.Model):
#     __tablename__ = 'SASSClassSubjectList'
    
#     SubjectListId = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId'))
#     SubjectId = db.Column(db.Integer, db.ForeignKey('SPSSubject.SubjectId'))
#     ServiceId = db.Column(db.Integer, db.ForeignKey('SASSServices.ServiceId'))
    
#     def to_dict(self):
#         return {
#             'SubjectListId': self.SubjectListId,
#             'SubjectId': self.SubjectId,
#             'ServiceId': self.ServiceId,
#             # Add other attributes if needed
#         }

#======================================================#
#==============Link with the Students==================#
#======================================================#
# SassSubject
class AddSubjects(db.Model):
    __tablename__ = 'SASSAddSubjects'
    
    AddSubjectId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId =db.Column(db. Integer, db.ForeignKey('SPSStudent.StudentId'))
    FacultyRole =db.Column(db. String(50))
    Subject = db.Column(db.String(255))
    ServiceDetails = db.Column(db.String(255))
    SenderName = db.Column(db.String(50))
    SenderContactNo = db.Column(db.String(50))
    PaymentFile = db.Column(db.LargeBinary)
    Status = db.Column(db.String(20))
    Remarks =db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'AddSubjectId': self.AddSubjectId,
            'StudentId': self.StudentId,
            'FacultyRole': self.FacultyRole,
            'SubjectId': self.Subject,
            'ServiceDetails': self.ServiceDetails,
            'SenderName': self.SenderName,
            'SenderContactNo': self.SenderContactNo,
            'PaymentFile': self.PaymentFile,
            'Status': self.Status,
            'Remarks': self.Remarks

        }
#Notification
class Notification(db.Model, UserMixin):
    __tablename__ = 'SASSNotifications'

    NotificationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) 
    StudentNumber = db.Column(db.String(100), nullable=False)
    ServiceType = db.Column(db.String(100), nullable=False)
    UserResponsible = db.Column(db.String(255), nullable=False)
    Status = db.Column(db.String(100), nullable=False)
    Message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def to_dict(self):
        return {
            'NotificationId': self.NotificationId,
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'ServiceType': self.ServiceType,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
            'Message': self.Message,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


#======================================================#       
#Announcements
class Announcement(db.Model):
    __tablename__ = 'SASSAnnouncement'

    AnnouncementId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FacultyId = db.Column(db.Integer, db.ForeignKey('FISFaculty.FacultyId'))
    SystemAdminId = db.Column(db.Integer, db.ForeignKey('SPSSystemAdmin.SysAdminId'))
    AnnouncementType = db.Column(db.String(255))
    AnnouncementDetails = db.Column(db.Text)  # Fixing typo in column name
    DatePosted = db.Column(db.DateTime)
    AnnouncementFile = db.Column(db.String(50))

    def to_dict(self):
        return {
            'AnnouncementId': self.AnnouncementId,
            'FacultyId': self.FacultyId,
            'AnnouncementType': self.AnnouncementType,
            'AnnouncementDetails': self.AnnouncementDetails,
            'DatePosted': self.DatePosted,
            'AnnouncementFile': self.AnnouncementFile,
        }   


#angela data table
class ESISAnnouncement(db.Model):
    __tablename__ = 'ESISAnnouncement'

    # Assuming AnnouncementId is the primary key
    AnnouncementId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    CreatorId = db.Column(db.Integer, nullable=False)  # Assuming this references another table
    IsLive = db.Column(db.Boolean, default=False)
    Slug = db.Column(db.String(255), unique=True)
    Created = db.Column(db.DateTime, default=datetime.now)
    Updated = db.Column(db.DateTime, onupdate=datetime.now)
    Recipient = db.Column(db.String(255))  # Modify as needed based on recipient structure
    ImageUrl = db.Column(db.String(255))
    ImageId = db.Column(db.Integer)  # Modify as needed if it references another table
    ProjectId = db.Column(db.Integer)  # Modify as needed if it references another table

#hayme table
class Announcements(db.Model):
    __tablename__ = 'APMSAnnouncement' 
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    created_at = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = db.Column(TIMESTAMP(timezone=True))  # Deletion timestamp (null if not deleted)
    title = db.Column('Title', db.String)
    content = db.Column('Content', db.Text)
    post_type = db.Column('PostType', db.String)  # Discriminator column
    img_link = db.Column('ImgLink', db.String)
    # uploader_id = db.Column('UploaderId', db.UUID(as_uuid=True), db.ForeignKey('APMSUser.id', ondelete="CASCADE"))

#======================================================#       

# ==========Services========== #
# ==========Adding_subject_form========== #
# class AddSubjects(db.Model, UserMixin):
#     __tablename__ = 'SASSAddSubjects'

#     SubjectId = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) 
#     StudentNumber = db.Column(db.String(100), nullable=False)
#     Name = db.Column(db.String(255), nullable=False)  
#     SubjectNames = db.Column(db.String(255), nullable=False)
#     EnrollmentType = db.Column(db.String(100))  # 'regular50or 'irregular'
#     AddSubjectFiledata = db.Column(db.LargeBinary)  # Store binary data for the file
#     AddSubjectFilefilename = db.Column(db.String(255))  # Store the filename
#     UserResponsible = db.Column(db.String(255))  # Add user role attribute
#     Status = db.Column(db.String(100))
#     created_at = db.Column(db.TIMESTAMP, default=datetime.now)
#     updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

#     def to_dict(self):
#         return {
#             'SubjectId': self.SubjectId,
#             'StudentId': self.StudentId,
#             'StudentNumber': self.StudentNumber,
#             'Name': self.Name,
#             'SubjectNames': self.SubjectNames,
#             'EnrollmentType': self.EnrollmentType,
#             'AddSubjectFiledata': self.AddSubjectFiledata,
#             'AddSubjectFilefilename': self.AddSubjectFilefilename,
#             'UserResponsible': self.UserResponsible,  # Include user role in the dictionary
#             'Status': self.Status,
#         }

#     def get_AddSubjectsID(self):
#         return str(self.SubjectId)
    
# ==========Services========== #
# ==========Change_of_subjects=========== #
class ChangeSubject(db.Model):
    __tablename__ = 'SASSChangeSubjects'
    
    ChangeSubjectId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId =db.Column(db. Integer, db.ForeignKey('SPSStudent.StudentId'))
    FacultyRole =db.Column(db. String(50))
    FromSubject = db.Column(db.String(255))
    ToSubject = db.Column(db.String(255))
    ServiceDetails = db.Column(db.String(255))
    SenderName = db.Column(db.String(255))
    SenderContactNo = db.Column(db.String(255))
    PaymentFile = db.Column(db.LargeBinary)
    Status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'ChangeSubjectId': self.ChangeSubjectId,
            'StudentId': self.StudentId,
            'FacultyRole': self.FacultyRole,
            'FromSubject': self.FromSubject,
            'ToSubject': self.ToSubject,
            'ServiceDetails': self.ServiceDetails,
            'SenderName': self.SenderName,
            'SenderContactNo': self.SenderContactNo,
            'PaymentFile': self.PaymentFile,
            'Status': self.Status,

        }

# ==========Requests========== #
# ========== Reason need pdf file ========== #
class ManualEnrollment(db.Model, UserMixin):
    __tablename__ = 'SASSManualEnrollment'

    ManualEnrollmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) 
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    EnrollmentType = db.Column(db.String(100), nullable=False)
    Reason = db.Column(db.Text, nullable=False)
    MeFilefilename = db.Column(db.String(255))
    MeFiledata = db.Column(db.LargeBinary)
    UserResponsible = db.Column(db.String(255))  # Add user role attribute
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'ManualEnrollmentId': self.ManualEnrollmentId,
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'EnrollmentType': self.EnrollmentType,
            'Reason': self.Reason,
            'MeFilefilename': self.MeFilefilename,
            'MeFiledata': self.MeFiledata,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ==========Requests========== #
# ========== Files needed for the Certification ========== #

class CertificationRequest(db.Model, UserMixin):
    __tablename__ = 'SASSCertification'

    CertificationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) 
    StudentNumber = db.Column(db.String(255), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    CertificationType = db.Column(db.String(100), nullable=False)
    RequestFormfilename = db.Column(db.String(255), nullable=False)
    RequestFormdata = db.Column(db.LargeBinary)
    IdentificationCardfilename = db.Column(db.String(255), nullable=False)
    IdentificationCarddata = db.Column(db.LargeBinary)
    IsRepresentative = db.Column(db.Boolean, default=False)
    AuthorizationLetterfilename = db.Column(db.String(255))
    AuthorizationLetterdata = db.Column(db.LargeBinary)
    RepresentativeIdfilename = db.Column(db.String(255))
    RepresentativeIddata = db.Column(db.LargeBinary)
    UserResponsible = db.Column(db.String(255)) 
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    def to_dict(self):
        return {
            'CertificationId': self.CertificationId,
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'CertificationType': self.CertificationType,
            'RequestFormfilename': self.RequestFormfilename,
            'RequestFormdata': self.RequestFormdata,
            'IdentificationCardfilename': self.IdentificationCardfilename,
            'IdentificationCarddata': self.IdentificationCarddata,
            'IsRepresentative': self.IsRepresentative,
            'AuthorizationLetterfilename': self.AuthorizationLetterfilename,
            'AuthorizationLetterdata': self.AuthorizationLetterdata,
            'RepresentativeIdfilename': self.RepresentativeIdfilename,
            'RepresentativeIddata': self.RepresentativeIddata,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
        }

# ========== Requests ========== #
class GradeEntry(db.Model, UserMixin):
    __tablename__ = 'SASSGradeEntry'

    GradeEntryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId')) 

    StudentNumber =db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    ApplicationType = db.Column(db.String(150), nullable=False)
    CompletionFormfilename = db.Column(db.String(255), nullable=False)
    CompletionFormdata = db.Column(db.LargeBinary)  # Add this line
    ClassRecordfilename = db.Column(db.String(255), nullable=False)
    ClassRecorddata = db.Column(db.LargeBinary)  # Add this line
    Affidavitfilename = db.Column(db.String(255), nullable=False)
    Affidavitdata = db.Column(db.LargeBinary)  # Add this line
    UserResponsible = db.Column(db.String(100)) 
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'GradeEntryId': self.GradeEntryId,
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'ApplicationType': self.ApplicationType,
            'CompletionFormfilename': self.CompletionFormfilename,
            'CompletionFormdata': self.CompletionFormdata,  # Add this line
            'ClassRecordfilename': self.ClassRecordfilename,
            'ClassRecorddata': self.ClassRecorddata,  # Add this line
            'Affidavitfilename': self.Affidavitfilename,
            'Affidavitdata': self.Affidavitdata,  # Add this line
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
        }

    
# ==========Requests========== #  
# ========== Files needed to the request ========== #
class CrossEnrollment(db.Model, UserMixin):
    __tablename__ = 'SASSCrossEnrollment'

    CrossEnrollmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True)  
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    SchoolforCrossEnrollment = db.Column(db.String(255), nullable=False)
    TotalNumberofUnits = db.Column(db.Integer, nullable=False)
    AuthorizedSubjectstoTake = db.Column(db.Text, nullable=False)
    ApplicationLetterfilename = db.Column(db.String(255), nullable=False)
    ApplicationLetterdata = db.Column(db.LargeBinary)  # Add this line
    PermitCrossEnrollfilename = db.Column(db.String(255), nullable=False)
    PermitCrossEnrolldata = db.Column(db.LargeBinary)  # Add
    UserResponsible = db.Column(db.String(255)) 
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    def to_dict(self):
        return {
            'CrossEnrollmentId': self.CrossEnrollmentId,
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'SchoolforCrossEnrollment': self.SchoolforCrossEnrollment,
            'TotalNumberofUnits': self.TotalNumberofUnits,
            'AuthorizedSubjectstoTake': self.AuthorizedSubjectstoTake,
            'ApplicationLetterfilename': self.ApplicationLetterfilename,
            'ApplicationLetterdata': self.ApplicationLetterdata,  # Add this line
            'PermitCrossEnrollfilename': self.PermitCrossEnrollfilename,
            'PermitCrossEnrolldata': self.PermitCrossEnrolldata,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
            'StudentId': self.StudentId,
        }

    
# ==========Requests========== #
class PetitionRequest(db.Model, UserMixin):
    __tablename__ = 'SASSPetitionRequest'

    PetitionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) 
    StudentNumber = db.Column(db.String(100), nullable=False)#/Student number dpat ito/
    Name = db.Column(db.String(255), nullable=False)
    SubjectCode = db.Column(db.String(100), nullable=False)
    SubjectName = db.Column(db.String(255), nullable=False)
    PetitionType = db.Column(db.String(100), nullable=False)
    RequestReason = db.Column(db.Text, nullable=False)
    UserResponsible = db.Column(db.String(255)) 
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    def to_dict(self):
        return {
            'PetitionId': self.PetitionId,
            'StudentId': self.StudentId,
            'StudentNumber':self.StudentNumber,
            'Name': self.Name,
            'SubjectCode': self.SubjectCode,
            'SubjectName': self.SubjectName,
            'PetitionType': self.PetitionType,
            'RequestReason': self.RequestReason,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
        }

    
# ==========Services========== #  
# ========Accreditation-for-Shiftees-and-Regular========= #  
class ShiftingApplication(db.Model, UserMixin):
    __tablename__ = 'SASSShiftingApplication'

    ShiftingId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    CurrentProgram = db.Column(db.String(255), nullable=False)
    ResidencyYear = db.Column(db.Integer, nullable=False)
    IntendedProgram = db.Column(db.String(255), nullable=False)
    Qualifications = db.Column(db.Text)
    Shiftingfilename = db.Column(db.String(255))
    Shiftingdata = db.Column(db.LargeBinary)
    UserResponsible = db.Column(db.String(255)) 
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now) 

    def to_dict(self):
        return {
            'ShiftingId': self.ShiftingId,
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'CurrentProgram': self.CurrentProgram,
            'ResidencyYear': self.ResidencyYear,
            'IntendedProgram': self.IntendedProgram,
            'Qualifications': self.Qualifications,
            'Shiftingfilename': self.Shiftingfilename,
            'Shiftingdata': self.Shiftingdata,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
        }

# ==========Services========== #
# ==========Overload-3-6-units========== #
class OverloadApplication(db.Model, UserMixin):
    __tablename__ = 'SASSOverloadApplication'

    OverloadId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True) 
    Name = db.Column(db.String(255), nullable=False)
    StudentNumber = db.Column(db.String(100), nullable=False)
    ProgramCourse = db.Column(db.String(255), nullable=False)
    Semester = db.Column(db.String(20), nullable=False)
    SubjectsToAdd = db.Column(db.String(255), nullable=False)
    Justification = db.Column(db.Text, nullable=False)
    Overloadfilename = db.Column(db.String(255))
    Overloaddata = db.Column(db.LargeBinary)
    UserResponsible = db.Column(db.String(255))
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'OverloadId':  self.OverloadId,
            'StudentId': self.StudentId,
            'Name': self.Name,
            'StudentNumber': self.StudentNumber,
            'ProgramCourse':self.ProgramCourse,
            'Semester': self.Semester,
            'SubjectsToAdd': self.SubjectsToAdd,
            'Justification': self.Justification,
            'Overloadfilename': self.Overloadfilename,
            'Overloaddata': self.Overloaddata,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
        }

#Done
# ==========Services========== #
# ==========RO FORM========== #
class TutorialRequest(db.Model, UserMixin):
    __tablename__ = 'SASSTutorialRequest'

    TutorialId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentId = db.Column(db.Integer, db.ForeignKey('SPSStudent.StudentId', ondelete="CASCADE"), primary_key=True)
    StudentNumber = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    SubjectCode = db.Column(db.String(100), nullable=False)
    SubjectName = db.Column(db.String(255), nullable=False)
    Tutorialfilename = db.Column(db.String(255))
    Tutorialdata = db.Column(db.LargeBinary)
    UserResponsible = db.Column(db.String(255))
    Status = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

 #Status 
    
     
    def to_dict(self):
        return {
            'TutorialId': self.TutorialId,
            'StudentId': self.StudentId,
            'StudentNumber': self.StudentNumber,
            'Name': self.Name,
            'SubjectCode': self.SubjectCode,
            'SubjectName': self.SubjectName,
            'Tutorialdata': self.Tutorialdata,
            'Tutorialfilename': self.Tutorialfilename,
            'created_at': self.created_at,
            'UserResponsible': self.UserResponsible,
            'Status': self.Status,
        }

# ------------------------------------------------
# List of Faculty that is being called in the services needed
# FacultyList
# 
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
        # from data.student import student_data #done
        # from data.faculty import faculty_data #done
        # from data.systemadmin import system_admin_data
        # from data.course import course_data
        # from data.subject import subject_data
        # from data.metadata import metadata_data
        # from data.curriculum import curriculum_data
        # from data.courseEnrolled import course_enrolled_data
        # from data.classes import class_data
        # from data.classSubject import class_subject_data
        # from data.classSubjectGrade import class_subject_grade_data
        # from data.studentClassSubjectGrade import student_class_subject_grade_data # DONT HAVE DATA YET
        # from data.studentClassGrade import student_class_grade_data
        # from data.classGrade import class_grade_data # NOT IN MODELS
        # from data.courseGrade import course_grade_data
        # from data.latestBatchSemester import batch_semester_data

        def create_sample_data():
            # print('adding')
            # for data in student_data:
            #     student = Student(**data)
            #     db.session.add(student)

            # for data in faculty_data:
            #     faculty = Faculty(**data) 
            #     db.session.add(faculty)

            # for data in system_admin_data:
            #     system_admin = SystemAdmin(**data) 
            #     db.session.add(system_admin)

            # for data in course_data:
            #     course = Course(**data)
            #     db.session.add(course) 
            #     db.session.flush()
                
            # for data in subject_data:
            #     subject = Subject(**data) 
            #     db.session.add(subject)
            #     db.session.flush()

            # for data in metadata_data:
            #     metadata = Metadata(**data) 
            #     db.session.add(metadata)
            #     db.session.flush()

            # for data in curriculum_data:
            #     curriculum = Curriculum(**data) 
            #     db.session.add(curriculum)
            #     db.session.flush()
                
            # for data in course_enrolled_data:
            #     course_enrolled = CourseEnrolled(**data) 
            #     db.session.add(course_enrolled)
            #     db.session.flush()

            
            # for data in class_data:
            #     class_ = Class(**data)
            #     db.session.add(class_)
            #     db.session.flush()

            # for data in class_subject_data:
            #     class_subject = ClassSubject(**data) 
            #     db.session.add(class_subject)
            #     db.session.flush()
 
            # for data in student_class_grade_data:
            #     student_class_grade = StudentClassGrade(**data)
            #     db.session.add(student_class_grade)
            #     db.session.flush()
                
            # for data in student_class_subject_grade_data:
            #     student_class_subject_grade = StudentClassSubjectGrade(**data) # DONT HAVE DATA YET
            #     db.session.add(student_class_subject_grade)
            #     db.session.flush()

            # for data in course_grade_data:
            #     course_grade = CourseGrade(**data) # walang data model
            #     db.session.add(course_grade)
            #     db.session.flush()

            # for data in batch_semester_data:
            #     latest_batch_semester = LatestBatchSemester(**data)
            #     db.session.add(latest_batch_semester)
            #     db.session.flush()
                 
            db.session.commit()
            db.session.close()

        
        # if config_mode == 'development' :
        #     with app.app_context():
        #         inspector = inspect(db.engine)
        #         db.create_all()

        #         if add_data=='False':
        #             print("DEVELOPMENT AND ADDING DATA")
        #             create_sample_data()


        if config_mode == 'development' and add_data=='True':
            # print("DEVELOPMENT AND ADDING DATA")
            with app.app_context():
                inspector = inspect(db.engine)
                # if not inspector.has_table('SPSStudent'):
                db.create_all()
                create_sample_data()