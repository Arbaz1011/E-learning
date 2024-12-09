from flask import render_template, redirect, url_for
from app.main import bp
from app.models import Course, User
from flask_login import current_user

@bp.route('/')
@bp.route('/index')
def index():
    featured_courses = Course.query.filter_by(is_published=True).order_by(Course.created_at.desc()).limit(6).all()
    total_users = User.query.count()
    total_courses = Course.query.filter_by(is_published=True).count()
    
    return render_template('main/index.html', 
                         title='Home',
                         featured_courses=featured_courses,
                         total_users=total_users,
                         total_courses=total_courses)

@bp.route('/about')
def about():
    return render_template('main/about.html', title='About Us')

@bp.route('/contact')
def contact():
    return render_template('main/contact.html', title='Contact Us')

def some_function():
    from app.models import ForumTopic  # Import locally inside the function
