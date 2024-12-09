from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Remove the problematic import here
# from app.models import ForumTopic  # This import is causing the circular import

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class ForumTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ForumTopic {self.title}>'
    
class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    forum_topic_id = db.Column(db.Integer, db.ForeignKey('forum_topic.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    forum_topic = db.relationship('ForumTopic', backref=db.backref('posts', lazy=True))
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<ForumPost {self.id} by {self.user.username}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    enrolled_courses = db.relationship('Enrollment', back_populates='student')
    created_courses = db.relationship('Course', back_populates='instructor')
    notifications = db.relationship('Notification', back_populates='user')
    notes = db.relationship('Note', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_published = db.Column(db.Boolean, default=False)
    pdf_file = db.Column(db.String(255))  # Store the path to the PDF file
    
    # Relationships
    instructor = db.relationship('User', back_populates='created_courses')
    lessons = db.relationship('Lesson', back_populates='course', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', back_populates='course')

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    order = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', back_populates='lessons')
    progress = db.relationship('LessonProgress', back_populates='lesson')

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    student = db.relationship('User', back_populates='enrolled_courses')
    course = db.relationship('Course', back_populates='enrollments')
    progress = db.relationship('LessonProgress', back_populates='enrollment')

class LessonProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    enrollment = db.relationship('Enrollment', back_populates='progress')
    lesson = db.relationship('Lesson', back_populates='progress')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', back_populates='notifications')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='notes')

