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


def get_all_services():
    addsubject_list = AddSubjects.query.all()
    changesubjects_list = ChangeSubject.query.all()
    manual_enrollments_list = ManualEnrollment.query.all()
    certification_request_list = CertificationRequest.query.all()
    grade_entry_list = GradeEntry.query.all()
    cross_enrollment_list = CrossEnrollment.query.all()
    petition_requests_list = PetitionRequest.query.all()
    shifting_applications_list = ShiftingApplication.query.all()
    overload_applications_list = OverloadApplication.query.all()
    tutorial_requests_list = TutorialRequest.query.all()

    all_services_list = {}
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
    # Count the number of services with different statuses
    pending_count = sum(1 for service in all_services_list if service.get('Status') == 'pending')
    approved_count = sum(1 for service in all_services_list if service.get('Status') == 'Approved')
    denied_count = sum(1 for service in all_services_list if service.get('Status') == 'Rejected')

    return all_services_list, total_services, pending_count, approved_count, denied_count



def get_all_services_counts():
    # Define the models
    models = [AddSubjects, ChangeSubject, ManualEnrollment, CertificationRequest, GradeEntry, CrossEnrollment, PetitionRequest, ShiftingApplication, OverloadApplication, TutorialRequest]

    # Define the statuses you want to filter
    statuses_to_filter = ['pending', 'approved', 'rejected']

    # List to store counts for each status
    status_counts_list = []

    # Loop through each model and count the statuses
    for model in models:
        model_counts = {}
        # print(f"{model.__name__} Status Counts:")
        for status in statuses_to_filter:
            # Assuming 'Status' is the column name in the model storing the service status
            count = model.query.filter(func.lower(model.Status) == status).count()
            model_counts[status] = count
            # print(f"  {status.capitalize()}: {count}")
        status_counts_list.append({model.__name__: model_counts})

    return status_counts_list



    # models = [AddSubjects, ChangeSubject, ManualEnrollment, CertificationRequest, GradeEntry, CrossEnrollment, PetitionRequest, ShiftingApplication, OverloadApplication, TutorialRequest]

    # # Define the statuses you want to filter
    # statuses_to_filter = ['pending', 'approved', 'denied']

    # # Dictionary to store counts for each status
    # status_counts = {status: 0 for status in statuses_to_filter}

    # # Loop through each model and count the statuses
    # for model in models:
    #     print(f"{model.__name__} Status Counts:")
    #     for status in statuses_to_filter:
    #         # Assuming 'Status' is the column name in the model storing the service status
    #         count = model.query.filter(func.lower(model.Status) == status).count()
    #         print(f"{status.capitalize()}: {count}")
    #     print()





# def get_all_services():
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
    
#     # Convert non-serializable data to serializable format
#     for service in all_services_list:
#         # Example: Convert bytes to string
#         service['some_bytes_field'] = service['some_bytes_field'].decode('utf-8') if 'some_bytes_field' in service else None

#     total_services = len(all_services_list)
#     # Count the number of services with different statuses
#     pending_count = sum(1 for service in all_services_list if service.get('Status') == 'pending')
#     approved_count = sum(1 for service in all_services_list if service.get('Status') == 'Approved')
#     denied_count = sum(1 for service in all_services_list if service.get('Status') == 'Rejected')

#     return jsonify(all_services_list=all_services_list,
#                    total_services=total_services,
#                    pending_count=pending_count,
#                    approved_count=approved_count,
#                    denied_count=denied_count)

# def get_allstudent_services_by_course(course_code):
#     # Fetch all services filtered by CourseCode
#     addsubject_list = AddSubjects.query.filter_by(CourseCode=course_code).all()
#     changesubjects_list = ChangeSubject.query.filter_by(CourseCode=course_code).all()
#     manual_enrollments_list = ManualEnrollment.query.filter_by(CourseCode=course_code).all()
#     certification_request_list = CertificationRequest.query.filter_by(CourseCode=course_code).all()
#     grade_entry_list = GradeEntry.query.filter_by(CourseCode=course_code).all()
#     cross_enrollment_list = CrossEnrollment.query.filter_by(CourseCode=course_code).all()
#     petition_requests_list = PetitionRequest.query.filter_by(CourseCode=course_code).all()
#     shifting_applications_list = ShiftingApplication.query.filter_by(CourseCode=course_code).all()
#     overload_applications_list = OverloadApplication.query.filter_by(CourseCode=course_code).all()
#     tutorial_requests_list = TutorialRequest.query.filter_by(CourseCode=course_code).all()

#     # Grouping data based on different criteria
#     services_by_category = {
#         "AddSubjects": [subject.to_dict() for subject in addsubject_list],
#         "ChangeSubjects": [subject.to_dict() for subject in changesubjects_list],
#         "ManualEnrollments": [subject.to_dict() for subject in manual_enrollments_list],
#         "CertificationRequests": [subject.to_dict() for subject in certification_request_list],
#         "GradeEntries": [subject.to_dict() for subject in grade_entry_list],
#         "CrossEnrollments": [subject.to_dict() for subject in cross_enrollment_list],
#         "PetitionRequests": [subject.to_dict() for subject in petition_requests_list],
#         "ShiftingApplications": [subject.to_dict() for subject in shifting_applications_list],
#         "OverloadApplications": [subject.to_dict() for subject in overload_applications_list],
#         "TutorialRequests": [subject.to_dict() for subject in tutorial_requests_list]
#     }
#     # Calculate the total services and their statuses
#     total_services = sum(len(services) for services in services_by_category.values())
#     pending_count = sum(1 for category in services_by_category.values() for service in category if service.get('Status') == 'Pending')
#     approved_count = sum(1 for category in services_by_category.values() for service in category if service.get('Status') == 'Approved')
#     denied_count = sum(1 for category in services_by_category.values() for service in category if service.get('Status') == 'Rejected')

#     # Print statements for debugging (can be removed in production)
#     print(f"Number of services with status 'pending': {pending_count}")
#     print(f"Number of services with status 'approved': {approved_count}")
#     print(f"Number of services with status 'rejected': {denied_count}")
#     print(f"Total number of services: {total_services}")
#     print(services_by_category)
    
#     return services_by_category, total_services, pending_count, approved_count, denied_count
