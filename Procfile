web: gunicorn perpus_web.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn perpus_web.wsgi