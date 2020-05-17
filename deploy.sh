git pull
pip install -r requirements/base.txt
./manage.py migrate
./manage.py collectstatic --noinput
systemctl restart gunicorn
