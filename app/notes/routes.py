from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import Note
from app.notes.forms import NoteForm
from app.notes import bp

@bp.route('/notes')
@login_required
def index():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    form = NoteForm()  # Create an empty form for CSRF token
    return render_template('notes/index.html', notes=notes, form=form)

@bp.route('/notes/new', methods=['GET', 'POST'])
@login_required
def new_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        flash('Note created successfully!', 'success')
        return redirect(url_for('notes.index'))
    return render_template('notes/create.html', form=form)

@bp.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note.', 'danger')
        return redirect(url_for('notes.index'))
    
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes.index'))
    
    if request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('notes/edit.html', form=form, note=note)

@bp.route('/notes/<int:id>/delete', methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('You do not have permission to delete this note.', 'danger')
        return redirect(url_for('notes.index'))
    
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('notes.index'))
