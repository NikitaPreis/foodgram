# Foodgram
### Описание:

«Фудграм» — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также будет доступен сервис «Список покупок». Он позволит формировать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Стек технологий:

* Python
* Django
* Django REST framework
* PostgreSQL
* Gunicorn
* Nginx
* Docker

### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:NikitaPreis/foodgram.git
```

Перейдите в корень проекта
```
cd foodgram
```

Запустите Docker на вашем пк и введите в терминал команду для запуска Docker Compose:
```
docker compose -f docker-compose.production.yml up
```

В новом терминале соберите статические файлы:
```
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

Примините миграции:
```
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

##Проект будет доступен по адресу:
*http://localhost:10000*

### Памятка
1. Добавить новые теги и ингредиенты можно через админку.
2. После добавления рецептов, учтите что frontend приложения по умолчанию фильтрует записи по всем тегам. *Для того, чтобы увидеть все добавленные рецепты, отключите теги, кликнув по каждому из них.*


### Автор:
Никита Кузнецов
