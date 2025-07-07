from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, send_file
from flask_login import login_required, current_user
from datetime import datetime, date
import os
import io
from app import db
from app.models import Student, Grade, DisciplinaryNote, GeneralNote, Scholarship
from app.forms import StudentForm, GradeForm, DisciplinaryNoteForm, GeneralNoteForm, ScholarshipForm, ImportForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    total_students = Student.query.count()
    total_grades = Grade.query.count()
    total_scholarships = Scholarship.query.count()
    active_scholarships = Scholarship.query.filter_by(status='active').count()
    
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    recent_grades = Grade.query.order_by(Grade.date_recorded.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_students=total_students,
                         total_grades=total_grades,
                         total_scholarships=total_scholarships,
                         active_scholarships=active_scholarships,
                         recent_students=recent_students,
                         recent_grades=recent_grades)

@bp.route('/students')
@login_required
def students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    program_filter = request.args.get('program', '', type=str)
    
    query = Student.query
    
    if search:
        query = query.filter(
            (Student.full_name.contains(search)) |
            (Student.student_id.contains(search)) |
            (Student.email.contains(search))
        )
    
    if program_filter:
        query = query.filter(Student.program == program_filter)
    
    students = query.order_by(Student.full_name).paginate(
        page=page, per_page=10, error_out=False
    )
    
    programs = db.session.query(Student.program).distinct().filter(Student.program.isnot(None)).all()
    programs = [p[0] for p in programs if p[0]]
    
    return render_template('students.html', students=students, search=search, 
                         programs=programs, program_filter=program_filter)

@bp.route('/student/<int:id>')
@login_required
def student_detail(id):
    student = Student.query.get_or_404(id)
    grades = Grade.query.filter_by(student_id=id).order_by(Grade.date_recorded.desc()).all()
    disciplinary_notes = DisciplinaryNote.query.filter_by(student_id=id).order_by(DisciplinaryNote.date_created.desc()).all()
    general_notes = GeneralNote.query.filter_by(student_id=id).order_by(GeneralNote.date_created.desc()).all()
    scholarships = Scholarship.query.filter_by(student_id=id).order_by(Scholarship.start_date.desc()).all()
    
    return render_template('student_detail.html', student=student, grades=grades,
                         disciplinary_notes=disciplinary_notes, general_notes=general_notes,
                         scholarships=scholarships)

@bp.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        # Check if student ID already exists
        existing_student = Student.query.filter_by(student_id=form.student_id.data).first()
        if existing_student:
            flash('Student ID already exists!', 'error')
            return render_template('student_form.html', form=form, title='Add Student')
        
        student = Student(
            student_id=form.student_id.data,
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            year_of_study=form.year_of_study.data,
            program=form.program.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('main.student_detail', id=student.id))
    
    return render_template('student_form.html', form=form, title='Add Student')

@bp.route('/student/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    
    if form.validate_on_submit():
        # Check if student ID already exists (excluding current student)
        existing_student = Student.query.filter(
            Student.student_id == form.student_id.data,
            Student.id != id
        ).first()
        if existing_student:
            flash('Student ID already exists!', 'error')
            return render_template('student_form.html', form=form, title='Edit Student', student=student)
        
        student.student_id = form.student_id.data
        student.full_name = form.full_name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.date_of_birth = form.date_of_birth.data
        student.gender = form.gender.data
        student.year_of_study = form.year_of_study.data
        student.program = form.program.data
        student.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('main.student_detail', id=student.id))
    
    return render_template('student_form.html', form=form, title='Edit Student', student=student)

@bp.route('/student/<int:id>/delete', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('main.students'))

# Grade routes
@bp.route('/student/<int:student_id>/grade/add', methods=['GET', 'POST'])
@login_required
def add_grade(student_id):
    student = Student.query.get_or_404(student_id)
    form = GradeForm()
    
    if form.validate_on_submit():
        grade = Grade(
            student_id=student_id,
            subject_name=form.subject_name.data,
            grade=form.grade.data,
            semester=form.semester.data,
            teacher_name=form.teacher_name.data
        )
        db.session.add(grade)
        db.session.commit()
        flash('Grade added successfully!', 'success')
        return redirect(url_for('main.student_detail', id=student_id))
    
    return render_template('grade_form.html', form=form, student=student, title='Add Grade')

@bp.route('/grade/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_grade(id):
    grade = Grade.query.get_or_404(id)
    form = GradeForm(obj=grade)
    
    if form.validate_on_submit():
        grade.subject_name = form.subject_name.data
        grade.grade = form.grade.data
        grade.semester = form.semester.data
        grade.teacher_name = form.teacher_name.data
        
        db.session.commit()
        flash('Grade updated successfully!', 'success')
        return redirect(url_for('main.student_detail', id=grade.student_id))
    
    return render_template('grade_form.html', form=form, student=grade.student, 
                         title='Edit Grade', grade=grade)

@bp.route('/grade/<int:id>/delete', methods=['POST'])
@login_required
def delete_grade(id):
    grade = Grade.query.get_or_404(id)
    student_id = grade.student_id
    db.session.delete(grade)
    db.session.commit()
    flash('Grade deleted successfully!', 'success')
    return redirect(url_for('main.student_detail', id=student_id))

# Disciplinary Note routes
@bp.route('/student/<int:student_id>/disciplinary/add', methods=['GET', 'POST'])
@login_required
def add_disciplinary_note(student_id):
    student = Student.query.get_or_404(student_id)
    form = DisciplinaryNoteForm()
    
    if form.validate_on_submit():
        note = DisciplinaryNote(
            student_id=student_id,
            description=form.description.data,
            severity=form.severity.data,
            created_by=form.created_by.data or current_user.username
        )
        db.session.add(note)
        db.session.commit()
        flash('Disciplinary note added successfully!', 'success')
        return redirect(url_for('main.student_detail', id=student_id))
    
    form.created_by.data = current_user.username
    return render_template('disciplinary_form.html', form=form, student=student, 
                         title='Add Disciplinary Note')

@bp.route('/disciplinary/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_disciplinary_note(id):
    note = DisciplinaryNote.query.get_or_404(id)
    form = DisciplinaryNoteForm(obj=note)
    
    if form.validate_on_submit():
        note.description = form.description.data
        note.severity = form.severity.data
        note.created_by = form.created_by.data
        
        db.session.commit()
        flash('Disciplinary note updated successfully!', 'success')
        return redirect(url_for('main.student_detail', id=note.student_id))
    
    return render_template('disciplinary_form.html', form=form, student=note.student,
                         title='Edit Disciplinary Note', note=note)

@bp.route('/disciplinary/<int:id>/delete', methods=['POST'])
@login_required
def delete_disciplinary_note(id):
    note = DisciplinaryNote.query.get_or_404(id)
    student_id = note.student_id
    db.session.delete(note)
    db.session.commit()
    flash('Disciplinary note deleted successfully!', 'success')
    return redirect(url_for('main.student_detail', id=student_id))

# General Note routes
@bp.route('/student/<int:student_id>/note/add', methods=['GET', 'POST'])
@login_required
def add_general_note(student_id):
    student = Student.query.get_or_404(student_id)
    form = GeneralNoteForm()
    
    if form.validate_on_submit():
        note = GeneralNote(
            student_id=student_id,
            title=form.title.data,
            content=form.content.data,
            created_by=form.created_by.data or current_user.username
        )
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully!', 'success')
        return redirect(url_for('main.student_detail', id=student_id))
    
    form.created_by.data = current_user.username
    return render_template('note_form.html', form=form, student=student, title='Add Note')

@bp.route('/note/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_general_note(id):
    note = GeneralNote.query.get_or_404(id)
    form = GeneralNoteForm(obj=note)
    
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.created_by = form.created_by.data
        
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('main.student_detail', id=note.student_id))
    
    return render_template('note_form.html', form=form, student=note.student,
                         title='Edit Note', note=note)

@bp.route('/note/<int:id>/delete', methods=['POST'])
@login_required
def delete_general_note(id):
    note = GeneralNote.query.get_or_404(id)
    student_id = note.student_id
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('main.student_detail', id=student_id))

# Scholarship routes
@bp.route('/student/<int:student_id>/scholarship/add', methods=['GET', 'POST'])
@login_required
def add_scholarship(student_id):
    student = Student.query.get_or_404(student_id)
    form = ScholarshipForm()
    
    if form.validate_on_submit():
        scholarship = Scholarship(
            student_id=student_id,
            name=form.name.data,
            amount=form.amount.data,
            source=form.source.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data
        )
        db.session.add(scholarship)
        db.session.commit()
        flash('Scholarship added successfully!', 'success')
        return redirect(url_for('main.student_detail', id=student_id))
    
    return render_template('scholarship_form.html', form=form, student=student,
                         title='Add Scholarship')

@bp.route('/scholarship/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_scholarship(id):
    scholarship = Scholarship.query.get_or_404(id)
    form = ScholarshipForm(obj=scholarship)
    
    if form.validate_on_submit():
        scholarship.name = form.name.data
        scholarship.amount = form.amount.data
        scholarship.source = form.source.data
        scholarship.start_date = form.start_date.data
        scholarship.end_date = form.end_date.data
        scholarship.status = form.status.data
        
        db.session.commit()
        flash('Scholarship updated successfully!', 'success')
        return redirect(url_for('main.student_detail', id=scholarship.student_id))
    
    return render_template('scholarship_form.html', form=form, student=scholarship.student,
                         title='Edit Scholarship', scholarship=scholarship)

@bp.route('/scholarship/<int:id>/delete', methods=['POST'])
@login_required
def delete_scholarship(id):
    scholarship = Scholarship.query.get_or_404(id)
    student_id = scholarship.student_id
    db.session.delete(scholarship)
    db.session.commit()
    flash('Scholarship deleted successfully!', 'success')
    return redirect(url_for('main.student_detail', id=student_id))

# Import/Export routes
@bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_students():
    form = ImportForm()
    
    if form.validate_on_submit():
        flash('Excel import functionality requires pandas and openpyxl. Please install these packages first.', 'warning')
        # TODO: Implement Excel import when pandas is available
        # For now, show the form but don't process
    
    return render_template('import.html', form=form)

@bp.route('/export')
@login_required
def export_students():
    flash('CSV export functionality requires pandas. Please install pandas first.', 'warning')
    # TODO: Implement Excel export when pandas is available
    # For now, redirect back to students page
    return redirect(url_for('main.students'))