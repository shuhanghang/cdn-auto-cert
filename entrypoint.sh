gunicorn  -w 1 app:app -b 0.0.0.0:8080 --access-logfile=- --error-logfile=-
