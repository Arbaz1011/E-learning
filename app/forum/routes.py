from flask import abort, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forum import bp
from app.models import ForumTopic, ForumPost, Course
from app.forum.forms import TopicForm, PostForm

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    topics = ForumTopic.query.order_by(ForumTopic.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('forum/index.html',
                         title='Discussion Forum',
                         topics=topics)

@bp.route('/course/<int:course_id>/topics')
@login_required
def course_topics(course_id):
    course = Course.query.get_or_404(course_id)
    page = request.args.get('page', 1, type=int)
    topics = ForumTopic.query.filter_by(course_id=course_id)\
        .order_by(ForumTopic.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    return render_template('forum/course_topics.html',
                         title=f'Discussions - {course.title}',
                         course=course,
                         topics=topics)

@bp.route('/topic/new/<int:course_id>', methods=['GET', 'POST'])
@login_required
def new_topic(course_id):
    course = Course.query.get_or_404(course_id)
    form = TopicForm()
    if form.validate_on_submit():
        topic = ForumTopic(
            title=form.title.data,
            course_id=course.id
        )
        post = ForumPost(
            content=form.content.data,
            author=current_user
        )
        topic.posts.append(post)
        db.session.add(topic)
        db.session.commit()
        flash('Your topic has been created!', 'success')
        return redirect(url_for('forum.topic', topic_id=topic.id))
    return render_template('forum/new_topic.html',
                         title='New Discussion Topic',
                         form=form,
                         course=course)

@bp.route('/topic/<int:topic_id>')
@login_required
def topic(topic_id):
    topic = ForumTopic.query.get_or_404(topic_id)
    page = request.args.get('page', 1, type=int)
    posts = ForumPost.query.filter_by(topic_id=topic_id)\
        .order_by(ForumPost.created_at.asc())\
        .paginate(page=page, per_page=10, error_out=False)
    form = PostForm()
    return render_template('forum/topic.html',
                         title=topic.title,
                         topic=topic,
                         posts=posts,
                         form=form)

@bp.route('/topic/<int:topic_id>/reply', methods=['POST'])
@login_required
def reply(topic_id):
    topic = ForumTopic.query.get_or_404(topic_id)
    form = PostForm()
    if form.validate_on_submit():
        post = ForumPost(
            content=form.content.data,
            author=current_user,
            topic=topic
        )
        db.session.add(post)
        db.session.commit()
        flash('Your reply has been posted!', 'success')
    return redirect(url_for('forum.topic', topic_id=topic_id, _anchor=f'post-{post.id}'))

@bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('forum.topic', topic_id=post.topic_id, _anchor=f'post-{post.id}'))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('forum/edit_post.html',
                         title='Edit Post',
                         form=form,
                         post=post)

@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    if post.author != current_user and current_user.role != 'admin':
        abort(403)
    topic_id = post.topic_id
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('forum.topic', topic_id=topic_id))

# Lazy import
def load_forum_models():
    from app.models import ForumTopic, ForumPost, Course
    return ForumTopic, ForumPost, Course

@login_required
def show_forum():
    ForumTopic, ForumPost, Course = load_forum_models()
    # Logic to show forum topics and posts
    topics = ForumTopic.query.all()
    return render_template('forum.html', topics=topics)
