# NOTES: Any data here is a dummy only for development purposes

from werkzeug.security import generate_password_hash

faculty_data = [
    {
        'FacultyType': 'Professor',
        'Rank': 'Associate Professor',
        'Units': 3.5,
        'Name': 'John Doe',
        'FirstName': 'John',
        'LastName': 'Doe',
        'MiddleName': 'Alexander',
        'MiddleInitial': 'A',
        'NameExtension': 'Jr.',
        'BirthDate': '1980-05-15',
        'DateHired': '2010-08-20',
        'Degree': 'Ph.D. in Computer Science',
        'Remarks': 'Experienced researcher',
        'FacultyCode': 1001,
        'Honorific': 'Dr.',
        'Age': 42,
        'Email': 'john.doe@example.com',
        'ResidentialAddress': '123 Main Street, Cityville',
        'MobileNumber': '555-1234',
        'Gender': 1,  # 1 for Male
        'IsActive': True,
        'Password': generate_password_hash('Faculty123')
    },
    {
        'FacultyType': 'Instructor',
        'Rank': 'Assistant Professor',
        'Units': 2.0,
        'Name': 'Jane Smith',
        'FirstName': 'Jane',
        'LastName': 'Smith',
        'BirthDate': '1985-08-10',
        'DateHired': '2015-03-12',
        'Degree': 'M.Sc. in Chemistry',
        'FacultyCode': 1002,
        'Age': 37,
        'Email': 'jane.smith@example.com',
        'MobileNumber': '555-5678',
        'Gender': 2,  # 2 for Female
        'IsActive': True,
        'Password': generate_password_hash('Faculty123')
    },
    {
        'FacultyType': 'Lecturer',
        'Rank': 'Full Professor',
        'Units': 4.0,
        'Name': 'Robert Johnson',
        'FirstName': 'Robert',
        'LastName': 'Johnson',
        'BirthDate': '1990-01-05',
        'DateHired': '2020-06-08',
        'FacultyCode': 1003,
        'Age': 31,
        'Email': 'robert.johnson@example.com',
        'MobileNumber': '555-8765',
        'Gender': 1,  # 1 for Male
        'IsActive': True,
        'Password': generate_password_hash('Faculty123')
    },
    {
        'FacultyType': 'Professor',
        'Rank': 'Full Professor',
        'Units': 4.0,
        'Name': 'Emily White',
        'FirstName': 'Emily',
        'LastName': 'White',
        'BirthDate': '1975-03-25',
        'DateHired': '2005-01-01',
        'Degree': 'Ph.D. in Physics',
        'FacultyCode': 1004,
        'Age': 47,
        'Email': 'emily.white@example.com',
        'MobileNumber': '555-4321',
        'Gender': 2,  # 2 for Female
        'IsActive': True,
        'Password': generate_password_hash('Faculty123')
    },
    {
        'FacultyType': 'Instructor',
        'Rank': 'Lecturer',
        'Units': 1.5,
        'Name': 'Michael Turner',
        'FirstName': 'Michael',
        'LastName': 'Turner',
        'BirthDate': '1988-07-18',
        'DateHired': '2018-02-03',
        'Degree': 'M.A. in English',
        'FacultyCode': 1005,
        'Age': 33,
        'Email': 'michael.turner@example.com',
        'MobileNumber': '555-9876',
        'Gender': 1,  # 1 for Male
        'IsActive': True,
        'Password': generate_password_hash('Faculty123')
    },
]

