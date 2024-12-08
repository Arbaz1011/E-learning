from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.models import User, Course, Enrollment
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_courses = Course.query.order_by(Course.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments,
                         recent_users=recent_users,
                         recent_courses=recent_courses)

@bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html',
                         title='Manage Users',
                         users=users)

@bp.route('/user/<int:user_id>/toggle-role', methods=['POST'])
@login_required
@admin_required
def toggle_role(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot change your own role.', 'danger')
    else:
        if user.role == 'student':
            user.role = 'instructor'
            flash(f'{user.username} is now an instructor.', 'success')
        elif user.role == 'instructor':
            user.role = 'student'
            flash(f'{user.username} is now a student.', 'success')
        db.session.commit()
    
    return redirect(url_for('admin.users'))

@bp.route('/user/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_status(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot change your own status.', 'danger')
    else:
        user.is_active = not user.is_active
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.username} has been {status}.', 'success')
        db.session.commit()
    
    return redirect(url_for('admin.users'))

@bp.route('/courses')
@login_required
@admin_required
def courses():
    page = request.args.get('page', 1, type=int)
    courses = Course.query.order_by(Course.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/courses.html',
                         title='Manage Courses',
                         courses=courses)

@bp.route('/course/<int:course_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_course_status(course_id):
    course = Course.query.get_or_404(course_id)
    course.is_published = not course.is_published
    status = 'published' if course.is_published else 'unpublished'
    flash(f'Course "{course.title}" has been {status}.', 'success')
    db.session.commit()
    
    return redirect(url_for('admin.courses'))

@bp.route('/statistics')
@login_required
@admin_required
def statistics():
    # User statistics
    total_users = User.query.count()
    student_count = User.query.filter_by(role='student').count()
    instructor_count = User.query.filter_by(role='instructor').count()
    
    # Course statistics
    total_courses = Course.query.count()
    published_courses = Course.query.filter_by(is_published=True).count()
    total_enrollments = Enrollment.query.count()
    
    # Calculate average enrollments per course
    avg_enrollments = total_enrollments / total_courses if total_courses > 0 else 0
    
    return render_template('admin/statistics.html',
                         title='Platform Statistics',
                         total_users=total_users,
                         student_count=student_count,
                         instructor_count=instructor_count,
                         total_courses=total_courses,
                         published_courses=published_courses,
                         total_enrollments=total_enrollments,
                         avg_enrollments=avg_enrollments)
