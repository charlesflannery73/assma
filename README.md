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
+ remove anonymouse users
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
sudo su assmauser
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