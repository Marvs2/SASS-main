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
                return render_template('404.html'), 404
        return wrapper
    return decorator

# def faculty_required(route_function):
#     @login_required
#     @wraps(route_function)
#     def wrapper(*args, **kwargs):
#         if current_user.is_authenticated and isinstance(current_user, Faculty):
#             return route_function(*args, **kwargs)
#         else:
#             abort(401)  # Unauthorized
#     return wrapper
