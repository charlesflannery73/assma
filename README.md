# assma

#setup
git clone https://github.com/charlesflannery73/assma
cd assma
python3 -m venv .venv --prompt assma
source .venv/bin/activate
pip install -r requirements.txt
# if wanting to clean all and start again
# rm -rf db.sqlite3 assma/__pycache__ web/__pycache__ users/__pycache__ 
# or  leave users alone
# rm -rf db.sqlite3 assma/__pycache__ web/__pycache__ 
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
