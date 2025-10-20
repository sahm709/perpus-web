web: gunicorn perpus_web.wsgi --log-file - 

web: python manage.py migrate && gunicorn perpus_web.wsgi