from app import create_app, db
from app.models import User
from datetime import datetime
from flask_migrate import Migrate, init, migrate, upgrade, current
import os
from sqlalchemy.exc import OperationalError
import sys

def setup_database(app):
    """Set up the database and migrations"""
    with app.app_context():
        try:
            # Create migrations directory if it doesn't exist
            if not os.path.exists('migrations'):
                print("Initializing migrations directory...")
                init()
                
                # Create the initial migration
                print("Creating initial migration...")
                migrate(message='initial migration')
            
            # Create the database tables
            print("Creating database tables...")
            db.create_all()
            
            # Apply any pending migrations
            print("Applying migrations...")
            upgrade()
            
            print("Database setup completed successfully!")
            
        except Exception as e:
            print(f"Error setting up database: {e}")
            print("\nTroubleshooting steps:")
            print("1. Ensure you have activated your virtual environment")
            print("2. Make sure all required packages are installed:")
            print("   pip install -r requirements.txt")
            print("3. Check if the database path is writable")
            print("4. Verify your database configuration in config.py")
            sys.exit(1)

def create_admin():
    """Create admin user if it doesn't exist"""
    app = create_app()
    
    print("Starting database setup...")
    setup_database(app)
    
    with app.app_context():
        try:
            # Check if admin already exists
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    role='admin',
                    created_at=datetime.utcnow(),
                    is_active=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print('\nAdmin user created successfully!')
                print('Login credentials:')
                print('Email: admin@example.com')
                print('Password: admin123')
            else:
                print('\nAdmin user already exists.')
        except OperationalError as e:
            print(f"\nDatabase error: {e}")
            print("Please ensure your database is properly configured in config.py")
            sys.exit(1)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            sys.exit(1)

if __name__ == '__main__':
    print("Starting database setup and admin user creation...")
    create_admin()
