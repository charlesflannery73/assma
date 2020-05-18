Based on the instructions from 
```
https://www.shellvoide.com/hacks/installing-django-application-with-nginx-mysql-and-gunicorn-on-ubuntu-vps/
```

# Install dependant packages
For Ubuntu 18.04
```
sudo apt-get install python3-venv nginx mysql-server python3-pip libmysqlclient-dev ufw
```

# For development
## get assma and runserver
```
git clone https://github.com/charlesflannery73/assma
cd assma
python3 -m venv .venv --prompt assma
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata groups
python manage.py createsuperuser
python manage.py runserver
```
# For deployment
##Setup MySql
```
sudo mysql_secure_installation
```
+ set root password
+ remove anonymous users
+ disallow root login remotely
+ remove test database
+ reload privileges
```
sudo mysql

CREATE DATABASE assma;
CREATE USER assmauser;
GRANT ALL ON assma.* TO 'assmauser'@'localhost' IDENTIFIED BY 'password_change_me';
ALTER DATABASE assma CHARACTER SET 'utf8';
exit;
```
##Create assmauser
```
sudo adduser --disabled-password assmauser
sudo su - assmauser
```
## Install assma
```
git clone https://github.com/charlesflannery73/assma
cd assma
python3 -m venv .venv --prompt assma
source .venv/bin/activate
pip install -r requirements.txt
```

create .env file
---
```
# create .env file in same dir as assma/assma/settings.py

SECRET_KEY=my-super-secret-key-erlksduhiuyhwnci4nu9576w7vtysueh-change-me
DEBUG=False
ALLOWED_HOSTS='*'
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

SECURE_HSTS_SECONDS=60
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

DB_ENGINE=django.db.backends.mysql
DB_NAME=assma
DB_USER=assmauser
DB_PASSWORD=password_change_me
DB_HOST=127.0.0.1
DB_PORT=3306
```

# setup database
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata groups
python manage.py collectstatic
python manage.py createsuperuser
```

# setup gunicorn
## create daemon file
 /etc/systemd/system/gunicorn.service
```
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=assmauser
Group=www-data
WorkingDirectory=/home/assmauser/assma/assma
ExecStart=/home/assmauser/assma/.venv/bin/gunicorn --access-logfile - --workers 3 --chdir /home/assmauser/assma --bind unix:/home/assmauser/assma/assma/assma.sock assma.wsgi:application

[Install]
WantedBy=multi-user.target
```

## start gunicorn daemon
```
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn
systemctl status gunicorn

```
# nginx setup
create file 
/etc/nginx/sites-available/assma
```
server {
       listen 80;
       server_name 127.0.0.1;
       location = /static/favicon.ico {access_log off;log_not_found off;}

       location /static/ {
            root /home/assmauser/assma;    
       }

       location /media/ {
            root /home/assmauser/assma;    
       }
       
       location / {
            include proxy_params;
            proxy_pass http://unix:/home/eassmauser/assma/assma/assma.sock;
       }
}

```

```
ln -s /etc/nginx/sites-available/assma /etc/nginx/sites-enabled/assma
nginx -t
ufw allow 'Nginx Full'
systemctl restart nginx
```

