# Where are my friends?


### Link for the website:

https://flap.acceleratorpracticum.ru/


### Project description:

Web application for finding friends on the map. Here people can search and add new friends, share their geolocation and see the location of a friend, gather for fun meetings and have a great time.


Used technologies:
-
    - python 3.11
    - django 4.1
    - djangorestframework 3.14
    - python-dotenv 0.21.1
    - django-filter 22.1
    - PostgreSQL
    - Docker


Features:
-
    - You can search and add new friends
    - You can view your friends location
    - Admin-zone
    - ...


### How to start a project:

1. Clone a repository and change to it on the command line:

```
git clone git@github.com:friends-locator/backend.git
```

```
cd backend
```

2. Create and activate virtual environment:

```
python3 -m venv venv
or
python -m venv venv
```

```
. venv/bin/activate
or
source venv/Scripts/activate
```

3. Install requirements from a file requirements.txt:

```
pip install -r requirements.txt
```

4. Run migrations:

```
python3 manage.py migrate
or
python manage.py migrate
```

5. Start project:

```
python3 manage.py runserver
or
python manage.py runserver
```


### How to run documentation:

1. Open application Docker

2. Go to directory infra:

```
cd infra
```

3. Run docker-compose:

```
docker-compose up
```

Documentation and request examples are available at:

```
http://flap.acceleratorpracticum.ru/api/docs/
```


### How to run a project on a remote server:

1. Clone a repository and change to it on the command line:

```
git clone git@github.com:friends-locator/backend.git
```

```
cd backend
```

2. Copy the docker-compose.yml and nginx.conf files from the infra folder to the remote server:

```
cd backend/infra/
```

```
scp docker-compose.yml <username>@<IP>:/home/<username>/
scp nginx.conf <username>@<IP>:/home/<username>/
# username - username of the server
# IP - public IP address of the server
```

3. In the repository settings on GitHub, create environment variables in the Settings -> Secrets -> Actions:

```
SSH_KEY # private ssh key
PASSPHRASE # ssh key password
DOCKER_USERNAME # login DockerHub
DOCKER_PASSWORD # password DockerHub
SECRET_KEY # secret key from Django project
HOST # public IP address of the server
USER # username of the server

DB_ENGINE=django.db.backends.postgresql # indicate that we are working with postgresql
DB_NAME=postgres # database name
POSTGRES_USER=postgres # login to connect to the database
POSTGRES_PASSWORD=postgres # password to connect to the database (set your own)
DB_HOST=db # name of the service (container)
DB_PORT=5432 # port to connect to the database
```

4. Run docker-compose on the server:

```
sudo docker-compose up -d
```

5. Now in the container you need to create and run migrations, collect statics and create a superuser. Execute commands in sequence:

```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```


### Project authors:

Larkin Mikhail
https://github.com/IhateChoosingNickNames

Klyahina Maria
https://github.com/ifyoumasha

Sheremet Oksana
https://github.com/sheremet-o

Zolkov Denis
https://github.com/ggastly

Antonevich Fedor
https://github.com/LevityLoveLight
