## Установка окружения
### pip install -r requirements.txt
### Подключение окружения
#### source venv/bin/activate
## Запуск бд:
#### sudo -iu postgres psql
#### CREATE DATABASE alar;
#### CREATE USER user WITH PASSWORD 'pass';
#### GRANT ALL PRIVILEGES ON DATABASE alar TO my_user;
#### Просто чтобы выйти из psql: 
#### \q
#### Создание таблиц:
#### python init_db
#### Создается две таблицы member и permission
## Запуск приложения:
#### python app.py
#### После этого входим как User:password и добавляем/удаляем/редактируем 
#### пользователей, но  НЕ НАДО менять доступ пользователю User, если
#### нет других пользователей с правами редактирования, иначе больше
#### нельзя будет ничего поменять