from functools import wraps
from flask import redirect, url_for, flash

from functools import wraps
from flask import redirect, url_for, flash, session

def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_role' in session and session['user_role'] == 'student':
            return fn(*args, **kwargs)
        else:
            flash('', 'danger')
            return redirect(url_for('home'))
    return wrapper

def faculty_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_role' in session and session['user_role'] == 'faculty':
            return fn(*args, **kwargs)
        else:
            flash('Access denied', 'danger')
            return redirect(url_for('home'))
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
            return redirect(url_for(f"{role}_home"))
        return fn(*args, **kwargs)
    return wrapper

# def faculty_required(route_function):
#     @login_required
#     @wraps(route_function)
#     def wrapper(*args, **kwargs):
#         if current_user.is_authenticated and isinstance(current_user, Faculty):
#             return route_function(*args, **kwargs)
#         else:
#             abort(401)  # Unauthorized
#     return wrapper
