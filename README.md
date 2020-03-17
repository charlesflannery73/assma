git clone https://github.com/charlesflannery73/assma

cd assma

sudo apt-get install python3-venv

python3 -m venv .venv --prompt assma

source .venv/bin/activate

pip install -r requirements.txt

 #if wanting to clean all and start again, start from here, if new install, skip this step

rm -rf db.sqlite3 web/0*

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
