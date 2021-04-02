git rm -rf --cached db.sqlite3
rm -rf mtrushmoreapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations mtrushmoreusapi
python3 manage.py migrate mtrushmoreusapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata rushmoreusers
python3 manage.py loaddata groups
python3 manage.py loaddata threads
python3 manage.py loaddata comments
python3 manage.py loaddata posts
python3 manage.py loaddata options





