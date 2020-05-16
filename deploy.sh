git pull
./manage.py collectstatic --noinput
systemctl restart gunicorn
