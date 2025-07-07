from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SelectField, TextAreaField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from datetime import datetime

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=1, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[Optional()])
    year_of_study = IntegerField('Year of Study', validators=[Optional(), NumberRange(min=1, max=10)])
    program = StringField('Program/Track', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Save Student')

class GradeForm(FlaskForm):
    subject_name = StringField('Subject Name', validators=[DataRequired(), Length(min=1, max=100)])
    grade = FloatField('Grade', validators=[DataRequired(), NumberRange(min=0, max=100)])
    semester = StringField('Semester', validators=[DataRequired(), Length(min=1, max=20)])
    teacher_name = StringField('Teacher Name', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Save Grade')

class DisciplinaryNoteForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=1000)])
    severity = SelectField('Severity', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired()])
    created_by = StringField('Created By', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Save Note')

class GeneralNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=1000)])
    created_by = StringField('Created By', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Save Note')

class ScholarshipForm(FlaskForm):
    name = StringField('Scholarship Name', validators=[DataRequired(), Length(min=1, max=100)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    source = StringField('Source', validators=[DataRequired(), Length(min=1, max=100)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('expired', 'Expired'), ('suspended', 'Suspended')], validators=[DataRequired()])
    submit = SubmitField('Save Scholarship')

class ImportForm(FlaskForm):
    file = FileField('Excel File', validators=[DataRequired(), FileAllowed(['xlsx', 'xls'], 'Excel files only!')])
    submit = SubmitField('Import Students')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=120)])
    submit = SubmitField('Login')