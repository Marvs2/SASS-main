from functools import wraps
from flask import redirect, url_for, flash

from functools import wraps
from flask import redirect, url_for, session, render_template

def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_role' in session and session['user_role'] == 'student':
            return fn(*args, **kwargs)
        else:
            flash('Access Denied', category='danger')
            return redirect(url_for('studentLogin'))
    return wrapper

def faculty_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_role' in session and session['user_role'] == 'faculty':
            return fn(*args, **kwargs)
        else:
            flash('Access denied', category='danger')
            return redirect(url_for('faculty_portal'))
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_role' in session and session['user_role'] == 'admin':
            return fn(*args, **kwargs)
        else:
            flash('Access denied', 'danger')
            return redirect(url_for('home'))
    return wrapper

def prevent_authenticated(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_role' in session:
            role = session['user_role']
            return redirect(url_for(f"{role}_dashboard"))
        return fn(*args, **kwargs)
    return wrapper

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = session.get('user_role')
            if user_role == required_role:
                return func(*args, **kwargs)
            else:
                flash('Access Denied', category='danger')
                return redirect(url_for('studentLogin'))
        return wrapper
    return decorator

    

# Dictionary mapping facultyId to their respective HTML menu content
# faculty_menus = {
#     10017: """
#     <ul class="side-dropdown">
#         <li><a href="{{ url_for('facultyoverload') }}">Overload of Subjects</a></li>
#         <li><a href="{{ url_for('facultypetition') }}">Online Petition of Subjects</a></li>
#         <li><a href="{{ url_for('facultyshifting') }}">Application for Shifting</a></li>
#         <li><a href="{{ url_for('facultytutorial') }}">Online Request for Tutorial</a></li>
#     </ul>
#     """,
#     10018: """
#     <ul class="side-dropdown">
#         <li><a href="{{ url_for('facultyadding') }}">Adding of Subjects</a></li>
#         <li><a href="{{ url_for('facultychange') }}">Change of Schedule/Subjects</a></li>
#         <li><a href="{{ url_for('facultycrossenrollment') }}">Cross-Enrollment</a></li>
#     </ul>
#     """,
#     1: """
#     <ul class="side-dropdown">
#         <li><a href="{{ url_for('facultycorrection') }}">Correction of Grade Entry</a></li>
#         <li><a href="{{ url_for('facultyenrollment') }}">Manual Enrollment</a></li>
#         <li><a href="{{ url_for('facultycertification') }}">Request for Certification</a></li>
#     </ul>
#     """
# }

# def faculty_menu_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         facultyId = session.get('facultyId')
#         faculty_menu = faculty_menus.get(facultyId, "")  # Default to empty string if facultyId not found
#         return fn(faculty_menu=faculty_menu, *args, **kwargs)
#     return wrapper
# def faculty_menu_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         facultyId = session.get('facultyId')
#         if facultyId in faculty_menus:
#             faculty_menu = faculty_menus[facultyId]
#         else:
#             faculty_menu = ""  # Fallback if facultyId not found
#         return fn(*args, **kwargs)
#     return wrapper
# def student_required(route_function):
#     @studentlogin_required
#     @wraps(route_function)
#     def wrapper(*args, **kwargs):
#         if current_user.is_authenticated and isinstance(current_user, Student):
#             return route_function(*args, **kwargs)
#         else:
#             abort(401)  # Unauthorized
#           return render_template("student/login.html")
#     return wrapper
