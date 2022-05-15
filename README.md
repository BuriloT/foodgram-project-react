# Foodgram

## Продуктовый помощник

> На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

> Через интерфейс Foodgram_api смогут работать мобильное приложение или чат-бот;
через него же можно будет передавать данные в любое приложение.

## Технологии проекта

- Python — высокоуровневый язык программирования.
- PostgreSQL — объектно-реляционная система управления базами данных.
- Foodgram это Django-проект, что позволило подключить библиотеку DRF.
- Для обмена данными в API применяется формат JSON.
- Для автоматизации развёртывания ПО был использован Docker.

## Как запустить приложение в контейнере:

В директории создайте файл .env с переменными окружения для работы с базой данных:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=#имя базы данных
POSTGRES_USER=#логин для подключения к базе данных
POSTGRES_PASSWORD=# пароль для подключения к БД
DB_HOST=название сервиса (контейнера)
DB_PORT=порт для подключения к БД
```

Выполнить команду:
```
docker-compose up
```
Произвести миграции:
```
docker-compose exec backend python manage.py migrate
```
Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
Собрать статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Загрузить ингредиенты в базу данных:
```
docker-compose exec backend python manage.py csv_import
```

## Документация к проекту.

После запуска приложения документация доступна по адресу:

```
http://localhost/api/docs/
```

## Некоторые примеры запросов к API.

Регистрация пользователя.

```
POST /api/users/
```

REQUEST:

```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```

Создание рецепта. Доступно только авторизованному пользователю.

```
POST /api/recipes/
```

REQUEST:

```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

Подписка на пользователя. Доступно только авторизованным пользователям.

```
POST /api/users/{id}/subscribe/
```

REQUEST:

```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```

