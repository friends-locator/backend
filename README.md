# Where are my friends?

Description: backend's API.

Used technologies:
-
    - python 3.11
    - django 4.1
    - djangorestframework 3.14
    - python-dotenv 0.21.1
    - django-filter 22.1
    - PostgreSQL ...
    - Docker ...

Features:
-
    - You can search and add new friends
    - You can view your friends location
    - Admin-zone
    - ...


# Launch instructions:

## enviroment:
Replace file called ".env.sample" with file called ".env" file and fill it with required keys:
- SECRET_KEY=...
- DB_ENGINE=...
- DB_NAME=...
- POSTGRES_USER=...
- POSTGRES_PASSWORD=...
- DB_HOST=db
- DB_PORT=5432

## Docker:

Build and launch containers:

    #### docker-compose up -d --build
For now app is available at localhost

### Some additional commands:
1. Create admin-user:
    #### winpty docker-compose exec backend python manage.py createsuperuser
2. To make dump of DB:
    #### docker-compose exec backend python manage.py dumpdata > your_fixture_name.json
3. To load fixtures:
    #### docker-compose exec backend python manage.py loaddata your_fixture_name.json

If you'll need any *manage.py* commands then you'll want to use prefix:

    docker-compose exec backend python manage.py *comand*

Admin-zone is available at:

    https://your_host/admin/

All available endpoints and responses you can find in documentation:

    https://your_host/api/docs/


Examples:
-
    - GET http://127.0.0.1:8000/api/v1/...
    - POST http://127.0.0.1:8000/api/v1/...
    - DELETE http://127.0.0.1:8000/api/v1/...
    - PUT http://127.0.0.1:8000/api/v1/...

Examples of responses:
-
...

Authors: Larkin Michael, Maria Klyahina, Sergey Samoylov, Oksana
