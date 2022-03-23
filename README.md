## Подключение окружения
###### *source venv/bin/activate*
## Установка окружения
###### *pip install -r requirements.txt*
## Запуск бд:
###### *sudo -iu postgres psql*
###### *CREATE DATABASE alar;*
###### *CREATE USER user WITH PASSWORD 'pass';*
###### *GRANT ALL PRIVILEGES ON DATABASE alar TO my_user;*
###### *pip install -r requirements.txt*
## Запуск бд:
###### *sudo -iu postgres psql*
###### *CREATE DATABASE alar;*
###### *CREATE USER my_user WITH PASSWORD 'pass';*
###### *GRANT ALL PRIVILEGES ON DATABASE alar TO my_user;*
#### Просто чтобы выйти из psql: 
###### *\q*
#### Создание таблиц:
###### *python init_db*
###### *python init_db.py*
#### Создается две таблицы member и permission
## Запуск приложения:
###### *python app.py*
##### После этого входим как User:password и добавляем/удаляем/редактируем 
##### пользователей, но  НЕ НАДО менять доступ пользователю User, если
##### нет других пользователей с правами редактирования, иначе больше
##### нельзя будет ничего поменять
## Запуск асинхронной части
### Сначала надо запустить сервер
###### *python app.py*
### Затем запуск модуля асинхронных запросов
###### *python async_request.py* 
#### Данные идут из функций arr1, arr2, arr3 в модуле app.py 