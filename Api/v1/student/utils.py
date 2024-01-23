
from models import AddSubjects, CertificationRequest, ChangeSubject, Class, Course, CrossEnrollment, Faculty, GradeEntry, ManualEnrollment, Metadata, OverloadApplication, PetitionRequest, ShiftingApplication, StudentClassGrade, LatestBatchSemester, StudentClassSubjectGrade, ClassSubject, Student, Subject, TutorialRequest, db, CourseEnrolled, Curriculum
from sqlalchemy import desc, func, and_
import re
from collections import defaultdict

from datetime import date, datetime


from flask import session, jsonify
from static.js.utils import convertGradeToPercentage, checkStatus
from flask_mail import Message
#from mail import mail
import pandas as pd
import random
import string
#from sqlalchemy.orm import Session
from sqlalchemy import func


#from collections import defaultdict





# DOING HERE
def getStudentClassSubjectData(classSubjectId, skip, top, order_by, filter):
    try:
        print('skip, top, order_by, filter: ', skip, top, order_by, filter)
        data_class_details = db.session.query(ClassSubject).filter_by(ClassSubjectId = classSubjectId).first()
        
        # Get the StudentClassSubjectGrade
        if data_class_details:
            data_student_subject_grade_query = db.session.query(StudentClassSubjectGrade, Student).join(Student, Student.StudentId == StudentClassSubjectGrade.StudentId)
            
            # Default filter
            # .filter(StudentClassSubjectGrade.ClassSubjectId == data_class_details.ClassSubjectId).all()
            
            filter_conditions = []
            
            filter_conditions.append(
                StudentClassSubjectGrade.ClassSubjectId == classSubjectId
            )
            
            if filter:
                filter_parts = filter.split(' and ')
                for part in filter_parts:
                    
                    # Check if part has to lower in value
                    if '(tolower(' in part:
                        # Extracting column name and value
                        column_name = part.split("(")[3].split("),'")[0]
                        value = part.split("'")[1]
                        # print column name and value
                        print('column_name, value: ', column_name, value)
                        column_str = None
                        if column_name.strip() == 'StudentNumber':
                            column_str = getattr(Student, 'StudentNumber')
                        elif column_name.strip() == 'Name':
                            column_str = getattr(Student, 'Name')
                        elif column_name.strip() == 'Email':
                            column_str =  getattr(Student, 'Email')     
                            
                        if column_str:
                            # Append column_str
                            filter_conditions.append(
                                func.lower(column_str).like(f'%{value}%')
                            )
                    else:
                        # column_name = part[0][1:]  # Remove the opening '('
                        column_name, value = [x.strip() for x in part[:-1].split("eq")]
                        column_name = column_name[1:]
                        
                        # print column name and value
                        print('column_name, value: ', column_name, value)
                        
                        column_num = None
                        int_value = value.strip(')')
                
                        if column_name.strip() == 'Grade':
                            column_num = StudentClassSubjectGrade.Grade
                        
                            filter_conditions.append(
                                column_num == int_value
                            )
                            
            filter_query = data_student_subject_grade_query.filter(and_(*filter_conditions))
            
            if order_by:
                # Determine the order attribute
                if order_by.split(' ')[0] == 'StudentNumber':
                    order_attr = getattr(Student, 'StudentNumber')
                elif order_by.split(' ')[0] == "Name":
                    order_attr = getattr(Student, 'Name')
                elif order_by.split(' ')[0] == 'Email':
                    order_attr = getattr(Student, 'Email')
                elif order_by.split(' ')[0] == 'Grade':
                    order_attr = getattr(StudentClassSubjectGrade, 'Grade')
                else:
                    order_attr = getattr(StudentClassSubjectGrade, 'DateEnrolled')
    
                if ' ' in order_by:
                    order_query = filter_query.order_by(desc(order_attr))
                else:
                    order_query = filter_query.order_by(order_attr)
            else:
                # Apply default sorting
                order_query = filter_query.order_by(desc(Student.StudentNumber))
        
        
            # Query for counting all records
            total_count = order_query.count()
            # Limitized query = 
            student_limit_offset_query = order_query.offset(skip).limit(top).all()
            
            if student_limit_offset_query:
                list_student_data = []
                    # For loop the data_student and put it in dictionary
                for student_subject_grade in student_limit_offset_query:
                    dict_student_subject_grade = {
                        'DateEnrolled': student_subject_grade.StudentClassSubjectGrade.DateEnrolled,
                        "ClassSubjectId": student_subject_grade.StudentClassSubjectGrade.ClassSubjectId,
                        "StudentId": student_subject_grade.Student.StudentId,
                        "StudentNumber": student_subject_grade.Student.StudentNumber,
                        "Name": student_subject_grade.Student.Name,
                        "Email": student_subject_grade.Student.Email,
                        "Grade": student_subject_grade.StudentClassSubjectGrade.Grade
                    }
                    list_student_data.append(dict_student_subject_grade)
                return  jsonify({'result': list_student_data, 'count': total_count}), 200
            else:
                return jsonify({'result': [], 'count': 0})
        else:
            return None
    except Exception as e:
        # Handle the exception here, e.g., log it or return an error response
        return None
    

#none in apiroutes
def getCurrentSubjectFaculty(str_student_id):
    try:
        print("Hello from current subject str_student_id: ", str_student_id)
        
        # Get the Class of student that the IsGradeFinalized is False
        # Metadata =  Year, Semester, BAtch
        # Class = Section
        # ClassSubject = #Reference to the class subject 
        # StudentClassSubjectGrade =# Reference to the class subject and have reference in student #Grade
        class_of_students = db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Metadata, Subject, StudentClassGrade)\
        .join(Class, Class.ClassId == ClassSubject.ClassId)\
        .join(Metadata, Metadata.MetadataId == Class.MetadataId)\
        .join(StudentClassSubjectGrade, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)\
        .filter(StudentClassGrade, StudentClassGrade.StudentId == StudentClassGrade.StudentId)\
        .all()

        print(class_of_students)

        lists = []

        for classofstudent in class_of_students:
            dict_class_subject = {
                "Subject Code": classofstudent.Subject.SubjectCode,
                "Subject Name": classofstudent.Subject.Name,
                "Section": classofstudent.Section,
                "Year": classofstudent.Meta.data.Year,
                "Semester": classofstudent.Course.Course.Semester,
            }


            lists.append(dict_class_subject)

        # Using that class get all class subject along with StudenClassSubjectGrade that has the same studentidFilter

        # dict 
        print(lists)
      
        return jsonify(lists)
    except Exception as e:
        # Handle exceptions appropriately
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

#1 - confirm
def getCurrentSubject(str_student_id):
    try:
        print("Hello from current subject str_student_id: ", str_student_id)
        
        # Get the Class of student that the IsGradeFinalized is False
        # Metadata =  Year, Semester, BAtch
        # Class = Section
        # ClassSubject = #Reference to the class subject 
        # StudentClassSubjectGrade =# Reference to the class subject and have reference in student #Grade
        class_of_students = db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Metadata, Subject)\
        .join(Class, Class.ClassId == ClassSubject.ClassId)\
        .join(Metadata, Metadata.MetadataId == Class.MetadataId)\
        .join(StudentClassSubjectGrade, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)\
        .join(Subject, Subject.SubjectId == ClassSubject.ClassSubjectId)\
        .filter(Class.IsGradeFinalized == True, StudentClassSubjectGrade.StudentId == str_student_id)\
        .all()

        print(class_of_students)

        list = []

        for classofstudent in class_of_students:
            dict_class_subject = {
                "Subject Code": classofstudent.Subject.SubjectCode,
                "Subject Name": classofstudent.Subject.Name,
            }


            list.append(dict_class_subject)

        # Using that class get all class subject along with StudenClassSubjectGrade that has the same studentidFilter

        # dict 
        print(list)
      
        return jsonify(list)
    except Exception as e:
        # Handle exceptions appropriately
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
#2 - confirm
def getSubjectsGrade(str_student_id):
    try:
        data_student_class_subject_grade = (
            db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Course, Subject, Metadata )
            .join(ClassSubject, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)
            .join(Class, ClassSubject.ClassId == Class.ClassId)
            .join(Metadata, Metadata.MetadataId == Class.MetadataId)
            .join(Course, Course.CourseId == Metadata.CourseId)
            .join(Subject, ClassSubject.SubjectId == Subject.SubjectId)
            .filter(StudentClassSubjectGrade.StudentId == str_student_id)
            .order_by(desc(Metadata.Batch), desc(Metadata.Semester))
            .all()
        )
        
        # print('data_student_class_subject_grade: '. )
        
        if data_student_class_subject_grade:
            class_combinations = set()
            dict_class_group = {}
            list_student_class_subject_grade = []

            for student_class_subject_grade in data_student_class_subject_grade:
                teacher_name = ""
                
                # Check if teacher exist
                if student_class_subject_grade.ClassSubject.FacultyId:
                    # Query the teacher
                    data_teacher = (
                        db.session.query(Faculty)
                        .filter(Faculty.FacultyId == student_class_subject_grade.ClassSubject.FacultyId)
                        .first()
                    )
                    teacher_name = data_teacher.LastName + ', ' + data_teacher.FirstName + ' ' + data_teacher.MiddleName
                
                
                class_combination = (
                    student_class_subject_grade.Class.ClassId,
                    student_class_subject_grade.Metadata.Batch,
                    student_class_subject_grade.Metadata.Semester
                )
                if class_combination not in class_combinations:
                    class_combinations.add(class_combination)

                    # Check if existing in the list table already the ClassId and semester so it wont reiterate the query
                    data_student_class_grade = (
                        db.session.query(StudentClassGrade)
                        .filter(StudentClassGrade.StudentId == str_student_id, StudentClassGrade.ClassId == student_class_subject_grade.Class.ClassId)
                        .first()
                    ) 
                    dict_class_group = {
                        "Batch": student_class_subject_grade.Metadata.Batch,
                        "GPA": format(data_student_class_grade.Grade, '.2f') if data_student_class_grade and data_student_class_grade.Grade is not None else "No GPA yet",
                        "Semester": student_class_subject_grade.Metadata.Semester,
                        "Subject": []
                    }

                    list_student_class_subject_grade.append(dict_class_group)
                
                # Append the subject details to the existing class group
                subject_details = {
                    "Grade": format(student_class_subject_grade.StudentClassSubjectGrade.Grade, '.2f') if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "0.00",
                    "Subject": student_class_subject_grade.Subject.Name,
                    "Code": student_class_subject_grade.Subject.SubjectCode,
                    "Teacher": teacher_name if teacher_name else "N/A",
                    "SecCode": f"{student_class_subject_grade.Course.CourseCode} {student_class_subject_grade.Metadata.Year}-{student_class_subject_grade.Class.Section}",
                    "Units": format(student_class_subject_grade.Subject.Units, '.2f'),
                    "Status": checkStatus(student_class_subject_grade.StudentClassSubjectGrade.Grade) if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "-"                
                }

                dict_class_group["Subject"].append(subject_details)
            return (list_student_class_subject_grade)

        else:
            return None
    except Exception as e:
        print("ERROR HERE: ", e)
        # Handle the exception here, e.g., log it or return an error response
        return None
    
    #studentclassgrade = classId
    #class = 
    #ClassSubject
#3 - confirm
def getStudentClassSGrade(str_student_id):
    try:       
        data_student_subject_grade = (
                db.session.query(StudentClassGrade, Class)
                .join(StudentClassGrade, StudentClassGrade.ClassId == Class.ClassId)
                .filter(Class.IsGradeFinalized == False, StudentClassGrade.StudentId == str_student_id)
                .all()
            )

        list_data_student_subject_grade = []

        for item in data_student_subject_grade:
            student_class_subject = (
                db.session.query(StudentClassSubjectGrade, ClassSubject, Subject, Class, Metadata, Course)
                .join(ClassSubject, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
                .join(Subject, Subject.SubjectId == ClassSubject.SubjectId)
                .join(Class, Class.ClassId == ClassSubject.ClassId)
                .join(Metadata, Metadata.MetadataId == Class.MetadataId)
                .join(Course, Course.CourseId == Metadata.CourseId)
                .filter(StudentClassSubjectGrade.StudentId == str_student_id, StudentClassSubjectGrade != 0, Class.ClassId == item.Class.ClassId)
                .all()
            )
            for data in student_class_subject:
                section_code = data.Course.CourseCode + ' ' + str(data.Metadata.Year) + '-' + str(data.Class.Section)
                teacher = data.ClassSubject.FacultyId if data.ClassSubject.FacultyId else ''

                subject_data = {
                    'SectionCode': section_code,
                    'SubjectName': data.Subject.Name,
                    'SubjectCode': data.Subject.SubjectCode,
                    'Teacher': teacher,
                    'Batch': data.Metadata.Batch,
                    'Year': data.Metadata.Year,
                    'Semester': data.Metadata.Semester,
                }

                list_data_student_subject_grade.append(subject_data)

        return jsonify(list_data_student_subject_grade)
    except Exception as e:
        print("ERROR HERE: ", e)
        # Handle the exception here, e.g., log it or return an error response
        return None

def getSubjectFuture(str_student_id):
    try:       
        no_list_subject = (
                db.session.query(CourseEnrolled, Curriculum, Metadata, Course)
                .join(CourseEnrolled, CourseEnrolled.CourseId == Course.CourseId)
                .join(Curriculum, Curriculum.MetadataId == Metadata.MetadataId)
                .join(Course, Course.CourseId == Metadata.CourseId)
                .filter(Class.IsGradeFinalized == False, StudentClassGrade.StudentId == str_student_id)
                .all()
            )
        print(no_list_subject)
        return jsonify(no_list_subject)
    except Exception as e:
        print("ERROR HERE: ", e)
        # Handle the exception here, e.g., log it or return an error response
        return None
#5
# def getAllSubjects(str_student_id):
#     try:
#         # Assuming you have a specific course ID, replace 'your_course_id' with the actual course ID
#         data_all_subjects = (
#             db.session.query(Subject, ClassSubject, Class, Metadata, Course, CourseEnrolled)
#             .join(ClassSubject, ClassSubject.SubjectId == Subject.SubjectId)
#             .join(Class, Class.ClassId == ClassSubject.ClassId)
#             .join(Metadata, Metadata.MetadataId == Class.MetadataId)
#             .join(CourseEnrolled, CourseEnrolled.CourseId == Metadata.CourseId)
#             .filter(Class.IsGradeFinalized == True, CourseEnrolled.StudentId == str_student_id)
#             .all()
#         )

#         list_data_subject_grade = []
#         print(list_data_subject_grade)
        
#         for data in data_all_subjects:
#             # Processing data and creating a dictionary
#             section_code = data.Course.CourseCode + ' ' + str(data.Metadata.Year) + '-' + str(data.Class.Section)
#             teacher = data.ClassSubject.FacultyId if data.ClassSubject.FacultyId else ''
#             subject_data = {
#                 'SectionCode': section_code,
#                 'SubjectName': data.Subject.Name,
#                 'SubjectCode': data.Subject.SubjectCode,
#                 'Teacher': teacher,
#                 'Batch': data.Metadata.Batch
#             }

#             list_data_subject_grade.append(subject_data)
#         return jsonify(list_data_subject_grade)
#     except Exception as e:
#         print("ERROR HERE: ", e)
#         return None
        
def getAllSubjects(str_student_id):
    try:
        # Query to fetch all subjects for the courses a student is enrolled in
        data_all_subjects = (
            db.session.query(Subject, ClassSubject, Class, Metadata, Course, CourseEnrolled)
            .join(ClassSubject, ClassSubject.SubjectId == Subject.SubjectId)
            .join(Class, Class.ClassId == ClassSubject.ClassId)
            .join(Metadata, Metadata.MetadataId == Class.MetadataId)
            .join(Course, Course.CourseId == Metadata.CourseId)
            .join(CourseEnrolled, CourseEnrolled.CourseId == Course.CourseId)
            .filter(CourseEnrolled.StudentId == str_student_id)
            .all()
        )

        list_data_subjects = []
        
        for subject, class_subject, class_, metadata, course, course_enrolled in data_all_subjects:
            # Creating a dictionary for each subject
            teacher = class_subject.FacultyId if class_subject.FacultyId else ''
            subject_data = {
                'SubjectName': subject.Name,
                'SubjectCode': subject.SubjectCode,
                'Teacher': teacher,
                'Batch': metadata.Batch
            }

            list_data_subjects.append(subject_data)

        return jsonify(list_data_subjects)
    except Exception as e:
        print("ERROR HERE: ", e)
        return None
    
def get_student_services(student_id):
    addsubject_list = AddSubjects.query.filter_by(StudentId=student_id).all()
    changesubjects_list = ChangeSubject.query.filter_by(StudentId=student_id).all()
    manual_enrollments_list = ManualEnrollment.query.filter_by(StudentId=student_id).all()
    certification_request_list = CertificationRequest.query.filter_by(StudentId=student_id).all()
    grade_entry_list = GradeEntry.query.filter_by(StudentId=student_id).all()
    cross_enrollment_list = CrossEnrollment.query.filter_by(StudentId=student_id).all()
    petition_requests_list = PetitionRequest.query.filter_by(StudentId=student_id).all()
    shifting_applications_list = ShiftingApplication.query.filter_by(StudentId=student_id).all()
    overload_applications_list = OverloadApplication.query.filter_by(StudentId=student_id).all()
    tutorial_requests_list = TutorialRequest.query.filter_by(StudentId=student_id).all()

    # Concatenate all lists into one comprehensive list
    all_services_list = (
        [subject.to_dict() for subject in addsubject_list] +
        [subject.to_dict() for subject in changesubjects_list] +
        [subject.to_dict() for subject in manual_enrollments_list] +
        [subject.to_dict() for subject in certification_request_list] +
        [subject.to_dict() for subject in grade_entry_list] +
        [subject.to_dict() for subject in cross_enrollment_list] +
        [subject.to_dict() for subject in petition_requests_list] +
        [subject.to_dict() for subject in shifting_applications_list] +
        [subject.to_dict() for subject in overload_applications_list] +
        [subject.to_dict() for subject in tutorial_requests_list]
    )
    total_services = len(all_services_list)
    # Count the number of services with status "pending"
    pending_count = sum(1 for service in all_services_list if service.get('Status') == 'pending')
    approved_count = sum(1 for service in all_services_list if service.get('Status') == 'Approved')
    denied_count = sum(1 for service in all_services_list if service.get('Status') == 'Rejected')

    print(f"Number of services with status 'pending': {pending_count}")
    print(f"Number of services with status 'approved': {approved_count}")
    print(f"Number of services with status 'rejected': {denied_count}")
    print(total_services)
    
    return all_services_list, total_services, pending_count, approved_count, denied_count

 
# def totalfailure(student_id=None):
#     try:
#         # Query to fetch student grades, join with CourseEnrolled and Metadata to get course and year level
#         query = (db.session.query(StudentClassGrade, Metadata.Year, Metadata.CourseId)
#                  .join(CourseEnrolled, CourseEnrolled.StudentId == StudentClassGrade.StudentId)
#                  .join(Metadata, Metadata.CourseId == CourseEnrolled.CourseId)
#                  .filter(and_(StudentClassGrade.Grade > 2.5, StudentClassGrade.Grade < 3.0))
#                  .all())

#         # Initialize an empty dictionary for course and year level counts
#         course_year_level_counts = {}

#         # Process query results to get count of students per course and year level
#         for record in query:
#             grade, year, course_id = record
#             if course_id not in course_year_level_counts:
#                 course_year_level_counts[course_id] = {}
#             course_year_level_counts[course_id][year] = course_year_level_counts[course_id].get(year, 0) + 1

#         print(course_year_level_counts)
#         return jsonify(course_year_level_counts)

#     except Exception as e:
#         print("ERROR HERE: ", e)
#         return None


def totalfailure(student_id=None):
    try:
        # Query to fetch student grades, join with CourseEnrolled and Metadata to get year level
        query = (db.session.query(StudentClassGrade, Metadata.Year)
                 .join(CourseEnrolled, CourseEnrolled.StudentId == StudentClassGrade.StudentId)
                 .join(Metadata, Metadata.CourseId == CourseEnrolled.CourseId)
                 .filter(and_(StudentClassGrade.Grade > 2.5, StudentClassGrade.Grade < 3.0))
                 .all())

        # Initialize an empty dictionary for year level counts
        year_level_counts = {}

        # Process query results to get count of students per year level
        for record in query:
            # Assuming record is a tuple with (StudentClassGrade, Year)
            Grade, year = record
            year_level_counts[year] = year_level_counts.get(year, 0) + 1

        print(record)
        return jsonify(year_level_counts)

    except Exception as e:
        print("ERROR HERE: ", e)
        return None
    
#======================================Failing per Batch===========================#
def failingradeperbatch():
    try:
        result = (
            db.session.query(
                Metadata.Batch,
                func.count(StudentClassSubjectGrade.AcademicStatus).label('status_count')
            )
            .join(Class, Metadata.MetadataId == Class.MetadataId)
            .join(ClassSubject, Class.ClassId == ClassSubject.ClassId)
            .join(StudentClassSubjectGrade, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
            .filter(StudentClassSubjectGrade.AcademicStatus == 2)
            .group_by(Metadata.Batch)
            .all()
        )

        # The result will be a list of tuples, each containing (Batch, status_count)
        for batch, count in result:
            print(f'Batch: {batch}, Count of AcademicStatus Failed == 2: {count}')

    except Exception as e:
        print("ERROR HERE: ", e)
        return None