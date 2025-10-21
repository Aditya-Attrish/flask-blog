# Flask Blog Application

A full-featured blog application built with Flask that demonstrates modern web development practices, user authentication, and CRUD operations.

## 🚀 Project Overview

This is a complete blog platform where users can create accounts, write blog posts, and manage their content. The application showcases proficiency in Python web development, database management, and user interface design.

## ✨ Key Features

### User Management
- **User Registration & Authentication**: Secure user registration with username validation
- **Login/Logout System**: Session management with Flask-Login
- **Profile Management**: Users can edit profiles and upload profile pictures
- **Password Validation**: Confirm password functionality during registration

### Blog Functionality
- **Create Posts**: Rich content creation with thumbnail uploads
- **Edit Posts**: Full CRUD operations for blog posts
- **Delete Posts**: Secure deletion with author verification
- **Pagination**: Efficient content browsing with configurable posts per page
- **Individual Post Views**: Dedicated pages for each blog post

### Additional Features
- **Contact Form**: Contact submission system with database storage
- **About Page**: Static content pages
- **Admin Dashboard**: Administrative interface for content management
- **File Upload**: Secure file handling for thumbnails and profile images
- **Responsive Design**: Bootstrap-powered responsive UI

## 🛠 Technical Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **File Handling**: Werkzeug secure filename utilities
- **Configuration**: JSON-based configuration management

## 📁 Project Structure

```
flask-blog/
├── __init__.py              # Application factory and models
├── routes.py                # URL routes and view functions
├── main.py                  # Application entry point
├── config.json             # Configuration parameters
├── requirements.txt        # Python dependencies
├── instance/
│   └── blog.db            # SQLite database
├── static/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── thumb/             # Blog post thumbnails
│   └── SVG/               # Icon assets
└── templates/
    ├── Base.html          # Base template
    ├── index.html         # Homepage
    ├── login.html         # Login form
    ├── register.html      # Registration form
    ├── admin.html         # Admin dashboard
    ├── Edit.html          # Post editor
    └── ...               # Other templates
```

## 🗄 Database Schema

### User Model
- ID (Primary Key)
- Username (Unique)
- Email (Unique)
- Password
- Profile Image
- One-to-many relationship with BlogPost

### BlogPost Model
- Serial Number (Primary Key)
- Title (120 charactors)
- Excerpt (300 charactors)
- Slug (300 charactors)
- Content (Text)
- Thumbnail Image Path
- views (Integer)
- Date Posted (Datetime)
- Created_at (Datetime)
- Author (Foreign Key to User)
- Comment (Foreign Key to Comment)

### Contact Model
- ID (Primary Key)
- Name
- Email
- Message

## 🔧 Key Implementation Highlights

### Security Features
- **Secure File Uploads**: Using `secure_filename()` to prevent directory traversal
- **User Authorization**: Route protection with `@login_required` decorator
- **Author Verification**: Users can only edit/delete their own posts
- **Password Confirmation**: Registration includes password matching validation

### Database Operations
- **SQLAlchemy ORM**: Clean database interactions with relationship mapping
- **Pagination**: Efficient content loading with Flask-SQLAlchemy pagination
- **Transaction Management**: Proper commit/rollback handling

### File Management
- **Image Upload System**: Handles thumbnails and profile pictures
- **Path Configuration**: Configurable upload directories
- **File Validation**: Secure file handling with existence checks

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install flask flask-sqlalchemy flask-login werkzeug
   ```

2. **Initialize Database**:
   ```bash
   python main.py
   ```

3. **Access Application**:
   - Open browser to `http://localhost:9000`
   - Register a new account or login
   - Start creating blog posts!

## 🎯 Technical Skills Demonstrated

- **Flask Framework**: Route handling, templating, request processing
- **Database Design**: Relational database modeling with SQLAlchemy
- **User Authentication**: Session management and security
- **File Handling**: Upload, validation, and storage
- **Frontend Integration**: Template inheritance and responsive design
- **Error Handling**: Form validation and user feedback
- **Code Organization**: Clean separation of concerns

## 🔮 Future Enhancements

- Comment system for blog posts
- Tag/category system for content organization
- Search functionality
- Email notifications
- Rich text editor integration
- API endpoints for mobile app integration

## 📋 Configuration

The application uses `config.json` for easy configuration:
```json
{
    "params": {
        "blog_web_name": "My Blog",
        "no_of_per_page": 2
    }
}
```

## 🎓 Learning Outcomes

This project demonstrates:
- Full-stack web development with Python
- Database design and ORM usage
- User authentication and authorization
- File upload and management
- Responsive web design
- Code organization and best practices

---

*This project showcases practical web development skills and can be easily extended with additional features. The codebase follows Flask best practices and demonstrates clean, maintainable code structure.*
