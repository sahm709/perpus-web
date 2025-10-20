release: python manage.py migrate
web: gunicorn perpus_web.wsgi:application --bind 0.0.0.0:$PORT