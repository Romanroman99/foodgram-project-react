# Для ревью:
Адрес сервера:
[http://158.160.32.16/](http://158.160.32.16/)

* Логин:
```bash
admin@mail.ru
```
* Пароль:
```bash
admin
```

# Foodgram - Продуктовый помощник
![Foodgram workflow](https://github.com/Edw125/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)  

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Описание и функционал проекта
Foodgram - Сервис для публикации рецептов. Пользователи могут публикавать свои рецепты, просматривать рецепты 
других пользователей, добовлять рецпты в Избранное, подписываться на публикации авторов, добовлять рецепты в 
список покупок и скачивать PDF список продуктов.


## Запуск проекта в Docker контейнере
* Установите Docker

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker compose:
```bash
docker-compose up -d --build
```  

  > После сборки появятся 4 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложений **frontend**
  > 3. контейнер приложения **backend**
  > 4. контейнер web-сервера **nginx**

* Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
* Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```
* Команда для остановки докера:
```bash
docker-compose down
```

* Чтобы залить в базу данные, введите команды:
```bash
docker-compose exec backend python manage.py load_csv_data --ingredients
```
Готово! 

## Авторы
https://github.com/Romanroman99 -   Бэкенд и деплой сервиса Foodgram

https://github.com/yandex-praktikum - Фронтенд сервиса Foodgram
