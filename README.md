
- данные хранятся в Elasticsearch
- API для обращения к базе данных на FastAPI с учетом параметров фильтрации и сортировки
- ответы ручек, запрошенных с одинаковыми параметрами, кешируются в Redis
- работа с внешними сервисами реализована через exponential backoff
- реализованы тесты на pytest


Проект состоит из двух приложений. 
   1. ETL и Admin Panel распологается по адресу https://github.com/DmitryShinkarev/new_admin_panel_sprint_3
   2. Второе Fast API в текущем репозитории https://github.com/vadim-miroshnik/FastAPI_MovieTheater_API

# Запуск проекта 
   1. Создать сеть для docker
       `docker network create --driver bridge app_movies_net`

   2. Клонировать и разверуть в соответствие с вложенной инструкцией первую часть

   3. Клонировать и запустить текущий проект
   `docker-compose up -d --build`
