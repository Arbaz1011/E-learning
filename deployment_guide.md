# Deploying E-Learning Platform on AWS EC2

This guide walks through deploying the E-Learning platform on an AWS EC2 instance.

## 1. EC2 Instance Setup

1. Launch an EC2 instance:
   - Choose Ubuntu Server 22.04 LTS
   - Select t2.micro (free tier) or larger
   - Configure Security Group:
     ```
     HTTP (80)      : 0.0.0.0/0
     HTTPS (443)    : 0.0.0.0/0
     SSH (22)       : Your IP
     ```
   - Create and download your key pair (.pem file)

2. Make your key pair file read-only:
   ```bash
   chmod 400 your-key.pem
   ```

3. Connect to your instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-public-dns
   ```

## 2. System Setup

1. Update system packages:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. Install required system packages:
   ```bash
   sudo apt install -y python3-pip python3-venv nginx
   ```

## 3. Application Deployment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/E-learn.git
   cd E-learn
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   sudo nano .env
   ```
   Add:
   ```
   FLASK_APP=wsgi.py
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///elearning.db
   ```

5. Initialize database:
   ```bash
   python create_admin.py
   ```

## 4. Gunicorn Setup

1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/elearning.service
   ```
   Add:
   ```ini
   [Unit]
   Description=E-Learning Platform
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/E-learn
   Environment="PATH=/home/ubuntu/E-learn/venv/bin"
   ExecStart=/home/ubuntu/E-learn/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```

2. Start and enable the service:
   ```bash
   sudo systemctl start elearning
   sudo systemctl enable elearning
   ```

## 5. Nginx Setup

1. Create Nginx configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/elearning
   ```
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # or your EC2 public IP

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /home/ubuntu/E-learn/app/static;
       }
   }
   ```

2. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/elearning /etc/nginx/sites-enabled
   sudo rm /etc/nginx/sites-enabled/default  # remove default site
   sudo systemctl restart nginx
   ```

## 6. SSL Setup (Optional)

1. Install Certbot:
   ```bash
   sudo snap install --classic certbot
   sudo ln -s /snap/bin/certbot /usr/bin/certbot
   ```

2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

## Maintenance

- View application logs:
  ```bash
  sudo journalctl -u elearning.service
  ```

- Restart application:
  ```bash
  sudo systemctl restart elearning
  ```

- Update application:
  ```bash
  cd E-learn
  git pull
  source venv/bin/activate
  pip install -r requirements.txt
  sudo systemctl restart elearning
  ```

## Troubleshooting

1. Check Gunicorn status:
   ```bash
   sudo systemctl status elearning
   ```

2. Check Nginx status:
   ```bash
   sudo systemctl status nginx
   ```

3. View Nginx error logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

4. Check application logs:
   ```bash
   sudo journalctl -u elearning.service -f
