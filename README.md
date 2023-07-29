# Где мои друзья?

## Демо

https://flap.acceleratorpracticum.ru/

## Оглавление

- [Описание](#description)
- [Стек технологий](#stack)
- [Особенности](#features)
- [Настройки](#settings)
- [Руководство для запуска на удаленном сервере](#howto-remote)
- [Руководство для разработчиков](#howto-dev)
- [Авторы](#authors)

## <a id="description"></a> Описание

Данное веб-приложение предназначено для поиска друзей на карте.
Здесь люди могут искать и добавлять новых друзей, делиться своим местоположением,
просматривать местоположение своих друзей, устраивать встречи и приятно проводить
время вместе.

## <a id="stack"></a> Стек технологий

* Python 3.11
* Django 4.1
* Django REST framework 3.14
* python-dotenv 0.21.1
* django-filter 22.1
* PostgreSQL 13.0
* Docker

## <a id="features"></a> Особенности

* Поиск и добавление новых друзей
* Просмотр местоположения ваших друзей
* Приглашение новых друзей
* Подтверждение запросов на добавление в друзья
* Удаление пользователей из списка друзей
* Администрирование учетных записей

## <a id="settings"></a> Настройки

Все возможные настройки приложения указаны в файле .env.template.
Этот файл содержит шаблон для переменных окружения,
которые можно настроить согласно требованиям вашей установки.

# <a id="howto-remote"></a> Руководство для запуска на удаленном сервере

### Шаг 1: Клонирование репозиториев

Создайте новую директорию. Откройте терминал на вашем локальном
компьютере и клонируйте рабочие репозитории для бекенда и фронтенда:

```
git clone https://github.com/friends-locator/backend.git
git clone https://github.com/friends-locator/frontend.git
```

### Шаг 2: Установка на сервере Docker, Docker Compose:

```
sudo apt install curl 
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt-get install docker-compose-plugin
```

### Шаг 3: Создание тома базы данных

Это приложение использует внешний том для базы данных,
поэтому перед началом работы вы должны создать этот том:

```
docker volume create --name=pg_volume
```

### Шаг 4: Копирование необходимых файлов

Перейдите в папку infra вашего проекта backend:

```
cd backend/infra/
```

Скопируйте папку infra на удаленный сервер любым
удобным вам способом, например через scp:

```
scp -r infra username@IP:infra   # username - имя пользователя на сервере
                                 # IP - публичный IP сервера
```

### Шаг 5: Запустите сервер

Запустите команду:

```
docker-compose up -d
```

### Шаг 6: Первоначальная настройка

После успешной сборки не забудьте выполнить миграции, создать учетную запись администратора
и заполнить статистику.

Выполнить миграции:

```
sudo docker-compose exec backend python manage.py migrate
```

Создать суперпользователя:

```
sudo docker compose exec backend python manage.py createsuperuser
```

Собрать статику:

```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

# <a id="howto-dev"></a> Руководство для разработчиков <a name="dev_guide"></a>

Это руководство поможет вам быстро начать работу с проектом "Friends Locator".
Следуйте этим шагам, чтобы настроить окружение разработки:

### Шаг 1: Клонирование репозиториев

Создайте новую директорию. Откройте терминал на вашем локальном
компьютере и клонируйте рабочие репозитории для бекенда и фронтенда:

```
git clone https://github.com/friends-locator/backend.git
git clone https://github.com/friends-locator/frontend.git
```

### Шаг 2: Изменение адреса API

Вам необходимо изменить адрес API для фронтенда для взаимодействия с локальным сервером.
Откройте файл frontend/src/constants/apiTemplate.js и замените строку:

```
const BASE_URL = 'https://flap.acceleratorpracticum.ru/api/v1';
```

на

```
const BASE_URL = 'http://localhost/api/v1';
```

### Шаг 3: Сборка Docker контейнеров

Перейдите в директорию infra-dev в бекенд-репозитории:

```
cd backend/infra-dev
```

Скопируйте .env.template в .env

```
cp .env.template .env
```

Запустите сборку с помощью Docker Compose:

```
docker-compose up -d --build
```

### Шаг 4: Миграции и создание учетной записи администратора

Перейдите в корневую директорию бекенд репозитория.
Теперь выполните миграции базы данных и создайте учетную запись администратора:

```
python manage.py migrate
python manage.py createsuperuser
```

### Шаг 5: Сборка статики

Соберите статику с помощью следующей команды:

```
python manage.py collectstatic --noinput
```

### Шаг 6: Создание папки для медиафайлов

Создайте папку для хранения медиафайлов:

```
mkdir media
```

### Шаг 7: Настройка почтового шлюза

Для разработки используйте console.EmailBackend, для этого в настройках
settings.py раскомментируйте строку EMAIL_BACKEND:

```
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

и закомментируйте строку:

```
EMAIL_BACKEND = "elasticemailbackend.backend.ElasticEmailBackend"
```

В итоге должно получиться так:

```
#EMAIL_BACKEND = "elasticemailbackend.backend.ElasticEmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### Шаг 8: Запуск сервера

```
python manage.py runserver
```

Готово! Вы успешно настроили окружение разработки. Теперь вы можете приступить
к разработке. Сайт будет доступен по адресу: http://localhost/

## <a id="authors"></a> Авторы:

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

Smirnov Alexey
https://github.com/AxelVonReems

Lashkin Sergey
https://github.com/lashkinse
