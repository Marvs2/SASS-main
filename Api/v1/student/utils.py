
from models import AddSubjects, CertificationRequest, ChangeSubject, Class, Course, CrossEnrollment, Faculty, GradeEntry, ManualEnrollment, Metadata, OverloadApplication, PetitionRequest, ShiftingApplication, StudentClassGrade, LatestBatchSemester, StudentClassSubjectGrade, ClassSubject, Student, Subject, TutorialRequest, db, CourseEnrolled, Curriculum
from sqlalchemy import AliasedReturnsRows, desc, func, and_
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

        lists = []

        for classofstudent in class_of_students:
            dict_class_subject = {
                "Subject Code": classofstudent.Subject.SubjectCode,
                "Subject Name": classofstudent.Subject.Name,
                "Subject Description": classofstudent.Subject.Description,
                "Section": classofstudent.Section,
                "Year": classofstudent.Meta.data.Year,
                "Semester": classofstudent.Course.Course.Semester,
            }


            lists.append(dict_class_subject)

        # Using that class get all class subject along with StudenClassSubjectGrade that has the same studentidFilter

      
        return jsonify(lists)
    except Exception as e:
        # Handle exceptions appropriately
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

#1 - confirm
# def getCurrentSubject(str_student_id):
#     try:        
#         # Get the Class of student that the IsGradeFinalized is False
#         # Metadata =  Year, Semester, BAtch
#         # Class = Section
#         # ClassSubject = #Reference to the class subject 
#         # StudentClassSubjectGrade =# Reference to the class subject and have reference in student #Grade
#         class_of_students = db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Metadata, Subject)\
#         .join(Class, Class.ClassId == ClassSubject.ClassId)\
#         .join(Metadata, Metadata.MetadataId == Class.MetadataId)\
#         .join(StudentClassSubjectGrade, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)\
#         .join(Subject, Subject.SubjectId == ClassSubject.ClassSubjectId)\
#         .filter(Class.IsGradeFinalized == True, StudentClassSubjectGrade.StudentId == str_student_id)\
#         .all()

#         list = []

#         for classofstudent in class_of_students:
#             dict_class_subject = {
#                 "Subject Code": classofstudent.Subject.SubjectCode,
#                 "Subject Name": classofstudent.Subject.Name,
#                 "Subject Description": classofstudent.Subject.Description,
#             }


#             list.append(dict_class_subject)

#         # Using that class get all class subject along with StudenClassSubjectGrade that has the same studentidFilter

#         # dict       
#         return jsonify(list)
#     except Exception as e:
#         # Handle exceptions appropriately
#         print(f"Error: {e}")
#         return jsonify({'error': 'Internal Server Error'}), 500
def getCurrentSubject(str_student_id):
    try:
        # Get the Class of student that the IsGradeFinalized is False
        # Metadata =  Year, Semester, BAtch
        # Class = Section
        # ClassSubject = #Reference to the class subject 
        # StudentClassSubjectGrade =# Reference to the class subject and have reference in student #Grade
        class_of_students = db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Metadata, Subject, Course, CourseEnrolled)\
            .join(Class, Class.ClassId == ClassSubject.ClassId)\
            .join(Metadata, Metadata.MetadataId == Class.MetadataId)\
            .join(StudentClassSubjectGrade, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)\
            .join(Subject, Subject.SubjectId == ClassSubject.ClassSubjectId)\
            .join(Course, Course.CourseId == Metadata.CourseId)\
            .join(CourseEnrolled, CourseEnrolled.StudentId == str_student_id)\
            .filter(Class.IsGradeFinalized == True, StudentClassSubjectGrade.StudentId == str_student_id)\
            .all()

        subject_list = []

        for classofstudent in class_of_students:
            dict_class_subject = {
                "Subject Code": classofstudent.Subject.SubjectCode,
                "Subject Name": classofstudent.Subject.Name,
                "Subject Description": classofstudent.Subject.Description,
                "Course": {
                    "Course Code": classofstudent.Course.CourseCode,  # Update this based on your actual column name
                    "Course Name": classofstudent.Course.Name  # Update this based on your actual column name
                },
                "CourseEnrolled": {
                    "Enrollment Date": classofstudent.CourseEnrolled.DateEnrolled,  # Update this based on your actual column name
                    # Add other CourseEnrolled details as needed
                }
            }

            subject_list.append(dict_class_subject)

        # Using that class get all class subject along with StudenClassSubjectGrade that has the same studentidFilter
        # dict
        return jsonify(subject_list)
    except Exception as e:
        # Handle exceptions appropriately
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
# #1st Sem
# def getFirstSemSubjectsGrade(str_student_id):
#     try:
#         data_student_class_subject_grade = (
#             db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Course, Subject, Metadata)
#             .join(ClassSubject, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)
#             .join(Class, ClassSubject.ClassId == Class.ClassId)
#             .join(Metadata, Metadata.MetadataId == Class.MetadataId)
#             .join(Course, Course.CourseId == Metadata.CourseId)
#             .join(Subject, ClassSubject.SubjectId == Subject.SubjectId)
#             .filter(StudentClassSubjectGrade.StudentId == str_student_id,
#                     Metadata.Batch == 2023,
#                     Metadata.Semester == 1)
#             .order_by(desc(Metadata.Batch), desc(Metadata.Semester))
#             .all()
#         )

#         if data_student_class_subject_grade:
#             dict_semester_subjects = {}

#             for student_class_subject_grade in data_student_class_subject_grade:
#                 class_combination = (
#                     student_class_subject_grade.Class.ClassId,
#                     student_class_subject_grade.Metadata.Batch,
#                     student_class_subject_grade.Metadata.Semester
#                 )

#                 # Check if class_combination already processed for this semester
#                 if class_combination not in dict_semester_subjects:
#                     dict_semester_subjects[class_combination] = {
#                         "Batch": student_class_subject_grade.Metadata.Batch,
#                         "GPA": "No GPA yet",  # Initialize with default value
#                         "Semester": student_class_subject_grade.Metadata.Semester,
#                         "Subject": []
#                     }

#                 subject_code = student_class_subject_grade.Subject.SubjectCode
#                 # Check if the subject is already added for this semester
#                 if subject_code not in [subject["Code"] for subject in dict_semester_subjects[class_combination]["Subject"]]:
#                     subject_details = {
#                         "Grade": format(student_class_subject_grade.StudentClassSubjectGrade.Grade, '.2f') if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "0.00",
#                         "Subject": student_class_subject_grade.Subject.Name,
#                         "Code": subject_code,
#                         "SecCode": f"{student_class_subject_grade.Course.CourseCode} {student_class_subject_grade.Metadata.Year}-{student_class_subject_grade.Class.Section}",
#                         "Units": format(student_class_subject_grade.Subject.Units, '.2f'),
#                         "Status": checkStatus(student_class_subject_grade.StudentClassSubjectGrade.Grade) if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "-"
#                     }

#                     dict_semester_subjects[class_combination]["Subject"].append(subject_details)

#             # Convert the dictionary values to a list
#             list_student_class_subject_grade = list(dict_semester_subjects.values())
#             return list_student_class_subject_grade

#         else:
#             return None
#     except Exception as e:
#         print("ERROR HERE: ", e)
#         return None
    

#1st Sem with section, year , smester, course, grade, current
def getFirstSemSubjectsGrade(str_student_id):
    try:
        data_student_class_subject_grade = (
            db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Course, Subject, Metadata)
            .join(ClassSubject, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)
            .join(Class, ClassSubject.ClassId == Class.ClassId)
            .join(Metadata, Metadata.MetadataId == Class.MetadataId)
            .join(Course, Course.CourseId == Metadata.CourseId)
            .join(Subject, ClassSubject.SubjectId == Subject.SubjectId)
            .filter(StudentClassSubjectGrade.StudentId == str_student_id,
                    Metadata.Batch == 2023,
                    Metadata.Semester == 1)
            .order_by(desc(Metadata.Batch), desc(Metadata.Semester))
            .all()
        )

        if data_student_class_subject_grade:
            dict_semester_subjects = {}

            for student_class_subject_grade in data_student_class_subject_grade:
                class_combination = (
                    student_class_subject_grade.Class.ClassId,
                    student_class_subject_grade.Metadata.Batch,
                    student_class_subject_grade.Metadata.Semester
                )

                # Check if class_combination already processed for this semester
                if class_combination not in dict_semester_subjects:
                    dict_semester_subjects[class_combination] = {
                        "Batch": student_class_subject_grade.Metadata.Batch,
                        "GPA": "No GPA yet",  # Initialize with default value
                        "Semester": student_class_subject_grade.Metadata.Semester,
                        "Year": student_class_subject_grade.Metadata.Year,
                        "Section": student_class_subject_grade.Class.Section,  # Include Section in the result
                        "Subject": []
                    }

                subject_code = student_class_subject_grade.Subject.SubjectCode
                # Check if the subject is already added for this semester
                if subject_code not in [subject["Code"] for subject in dict_semester_subjects[class_combination]["Subject"]]:
                    subject_details = {
                        "Grade": format(student_class_subject_grade.StudentClassSubjectGrade.Grade, '.2f') if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "0.00",
                        "Subject": student_class_subject_grade.Subject.Name,
                        "Code": subject_code,
                        "SecCode": f"{student_class_subject_grade.Course.CourseCode} {student_class_subject_grade.Metadata.Year}-{student_class_subject_grade.Class.Section}",
                        "Units": format(student_class_subject_grade.Subject.Units, '.2f'),
                        "Status": checkStatus(student_class_subject_grade.StudentClassSubjectGrade.Grade) if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "-"
                    }

                    dict_semester_subjects[class_combination]["Subject"].append(subject_details)

            # Convert the dictionary values to a list
            list_student_class_subject_grade = list(dict_semester_subjects.values())
            return list_student_class_subject_grade

        else:
            return None
    except Exception as e:
        print("ERROR HERE: ", e)
        return None


#2nd Sem
def getSecondSemSubjectsGrade(str_student_id):
    try:
        data_student_class_subject_grade = (
            db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Course, Subject, Metadata)
            .join(ClassSubject, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)
            .join(Class, ClassSubject.ClassId == Class.ClassId)
            .join(Metadata, Metadata.MetadataId == Class.MetadataId)
            .join(Course, Course.CourseId == Metadata.CourseId)
            .join(Subject, ClassSubject.SubjectId == Subject.SubjectId)
            .filter(StudentClassSubjectGrade.StudentId == str_student_id,
                    Metadata.Semester == 2)  # Update filter for the second semester
            .order_by(desc(Metadata.Batch), desc(Metadata.Semester))
            .all()
        )

        if data_student_class_subject_grade:
            class_combinations = set()
            dict_class_group = {}
            list_student_class_subject_grade = []

            for student_class_subject_grade in data_student_class_subject_grade:
                teacher_name = ""

                if student_class_subject_grade.ClassSubject.FacultyId:
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

                    data_student_class_grade = (
                        db.session.query(StudentClassGrade)
                        .filter(StudentClassGrade.StudentId == str_student_id,
                                StudentClassGrade.ClassId == student_class_subject_grade.Class.ClassId)
                        .first()
                    )
                    dict_class_group = {
                        "Batch": student_class_subject_grade.Metadata.Batch,
                        "GPA": format(data_student_class_grade.Grade, '.2f') if data_student_class_grade and data_student_class_grade.Grade is not None else "No GPA yet",
                        "Semester": student_class_subject_grade.Metadata.Semester,
                        "Subject": []
                    }

                    list_student_class_subject_grade.append(dict_class_group)

                subject_details = {
                    "Grade": format(student_class_subject_grade.StudentClassSubjectGrade.Grade, '.2f') if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "0.00",
                    "Subject": student_class_subject_grade.Subject.Name,
                    "Code": student_class_subject_grade.Subject.SubjectCode,
                    "SecCode": f"{student_class_subject_grade.Course.CourseCode} {student_class_subject_grade.Metadata.Year}-{student_class_subject_grade.Class.Section}",
                    "Units": format(student_class_subject_grade.Subject.Units, '.2f'),
                    "Status": checkStatus(student_class_subject_grade.StudentClassSubjectGrade.Grade) if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "-"
                }

                dict_class_group["Subject"].append(subject_details)

            return list_student_class_subject_grade

        else:
            return None
    except Exception as e:
        print("ERROR HERE: ", e)
        return None
 
#ALL Grades until second lateet - confirm without courseenrolled - status
# def getSubjectsGrade(str_student_id):
#     try:
#         data_student_class_subject_grade = (
#             db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Course, Subject, Metadata )
#             .join(ClassSubject, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)
#             .join(Class, ClassSubject.ClassId == Class.ClassId)
#             .join(Metadata, Metadata.MetadataId == Class.MetadataId)
#             .join(Course, Course.CourseId == Metadata.CourseId)
#             .join(Subject, ClassSubject.SubjectId == Subject.SubjectId)
#             .filter(StudentClassSubjectGrade.StudentId == str_student_id)
#             .order_by(desc(Metadata.Batch), desc(Metadata.Semester))
#             .all()
#         )
        
#         # print('data_student_class_subject_grade: '. )
        
#         if data_student_class_subject_grade:
#             class_combinations = set()
#             dict_class_group = {}
#             list_student_class_subject_grade = []

#             for student_class_subject_grade in data_student_class_subject_grade:
#                 teacher_name = ""
                
#                 # Check if teacher exist
#                 if student_class_subject_grade.ClassSubject.FacultyId:
#                     # Query the teacher
#                     data_teacher = (
#                         db.session.query(Faculty)
#                         .filter(Faculty.FacultyId == student_class_subject_grade.ClassSubject.FacultyId)
#                         .first()
#                     )
#                     teacher_name = data_teacher.LastName + ', ' + data_teacher.FirstName + ' ', data_teacher.MiddleName
                
                
#                 class_combination = (
#                     student_class_subject_grade.Class.ClassId,
#                     student_class_subject_grade.Metadata.Batch,
#                     student_class_subject_grade.Metadata.Semester
#                 )
#                 if class_combination not in class_combinations:
#                     class_combinations.add(class_combination)

#                     # Check if existing in the list table already the ClassId and semester so it wont reiterate the query
#                     data_student_class_grade = (
#                         db.session.query(StudentClassGrade)
#                         .filter(StudentClassGrade.StudentId == str_student_id, StudentClassGrade.ClassId == student_class_subject_grade.Class.ClassId)
#                         .first()
#                     ) 
#                     dict_class_group = {
#                         "Batch": student_class_subject_grade.Metadata.Batch,
#                         "GPA": format(data_student_class_grade.Grade, '.2f') if data_student_class_grade and data_student_class_grade.Grade is not None else "No GPA yet",
#                         "Semester": student_class_subject_grade.Metadata.Semester,
#                         "Subject": []
#                     }

#                     list_student_class_subject_grade.append(dict_class_group)
                
#                 # Append the subject details to the existing class group
#                 subject_details = {
#                     "Grade": format(student_class_subject_grade.StudentClassSubjectGrade.Grade, '.2f') if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "0.00",
#                     "Subject": student_class_subject_grade.Subject.Name,
#                     "Code": student_class_subject_grade.Subject.SubjectCode,
#                     "Teacher": teacher_name if teacher_name else "N/A",
#                     "SecCode": f"{student_class_subject_grade.Course.CourseCode} {student_class_subject_grade.Metadata.Year}-{student_class_subject_grade.Class.Section}",
#                     "Units": format(student_class_subject_grade.Subject.Units, '.2f'),
#                     "Status": checkStatus(student_class_subject_grade.StudentClassSubjectGrade.Grade) if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "-"
                        
#                 }

#                 dict_class_group["Subject"].append(subject_details)
#             return (list_student_class_subject_grade)

#         else:
#             return None
#     except Exception as e:
#         print("ERROR: ", e)
#         # Handle the exception here, e.g., log it or return an error response
#         return None


def getSubjectsGrade(str_student_id):
    try:
        data_student_class_subject_grade = (
            db.session.query(
                StudentClassSubjectGrade, ClassSubject, Class, Course, Subject, Metadata, CourseEnrolled.Status
            )
            .join(ClassSubject, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)
            .join(Class, ClassSubject.ClassId == Class.ClassId)
            .join(Metadata, Metadata.MetadataId == Class.MetadataId)
            .join(Course, Course.CourseId == Metadata.CourseId)
            .join(Subject, ClassSubject.SubjectId == Subject.SubjectId)
            .join(CourseEnrolled, and_(
                    CourseEnrolled.StudentId == str_student_id,
                    CourseEnrolled.CourseId == Metadata.CourseId
                ))
            .filter(StudentClassSubjectGrade.StudentId == str_student_id)
            .order_by(desc(Metadata.Batch), desc(Metadata.Semester))
            .all()
        )

        if data_student_class_subject_grade:
            class_combinations = set()
            list_student_class_subject_grade = []

            for record in data_student_class_subject_grade:
                student_class_subject_grade, class_subject, class_, course, subject, metadata, course_enrolled_status = record
                teacher_name = ""

                # Check if teacher exists
                if class_subject.FacultyId:
                    # Query the teacher
                    data_teacher = db.session.query(Faculty).filter(Faculty.FacultyId == class_subject.FacultyId).first()
                    teacher_name = data_teacher.LastName + ', ' + data_teacher.FirstName + (' ' + data_teacher.MiddleName if data_teacher.MiddleName else '')

                class_combination = (class_.ClassId, metadata.Batch, metadata.Semester)
                if class_combination not in class_combinations:
                    class_combinations.add(class_combination)
                    # Check if existing in the list table already the ClassId and semester so it won't reiterate the query
                    data_student_class_grade = db.session.query(StudentClassGrade).filter(
                        StudentClassGrade.StudentId == str_student_id,
                        StudentClassGrade.ClassId == class_.ClassId
                    ).first()
                    enrollment_status = "Continuing" if course_enrolled_status == 0 else "Graduated"
                    dict_class_group = {
                        "Batch": metadata.Batch,
                        "GPA": format(data_student_class_grade.Grade, '.2f') if data_student_class_grade and data_student_class_grade.Grade is not None else "No GPA yet",
                        "Semester": metadata.Semester,
                        "Subject": [],
                        "EnrollmentStatus": enrollment_status,
                        "SecCode": f"{course.CourseCode} {metadata.Year}-{class_.Section} - {course.Name}"  # Added SecCode
                    }

                    list_student_class_subject_grade.append(dict_class_group)

                subject_details = {
                    "Grade": format(student_class_subject_grade.Grade, '.2f') if student_class_subject_grade.Grade is not None else "0.00",
                    "Subject": subject.Name,
                    "Code": subject.SubjectCode,
                    "Teacher": teacher_name if teacher_name else "N/A",
                    "SecCode": f"{course.CourseCode} {metadata.Year}-{class_.Section} - {course.Name}",
                    "Units": format(subject.Units, '.2f'),
                    "Status": "Pass" if student_class_subject_grade.Grade >= 75 else "Fail"  # Assuming 75 is the passing grade
                }

                # Find the last dictionary in list_student_class_subject_grade and append the subject details to its "Subject" list
                list_student_class_subject_grade[-1]["Subject"].append(subject_details)
                
            return list_student_class_subject_grade

        else:
            return None
    except Exception as e:
        print("ERROR: ", e)
        # Handle the exception here, e.g., log it or return an error response
        return None

#first
# def getSubjectsGrade(str_student_id):
#     try:
#         data_student_class_subject_grade = (
#             db.session.query(StudentClassSubjectGrade, ClassSubject, Class, Course, Subject, Metadata )
#             .join(ClassSubject, StudentClassSubjectGrade.ClassSubjectId == ClassSubject.ClassSubjectId)
#             .join(Class, ClassSubject.ClassId == Class.ClassId)
#             .join(Metadata, Metadata.MetadataId == Class.MetadataId)
#             .join(Course, Course.CourseId == Metadata.CourseId)
#             .join(Subject, ClassSubject.SubjectId == Subject.SubjectId)
#             .filter(StudentClassSubjectGrade.StudentId == str_student_id)
#             .order_by(desc(Metadata.Batch), desc(Metadata.Semester))
#             .all()
#         )
        
#         # print('data_student_class_subject_grade: '. )
        
#         if data_student_class_subject_grade:
#             class_combinations = set()
#             dict_class_group = {}
#             list_student_class_subject_grade = []

#             for student_class_subject_grade in data_student_class_subject_grade:
#                 teacher_name = ""
                
#                 # Check if teacher exist
#                 if student_class_subject_grade.ClassSubject.FacultyId:
#                     # Query the teacher
#                     data_teacher = (
#                         db.session.query(Faculty)
#                         .filter(Faculty.FacultyId == student_class_subject_grade.ClassSubject.FacultyId)
#                         .first()
#                     )
#                     teacher_name = data_teacher.LastName + ', ' + data_teacher.FirstName + ' ' + data_teacher.MiddleName
                
                
#                 class_combination = (
#                     student_class_subject_grade.Class.ClassId,
#                     student_class_subject_grade.Metadata.Batch,
#                     student_class_subject_grade.Metadata.Semester
#                 )
#                 if class_combination not in class_combinations:
#                     class_combinations.add(class_combination)

#                     # Check if existing in the list table already the ClassId and semester so it wont reiterate the query
#                     data_student_class_grade = (
#                         db.session.query(StudentClassGrade)
#                         .filter(StudentClassGrade.StudentId == str_student_id, StudentClassGrade.ClassId == student_class_subject_grade.Class.ClassId)
#                         .first()
#                     ) 
#                     dict_class_group = {
#                         "Batch": student_class_subject_grade.Metadata.Batch,
#                         "GPA": format(data_student_class_grade.Grade, '.2f') if data_student_class_grade and data_student_class_grade.Grade is not None else "No GPA yet",
#                         "Semester": student_class_subject_grade.Metadata.Semester,
#                         "Year": student_class_subject_grade.Metadata.Year,
#                         "Section": student_class_subject_grade.Class.Section,
#                         "Subject": []
#                     }

#                     list_student_class_subject_grade.append(dict_class_group)
                
#                 # Append the subject details to the existing class group
#                 subject_details = {
#                     "Grade": format(student_class_subject_grade.StudentClassSubjectGrade.Grade, '.2f') if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "0.00",
#                     "Subject": student_class_subject_grade.Subject.Name,
#                     "Code": student_class_subject_grade.Subject.SubjectCode,
#                     "SecCode": f"{student_class_subject_grade.Course.CourseCode} {student_class_subject_grade.Metadata.Year}-{student_class_subject_grade.Class.Section}",
#                     "Units": format(student_class_subject_grade.Subject.Units, '.2f'),
#                     "Status": checkStatus(student_class_subject_grade.StudentClassSubjectGrade.Grade) if student_class_subject_grade.StudentClassSubjectGrade.Grade is not None else "-"                
#                 }

#                 dict_class_group["Subject"].append(subject_details)
#             return (list_student_class_subject_grade)

#         else:
#             return None
#     except Exception as e:
#         print("ERROR HERE: ", e)
#         # Handle the exception here, e.g., log it or return an error response
#         return None
    
    #studentclassgrade = classId
    #class = 
    #ClassSubject
#3 - confirm
# def getStudentClassSGrade(str_student_id):
#     try:       
#         data_student_subject_grade = (
#                 db.session.query(StudentClassGrade, Class)
#                 .join(StudentClassGrade, StudentClassGrade.ClassId == Class.ClassId)
#                 .filter(Class.IsGradeFinalized == False, StudentClassGrade.StudentId == str_student_id)
#                 .all()
#             )

#         list_data_student_subject_grade = []

#         for item in data_student_subject_grade:
#             student_class_subject = (
#                 db.session.query(StudentClassSubjectGrade, ClassSubject, Subject, Class, Metadata, Course)
#                 .join(ClassSubject, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
#                 .join(Subject, Subject.SubjectId == ClassSubject.SubjectId)
#                 .join(Class, Class.ClassId == ClassSubject.ClassId)
#                 .join(Metadata, Metadata.MetadataId == Class.MetadataId)
#                 .join(Course, Course.CourseId == Metadata.CourseId)
#                 .filter(StudentClassSubjectGrade.StudentId == str_student_id, StudentClassSubjectGrade != 0, Class.ClassId == item.Class.ClassId)
#                 .all()
#             )
#             for data in student_class_subject:
#                 section_code = data.Course.CourseCode + ' ' + str(data.Metadata.Year) + '-' + str(data.Class.Section)
#                 teacher = data.ClassSubject.FacultyId if data.ClassSubject.FacultyId else ''

#                 subject_data = {
#                     'SectionCode': section_code,
#                     'SubjectName': data.Subject.Name,
#                     'SubjectCode': data.Subject.SubjectCode,
#                     'Batch': data.Metadata.Batch,
#                     'Year': data.Metadata.Year,
#                     'Semester': data.Metadata.Semester,
#                 }

#                 list_data_student_subject_grade.append(subject_data)

#         return jsonify(list_data_student_subject_grade)
#     except Exception as e:
#         print("ERROR HERE: ", e)
#         # Handle the exception here, e.g., log it or return an error response
#         return None
def getStudentClassSGrade(str_student_id):
    try:
        # Determine the current semester based on the month
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Define semester based on month
        if 3 <= current_month <= 8:
            # March to August - 2nd Semester of the previous academic year
            semester = 2
            academic_year = current_year - 1 if current_month < 6 else current_year
        elif 10 <= current_month <= 12:
            # October to December - 1st Semester of the current academic year
            semester = 1
            academic_year = current_year
        elif 1 <= current_month <= 2:
            # January to February - 1st Semester of the current academic year
            semester = 1
            academic_year = current_year
        else:
            # September - Summer of the current academic year
            semester = 'Summer'
            academic_year = current_year

        data_student_subject_grade = (
            db.session.query(StudentClassGrade, Class)
            .join(StudentClassGrade, StudentClassGrade.ClassId == Class.ClassId)
            .filter(Class.IsGradeFinalized == False, 
                    StudentClassGrade.StudentId == str_student_id,
                    Class.Metadata.Year == academic_year,
                    Class.Metadata.Semester == semester,
                    Class.Metadata.Month <= current_month)  # Filter out future semesters
            .all()
        )
        print(current_month)
        list_data_student_subject_grade = []

        for item in data_student_subject_grade:
            student_class_subject = (
                db.session.query(StudentClassSubjectGrade, ClassSubject, Subject, Class, Metadata, Course)
                .join(ClassSubject, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
                .join(Subject, Subject.SubjectId == ClassSubject.SubjectId)
                .join(Class, Class.ClassId == ClassSubject.ClassId)
                .join(Metadata, Metadata.MetadataId == Class.MetadataId)
                .join(Course, Course.CourseId == Metadata.CourseId)
                .filter(StudentClassSubjectGrade.StudentId == str_student_id, 
                        StudentClassSubjectGrade != 0, 
                        Class.ClassId == item.Class.ClassId)
                .all()
            )
            for data in student_class_subject:
                section_code = f"{data.Course.CourseCode} {data.Metadata.Year}-{data.Class.Section}"
                teacher = data.ClassSubject.FacultyId if data.ClassSubject.FacultyId else ''

                subject_data = {
                    'SectionCode': section_code,
                    'SubjectName': data.Subject.Name,
                    'SubjectCode': data.Subject.SubjectCode,
                    'Batch': data.Metadata.Batch,
                    'Year': data.Metadata.Year,
                    'Semester': data.Metadata.Semester,
                }

                list_data_student_subject_grade.append(subject_data)

        return jsonify(list_data_student_subject_grade)
    except Exception as e:
        print("ERROR HERE: ", e)
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
        return jsonify(no_list_subject)
    except Exception as e:
        print("ERROR HERE: ", e)
        # Handle the exception here, e.g., log it or return an error response
        return None
        
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

    # print(f"Number of services with status 'pending': {pending_count}")
    # print(f"Number of services with status 'approved': {approved_count}")
    # print(f"Number of services with status 'rejected': {denied_count}")
    # print(total_services)
    
    return all_services_list, total_services, pending_count, approved_count, denied_count

# def get_incomplete_subjects(str_student_id):
#     incomplete_subjects = (
#         db.session.query(StudentClassSubjectGrade, ClassSubject, Subject)
#         .join(ClassSubject, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
#         .join(Subject, Subject.SubjectId == ClassSubject.SubjectId)
#         .filter(StudentClassSubjectGrade.StudentId == str_student_id, StudentClassSubjectGrade.AcademicStatus == 1)
#         .all()
#     )

#     return incomplete_subjects
# def get_incomplete_subjects(str_student_id):
#     try:
#         incomplete_subjects = (
#             db.session.query(StudentClassSubjectGrade, ClassSubject, Subject)
#             .join(ClassSubject, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
#             .join(Subject, Subject.SubjectId == ClassSubject.SubjectId)
#             .filter(StudentClassSubjectGrade.StudentId == str_student_id, StudentClassSubjectGrade.AcademicStatus == 1)
#             .all()
#         )

#         # # Convert each object in the result to a dictionary
#         incomplete_subjects_as_dict = [
#             {
#                 "StudentClassSubjectGrade": {
#                     "StudentClassSubjectGradeId": row.StudentClassSubjectGradeId,
#                     # add other attributes as needed
#                 },
#                 "ClassSubject": {
#                     "ClassSubjectId": row.ClassSubject.ClassSubjectId,
#                     # add other attributes as needed
#                 },
#                 "Subject": {
#                     "SubjectId": row.Subject.SubjectId,
#                     # add other attributes as needed
#                 }
#             }
#             for row in incomplete_subjects
#         ]

#         return jsonify(incomplete_subjects_as_dict)
#     except Exception as e:
#         print("ERROR HERE: ", e)
#         # Handle the exception here, e.g., log it or return an error response
#         return jsonify({"error": "An error occurred while processing the request"}), 500

def get_incomplete_subjects(str_student_id):
    try:
        incomplete_subjects = (
            db.session.query(StudentClassSubjectGrade, ClassSubject, Subject)
            .join(ClassSubject, ClassSubject.ClassSubjectId == StudentClassSubjectGrade.ClassSubjectId)
            .join(Subject, Subject.SubjectId == ClassSubject.SubjectId)
            .filter(
                StudentClassSubjectGrade.StudentId == str_student_id,
                StudentClassSubjectGrade.AcademicStatus == 3
            )
            .all()
        )

        # Create an array to store the incomplete subjects
        list_incomplete_subjects = []

        for row in incomplete_subjects:
            # Append each item to the array
            incomplete_subjects_item = {
                "ClassSubjectId": row.ClassSubject.ClassSubjectId,
                "SubjectId": row.Subject.SubjectId,
                "Grade": row.StudentClassSubjectGrade.Grade
            }
            list_incomplete_subjects.append(incomplete_subjects_item)

        return jsonify(list_incomplete_subjects)
    except Exception as e:
        print("ERROR HERE: ", e)
        # Handle the exception here, e.g., log it or return an error response
        return jsonify({"error": "An error occurred while processing the request"}), 500



#=================================================== to get all the status from different services given=====================================================#
#  def get_all_student_services():
#     addsubject_list = AddSubjects.query.all()
#     changesubjects_list = ChangeSubject.query.all()
#     manual_enrollments_list = ManualEnrollment.query.all()
#     certification_request_list = CertificationRequest.query.all()
#     grade_entry_list = GradeEntry.query.all()
#     cross_enrollment_list = CrossEnrollment.query.all()
#     petition_requests_list = PetitionRequest.query.all()
#     shifting_applications_list = ShiftingApplication.query.all()
#     overload_applications_list = OverloadApplication.query.all()
#     tutorial_requests_list = TutorialRequest.query.all()

#     # Concatenate all lists into one comprehensive list
#     all_services_list = (
#         [subject.to_dict() for subject in addsubject_list] +
#         [subject.to_dict() for subject in changesubjects_list] +
#         [subject.to_dict() for subject in manual_enrollments_list] +
#         [subject.to_dict() for subject in certification_request_list] +
#         [subject.to_dict() for subject in grade_entry_list] +
#         [subject.to_dict() for subject in cross_enrollment_list] +
#         [subject.to_dict() for subject in petition_requests_list] +
#         [subject.to_dict() for subject in shifting_applications_list] +
#         [subject.to_dict() for subject in overload_applications_list] +
#         [subject.to_dict() for subject in tutorial_requests_list]
#     )

#     total_services = len(all_services_list)
#     # Count the number of services with different statuses
#     pending_count = sum(1 for service in all_services_list if service.get('Status') == 'Pending')
#     approved_count = sum(1 for service in all_services_list if service.get('Status') == 'Approved')
#     denied_count = sum(1 for service in all_services_list if service.get('Status') == 'Rejected')

#     print(f"Number of services with status 'pending': {pending_count}")
#     print(f"Number of services with status 'approved': {approved_count}")
#     print(f"Number of services with status 'rejected': {denied_count}")
#     print(f"Total number of services: {total_services}")
    
#     return all_services_list, total_services, pending_count, approved_count, denied_count

#========================================get all te status that can filter based on the course=================================#
# def get_all_student_services(course_id):
#     addsubject_list = AddSubjects.query.filter_by(CourseId=course_id).all()
#     changesubjects_list = ChangeSubject.query.filter_by(CourseId=course_id).all()
#     manual_enrollments_list = ManualEnrollment.query.filter_by(CourseId=course_id).all()
#     certification_request_list = CertificationRequest.query.filter_by(CourseId=course_id).all()
#     grade_entry_list = GradeEntry.query.filter_by(CourseId=course_id).all()
#     cross_enrollment_list = CrossEnrollment.query.filter_by(CourseId=course_id).all()
#     petition_requests_list = PetitionRequest.query.filter_by(CourseId=course_id).all()
#     shifting_applications_list = ShiftingApplication.query.filter_by(CourseId=course_id).all()
#     overload_applications_list = OverloadApplication.query.filter_by(CourseId=course_id).all()
#     tutorial_requests_list = TutorialRequest.query.filter_by(CourseId=course_id).all()

#     # Concatenate all lists into one comprehensive list
#     all_services_list = (
#         [subject.to_dict() for subject in addsubject_list] +
#         [subject.to_dict() for subject in changesubjects_list] +
#         [subject.to_dict() for subject in manual_enrollments_list] +
#         [subject.to_dict() for subject in certification_request_list] +
#         [subject.to_dict() for subject in grade_entry_list] +
#         [subject.to_dict() for subject in cross_enrollment_list] +
#         [subject.to_dict() for subject in petition_requests_list] +
#         [subject.to_dict() for subject in shifting_applications_list] +
#         [subject.to_dict() for subject in overload_applications_list] +
#         [subject.to_dict() for subject in tutorial_requests_list]
#     )

#     total_services = len(all_services_list)
#     # Count the number of services with different statuses
#     pending_count = sum(1 for service in all_services_list if service.get('Status') == 'Pending')
#     approved_count = sum(1 for service in all_services_list if service.get('Status') == 'Approved')
#     denied_count = sum(1 for service in all_services_list if service.get('Status') == 'Rejected')

#     print(f"Number of services with status 'pending': {pending_count}")
#     print(f"Number of services with status 'approved': {approved_count}")
#     print(f"Number of services with status 'rejected': {denied_count}")
#     print(f"Total number of services: {total_services}")
    
#     return all_services_list, total_services, pending_count, approved_count, denied_count
#===============================================================================================================

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
    
def get_subject_name_by_code(subject_code):
    subject = Subject.query.filter_by(SubjectCode=subject_code).first()
    print(subject)
    return subject.Name if subject else None


# def haymeannouncement():
#     try:
#         uploader_user = AliasedReturnsRows(APMSUser)

#         # Query to retrieve data from the Announcements table
#         announcements_data = db.session.query(
#             Announcements.id,
#             Announcements.created_at,
#             Announcements.updated_at,
#             Announcements.deleted_at,
#             Announcements.title,
#             Announcements.content,
#             Announcements.post_type,
#             Announcements.img_link,
#             uploader_user.username.label('uploader_username')  # Assuming 'username' is a field in APMSUser
#         ).join(
#             uploader_user,
#             Announcements.uploader_id == uploader_user.id
#         ).all()

#         # Printing the result (you can use this data in your HTML template)
#         for announcement in announcements_data:
#             print(announcement)
    
#     except Exception as e:
#         print("ERROR HERE: ", e)
#         return None
    


def get_student_history_services(student_id):

    services_data = {}

    # Fetch AddSubjects based on the StudentId foreign key
    addsubjects = AddSubjects.query.filter_by(StudentId=student_id).all()
    services_data['addsubjects_list'] = [subject.to_dict() for subject in addsubjects]

    # Fetch ChangeOfSubjects based on the StudentId foreign key
    changesubjects = ChangeSubject.query.filter_by(StudentId=student_id).all()
    services_data['changesubjects_list'] = [subject.to_dict() for subject in changesubjects]

    # Fetch ManualEnrollment based on the StudentId foreign key
    manual_enrollments = ManualEnrollment.query.filter_by(StudentId=student_id).all()
    services_data['manual_enrollments_list'] = [subject.to_dict() for subject in manual_enrollments]

     # Fetch CertificationRequest based on the StudentId foreign key
    certification_request = CertificationRequest.query.filter_by(StudentId=student_id).all()
    services_data['certification_request_list'] = [subject.to_dict() for subject in certification_request]

        # Fetch GradeEntry based on the StudentId foreign key
    grade_entry = GradeEntry.query.filter_by(StudentId=student_id).all()
    services_data['grade_entry_list'] = [subject.to_dict() for subject in grade_entry]

        # Fetch CrossEnrollment based on the StudentId foreign key
    cross_enrollment = CrossEnrollment.query.filter_by(StudentId=student_id).all()
    services_data['cross_enrollment_list'] = [subject.to_dict() for subject in cross_enrollment]

        # Fetch PetitionRequest based on the StudentId foreign key
    petition_requests = PetitionRequest.query.filter_by(StudentId=student_id).all()
    services_data['petition_requests_list'] = [subject.to_dict() for subject in petition_requests]

        # Fetch ShiftingApplication based on the StudentId foreign key
    shifting_applications = ShiftingApplication.query.filter_by(StudentId=student_id).all()
    services_data['shifting_applications_list'] = [subject.to_dict() for subject in shifting_applications]

        # Fetch OverloadApplication based on the StudentId foreign key
    overload_applications = OverloadApplication.query.filter_by(StudentId=student_id).all()
    services_data['overload_applicationss_list'] = [subject.to_dict() for subject in overload_applications]

        # Fetch TutorialRequest based on the StudentId foreign key
    tutorial_requests = TutorialRequest.query.filter_by(StudentId=student_id).all()
    services_data['tutorial_requests_list'] = [subject.to_dict() for subject in tutorial_requests]

    service_counts = {
        'Add Subjects': len(services_data.get('addsubjects_list', [])),
        'Change of Subjects': len(services_data.get('changesubjects_list', [])),
        'Manual Enrollments': len(services_data.get('manual_enrollments_list', [])),
        'Certification Requests': len(services_data.get('certification_request_list', [])),
        'Grade Entries': len(services_data.get('grade_entry_list', [])),
        'Cross Enrollments': len(services_data.get('cross_enrollment_list', [])),
        'Petition Requests': len(services_data.get('petition_requests_list', [])),
        'Shifting Applications': len(services_data.get('shifting_applications_list', [])),
        'Overload Applications': len(services_data.get('overload_applicationss_list', [])),
        'Tutorial Requests': len(services_data.get('tutorial_requests_list', []))
    }

    return services_data