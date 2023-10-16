from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Student(db.Model, UserMixin):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)  
    email = db.Column(db.String(50), unique=True, nullable=False) 
    address = db.Column(db.String(50), nullable=True) 
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.Integer)  
    dateofBirth = db.Column(db.Date)  
    placeofBirth = db.Column(db.String(50), nullable=True)
    mobileNumber = db.Column(db.String(11))
    userImg = db.Column(db.String, nullable=False) 

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
        }
        
    def get_id(self):
        return str(self.id)  # Convert to string to ensure compatibility

class Payment(db.Model, UserMixin):
    __tablename__ = 'payments'

    paymentID = db.Column(db.Integer, primary_key=True)
    modeofPayment = db.Column(db.String(50))
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
            return str(self.paymentID)  # Convert to string to ensure compatibility

class Service(db.Model, UserMixin):
    __tablename__ = 'services'

    serviceID = db.Column(db.Integer, primary_key=True)
    typeofServices = db.Column(db.String(50))
    status = db.Column(db.String(50)) #Modifythelength
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
    name = db.Column(db.String(50))
    emailAddress = db.Column(db.String(50))
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
    name = db.Column(db.String(50))
    emailAddress = db.Column(db.String(50))
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
    announcementType = db.Column(db.String(50))  # e.g., 'General', 'Event', etc.
    announcementDetails = db.Column(db.TEXT)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    stud_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    fac_id = db.Column(db.Integer, db.ForeignKey('faculties.facultyID'), nullable=False)


    def to_dict(self):
        return {
            'announcementID': self.announcementID,
       #     'id': self.id,
       #     'facultyID': self.facultyID,
            'announcementType': self.announcementType,
            'announcementDetails': self.announcementDetails,
            'date': str(self.date),  # Convert Date to string for JSON serialization
            'time': str(self.time),  # Convert Time to string for JSON serialization
            #            'courseCode': self.courseCode,
            #             'sectionNumber': self.sectionNumber,
            #                'professorName': self.professorName,
            #                    'roomNo': self.roomNo,
            #                        'startDate': str(self.startDate),   #Convert Start Date and End Date to strings for JSON Serialization
            #                        'startTime': str(self.startTime),   # Convert Start Time to string for JSON serialization
            #                     'startDate': str(self.startDate),   # Convert Start Date to string for JSON Serialization
            #                     'startTime': str(self.startTime),   #Convert StartTime and EndTime to strings so that they can be serialized in json format
            #                        'dayOfWeek': self.dayOfWeek,
            #                            'startTime': self.startTime,
            #                                'endTime': self.endTime,
            'user_id': self.user_id
        }
    # **How to call it
    # announcement = Announcement.query.get(some_announcement_id)
    # announcement_data = announcement.to_dict()
    def get_announcementID(self):
        return str(self.announcementID)  # Convert to string to ensure compatibility


class Faculty(db.Model, UserMixin):
    __tablename__ = 'faculties'

    facultyID = db.Column(db.Integer, primary_key=True)  # UserID
    facultyNumber = db.Column(db.String(30), unique=True, nullable=False) #Faculty_Number
    userType = db.Column(db.String(50))  # e.g., 'Admin', 'Professor', etc.
    name = db.Column(db.String(50), nullable=False)  # Name
    email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    address = db.Column(db.String(255))  # You can use String or TEXT depending on the length
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    dateofBirth = db.Column(db.Date)  # dateofBirth
    placeofBirth = db.Column(db.String(50))  # placeofBirth
    mobile_number = db.Column(db.String(20))  # MobileNumber
    userImg = db.Column(db.String(255))  # Modify the length as needed
    is_active = db.Column(db.Boolean, default=True)

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
    name = db.Column(db.String(50), nullable=False)  # Name
    email = db.Column(db.String(50), unique=True, nullable=False)  # Email
    password = db.Column(db.String(128), nullable=False)  # Password
    gender = db.Column(db.Integer)  # Gender
    dateofBirth = db.Column(db.Date)  # dateofBirth
    placeofBirth = db.Column(db.String(50))  # placeofBirth
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
            create_sample_data()
        
#=====================================================================================================
# INSERTING DATA
def create_sample_data():
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
            'userType': 'Professor',
            'name': 'Faculty 1',
            'email': 'faculty1@example.com',
            'address': '100 Galaxy st. City 2',
            'password': generate_password_hash('password1'),
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
            'userType': 'Professor',
            'name': 'Faculty 2',
            'email': 'faculty2@example.com',
            'address': '101 Mercury st. City 3',
            'password': generate_password_hash('password2'),
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

