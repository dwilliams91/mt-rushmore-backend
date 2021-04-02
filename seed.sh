git rm -rf --cached db.sqlite3
rm -rf mtrushmoreapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations mtrushmoreusapi
python3 manage.py migrate mtrushmoreusapi

