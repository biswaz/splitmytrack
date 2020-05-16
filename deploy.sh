git pull
./manage.py migrate
./manage.py collectstatic --noinput
systemctl restart gunicorn
