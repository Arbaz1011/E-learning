#!/bin/bash

# Exit on error
set -e

echo "Starting E-Learning Platform deployment..."

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
echo "Installing system dependencies..."
sudo apt install -y python3-pip python3-venv nginx

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
FLASK_APP=wsgi.py
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
DATABASE_URL=sqlite:///elearning.db
EOL
fi

# Initialize database and create admin user
echo "Setting up database..."
python create_admin.py

# Set up Gunicorn service
echo "Setting up Gunicorn service..."
sudo bash -c 'cat > /etc/systemd/system/elearning.service << EOL
[Unit]
Description=E-Learning Platform
After=network.target

[Service]
User=ubuntu
WorkingDirectory='$(pwd)'
Environment="PATH='$(pwd)'/venv/bin"
ExecStart='$(pwd)'/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app

[Install]
WantedBy=multi-user.target
EOL'

# Set up Nginx configuration
echo "Setting up Nginx configuration..."
sudo bash -c 'cat > /etc/nginx/sites-available/elearning << EOL
server {
    listen 80;
    server_name $HOSTNAME;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /static {
        alias '$(pwd)'/app/static;
    }
}
EOL'

# Enable the Nginx site
echo "Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/elearning /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Create uploads directory if it doesn't exist
echo "Creating uploads directory..."
mkdir -p app/static/uploads
sudo chown -R ubuntu:ubuntu app/static/uploads

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Start and enable services
echo "Starting services..."
sudo systemctl enable elearning
sudo systemctl restart elearning
sudo systemctl restart nginx

# Check service status
echo "Checking service status..."
sudo systemctl status elearning --no-pager
sudo systemctl status nginx --no-pager

echo "Deployment completed successfully!"
echo "Your application should now be accessible at: http://$HOSTNAME"
echo ""
echo "To view application logs:"
echo "  sudo journalctl -u elearning.service -f"
echo ""
echo "To restart the application:"
echo "  sudo systemctl restart elearning"
