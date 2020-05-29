Based on the instructions from 
```
https://www.shellvoide.com/hacks/installing-django-application-with-nginx-mysql-and-gunicorn-on-ubuntu-vps/
```

# Install dependant packages for Ubuntu 18.04
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
+ validate password component (if asked)
+ set root password
+ remove anonymous users
+ disallow root login remotely
+ remove test database
+ reload privileges
```
sudo mysql -p

CREATE DATABASE assma;
CREATE USER 'assmauser'@'localhost' IDENTIFIED BY 'password_change_me';
GRANT ALL ON assma.* TO 'assmauser'@'localhost';
ALTER DATABASE assma CHARACTER SET 'utf8';
exit;
```
##Create assmauser
```
sudo adduser --disabled-password assmauser -ingroup www-data
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
 
suggested number of workers is 2 * n + 1 where n = number of cores

```
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=assmauser
Group=www-data
WorkingDirectory=/home/assmauser/assma/assma
ExecStart=/home/assmauser/assma/.venv/bin/gunicorn --access-logfile - --workers 5 --chdir /home/assmauser/assma --bind unix:/home/assmauser/assma/assma.sock assma.wsgi:application

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

# create self-signed certificate
```
sudo mkdir /etc/ssl/private
sudo chmod 700 /etc/ssl/private
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
openssl dhparam -out /etc/pki/tls/certs/dhparam.pem 2048
```

# nginx setup
create file /etc/nginx/snippets/self-signed.conf
```
ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
```
create file /etc/nginx/snippets/ssl-params.conf
```
# from https://cipherli.st/
# and https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html

ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
ssl_ecdh_curve secp384r1;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
# Disable preloading HSTS for now.  You can use the commented out header line that includes
# the "preload" directive if you understand the implications.
#add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
add_header Strict-Transport-Security "max-age=63072000; includeSubdomains";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;

ssl_dhparam /etc/ssl/certs/dhparam.pem;
```


create file /etc/nginx/sites-available/assma
```
server {
       listen 80 default_server;
       server_name 127.0.0.1;
       return 301 https://$server_name$request_uri;
}

server {
       listen 443 ssl http2 default_server;
       include snippets/self-signed.conf;
       include snippets/ssl-params.conf;

       location /static/ {
            root /home/assmauser/assma;
       }

       location /media/ {
            root /home/assmauser/assma;
       }

       location / {
            include proxy_params;
            proxy_pass http://unix:/home/assmauser/assma/assma.sock;
       }
}
```

```
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/assma /etc/nginx/sites-enabled/assma
nginx -t
ufw allow 'Nginx Full'
systemctl restart nginx
```
