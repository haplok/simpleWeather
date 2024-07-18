Прототип web приложения в котором пользователь вводит название города
и получает прогноз погоды на 7 дней(
диапазон температур, количество осадков, скорость ветра)

Внизу страницы отображается последний город, который искал пользователь
Так же выпадает меню автозаполнения ранее введенных городов

* язык: **Python 3.11**

* фреймворки и библиотеки: **Django, djangorestframework, requests**
* api для погоды: https://open-meteo.com/
* DB: **SQLite3**(Django ORM)

для создания контейнера:
`docker build -t simpleweather .`

для запуска приложения через докер:
`docker run -it -p 8000:8000 -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_PASSWORD=password -e DJANGO_SUPERUSER_E
MAIL=admin@example.com simpleweather`

Так же есть:
* тесты
* докер
* автодополнение
* API: ` /api/city-query-count/`
