# healthwise


## Project setup
```

1. Create virtual environment
python3 -m venv venv

2. Activate virtual environment
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Migrate database
python manage.py migrate

5. Create superuser
python manage.py createsuperuser

6. Start the server
python manage.py runserver

Open a new tab in your terminal and run the following command

7. Start the celery worker
celery -A healthwise worker --loglevel=info

Open a new tab in your terminal and run the following command

8. Start the redis server
redis-server


In case there is an error with the redis server, run the following command

brew services start redis


To access the admin page
http://127.0.0.1:8000/admin/login/?next=/admin/

To access the home page
http://127.0.0.1:8000/