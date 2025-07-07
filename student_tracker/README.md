# Student Tracker Admin System

A comprehensive Flask web application for managing students in an academic administration dashboard.

## Features

### 🧑 Student Management
- Complete student profiles with personal information
- Student ID, name, email, phone, date of birth, gender
- Year of study and program/track assignment
- Search and filter functionality
- Bulk import from Excel files

### 📊 Grade Tracking
- Record grades for various subjects
- Track semester, teacher, and date information
- View grade history and calculate averages
- Grade-based filtering and reporting

### ⚠️ Disciplinary Notes
- Add disciplinary notes with severity levels (Low, Medium, High)
- Track incident dates and responsible staff
- Edit and delete notes as needed
- Filter by severity and student

### 📝 General Notes
- Add general notes for each student
- Support for learning accommodations, scholarship renewals, etc.
- Timestamped with author information
- Full CRUD operations

### 🎓 Scholarship Management
- Track scholarship awards and amounts
- Monitor scholarship duration and status
- Support for multiple scholarships per student
- Filter by scholarship status (Active, Expired, Suspended)

### 🎨 User Interface
- Clean, responsive design with Bootstrap 5
- Intuitive navigation and dashboard
- Mobile-friendly interface
- Professional admin-focused design

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/galshohat/student-manage-ex.git
   cd student-manage-ex/student_tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - Login with default credentials: `admin` / `admin123`

## Project Structure

```
student_tracker/
│
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes.py            # Main application routes
│   ├── auth.py              # Authentication routes
│   ├── forms.py             # WTForms form definitions
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── students.html
│   │   ├── student_detail.html
│   │   ├── student_form.html
│   │   ├── grade_form.html
│   │   ├── disciplinary_form.html
│   │   ├── note_form.html
│   │   ├── scholarship_form.html
│   │   ├── import.html
│   │   └── auth/
│   │       └── login.html
│   └── static/
│       └── styles.css       # Custom CSS
│
├── data/
│   └── example_import.xlsx  # Sample import file
│
├── run.py                   # Application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Database Models

### Student
- ID, Student ID, Full Name, Email, Phone
- Date of Birth, Gender, Year of Study, Program
- Timestamps for creation and updates

### Grade
- Subject Name, Grade (0-100), Semester
- Teacher Name, Date Recorded
- Foreign key to Student

### DisciplinaryNote
- Description, Severity Level, Date Created
- Created By (staff member)
- Foreign key to Student

### GeneralNote
- Title, Content, Date Created
- Created By (staff member)  
- Foreign key to Student

### Scholarship
- Name, Amount, Source, Duration
- Status (Active, Expired, Suspended)
- Foreign key to Student

## Excel Import Format

For bulk student import, use an Excel file with these columns:

| Column | Required | Description |
|--------|----------|-------------|
| student_id | Yes | Unique student identifier |
| full_name | Yes | Student's full name |
| email | Yes | Student's email address |
| phone | No | Phone number |
| date_of_birth | No | Format: YYYY-MM-DD |
| gender | No | Male, Female, or Other |
| year_of_study | No | Numeric value |
| program | No | Program/track name |

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### Default Settings
- Database: SQLite (`student_tracker.db`)
- Upload limit: 16MB
- Session timeout: 4 hours

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Login required for all student data access
- CSRF protection on forms
- File upload validation

## API Endpoints

### Authentication
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Students
- `GET /` or `/dashboard` - Dashboard overview
- `GET /students` - Student list with search/filter
- `GET /student/<id>` - Student detail view
- `GET/POST /student/add` - Add new student
- `GET/POST /student/<id>/edit` - Edit student
- `POST /student/<id>/delete` - Delete student

### Grades
- `GET/POST /student/<id>/grade/add` - Add grade
- `GET/POST /grade/<id>/edit` - Edit grade
- `POST /grade/<id>/delete` - Delete grade

### Notes & Scholarships
- Similar CRUD patterns for disciplinary notes, general notes, and scholarships

### Import/Export
- `GET/POST /import` - Import students from Excel
- `GET /export` - Export students to Excel

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python run.py
```

### Database Initialization
The database is automatically created on first run with a default admin user.

### Adding New Features
1. Update models in `app/models.py`
2. Create forms in `app/forms.py`
3. Add routes in `app/routes.py`
4. Create templates in `app/templates/`

## Production Deployment

1. Set environment variables:
   ```bash
   export SECRET_KEY="your-production-secret-key"
   export DATABASE_URL="your-database-url"
   ```

2. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```

3. Configure nginx or Apache as reverse proxy
4. Set up SSL/TLS certificates
5. Configure database backups

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## Changelog

### Version 1.0.0
- Initial release with full student management functionality
- Authentication system
- Grade tracking
- Note management
- Scholarship tracking
- Excel import/export
- Responsive web interface