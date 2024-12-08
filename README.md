# E-Learning Platform

A comprehensive e-learning platform built with Flask that allows instructors to create courses and students to enroll and learn.

## Local Development Setup

1. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up the admin user and database:
```bash
python create_admin.py
```

This script will:
- Initialize the database
- Create necessary tables
- Set up an admin user with the following credentials:
  - Email: admin@example.com
  - Password: admin123

## Running Locally

1. Start the development server:
```bash
python wsgi.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Log in with the admin credentials created above.

## Deploying to AWS EC2

1. Launch and connect to your EC2 instance following the instructions in `deployment_guide.md`

2. Clone the repository on your EC2 instance:
```bash
git clone https://github.com/your-username/E-learn.git
cd E-learn
```

3. Make the deployment script executable:
```bash
chmod +x deploy.sh
```

4. Run the deployment script:
```bash
./deploy.sh
```

The script will:
- Install system dependencies
- Set up Python virtual environment
- Install Python packages
- Configure Nginx and Gunicorn
- Set up the database
- Start the application

For detailed deployment instructions and troubleshooting, see `deployment_guide.md`

## Features

- User authentication and authorization
- Course creation and management
- Student enrollment system
- Course content management
- Notes taking system
- Discussion forum
- Admin dashboard
- File upload support
- User profiles

## Project Structure

```
e-learning/
├── app/
│   ├── admin/         # Admin panel functionality
│   ├── auth/          # Authentication
│   ├── courses/       # Course management
│   ├── forum/         # Discussion forum
│   ├── main/          # Main routes
│   ├── notes/         # Notes functionality
│   ├── static/        # Static files
│   ├── templates/     # HTML templates
│   └── models.py      # Database models
├── migrations/        # Database migrations
├── config.py         # Configuration
├── create_admin.py   # Admin user creation
├── deploy.sh        # Deployment script
├── deployment_guide.md # EC2 deployment instructions
└── wsgi.py          # Application entry point
```

## Configuration

The application can be configured through environment variables or the config.py file:

- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection URL (defaults to SQLite)
- `MAIL_USERNAME`: Email for notifications
- `MAIL_PASSWORD`: Email password

## Production Deployment Considerations

1. SSL/HTTPS Setup:
   - Follow the SSL setup instructions in deployment_guide.md
   - Use Certbot for free SSL certificates

2. Database:
   - Consider using a managed database service for production
   - Regular backups are recommended

3. File Storage:
   - For production, consider using AWS S3 for file storage
   - Ensure proper backup of uploaded files

4. Monitoring:
   - Set up monitoring for the EC2 instance
   - Configure logging and alerts

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
