### Install dependant packages
For Ubuntu 18.04
```
sudo apt-get install python3-venv nginx mysql-server python3-pip libmysqlclient-dev ufw
```
### Setup MySql
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
GRANT ALL ON assma.* TO 'assmauser'@'localhost' IDENTIFIED BY '8ik,(OL>';
ALTER DATABASE assma CHARACTER SET 'utf8';
exit;
```

Create assmauser
---
```
sudo adduser --disabled-password assmauser
sudo su - assmauser
```

Get assma
---------
```
git clone https://github.com/charlesflannery73/assma
cd assma
python3 -m venv .venv --prompt assma
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

create  production .env file if deploying to production
---
```
# create .env file in same dir as assma/assma/settings.py

SECRET_KEY=my-super-secret-key-erlksduhiuyhwnci4nu9576w7vtysueh-change-me
DEBUG=False
ALLOWED_HOSTS='0.0.0.0'

DB_ENGINE=django.db.backends.mysql
DB_NAME=assma
DB_USER=assmauser
DB_PASSWORD=change-me
DB_HOST=127.0.0.1
DB_PORT=3306

```
