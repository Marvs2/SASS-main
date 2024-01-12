from werkzeug.security import generate_password_hash


system_admin_data = [
    {
        "SysAdminNumber": "2020-00001-SA-0",
        "FacultyId":26,
        "Name": "Floyd Dela Cruz",
        "Email": "floyd@gmail.com",
        "Password": generate_password_hash("Admin123"),
        "Gender": 2,
        "DateOfBirth": "1995-03-10",
        "PlaceOfBirth": "Quezon City",
        "ResidentialAddress": "Quezon City",
        "MobileNumber": "09613523624",
        "IsActive": True

    },
    {
        "SysAdminNumber": "2020-00002-SA-0",
        "FacultyId":26,
        "Name": "Floyd Mayweahter",
        "Email": "systemadmin@gmail.com",
        "Password": generate_password_hash("Admin123"),
        "Gender": 1,
        "DateOfBirth": "1980-09-18",
        "PlaceOfBirth": "Quezon City",
        "ResidentialAddress": "Quezon City",
        "MobileNumber": "09612363261",
        "IsActive": True

    },
    # Add more admin data as needed
]
