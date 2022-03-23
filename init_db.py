import os
import psycopg2
from werkzeug.security import generate_password_hash

conn = psycopg2.connect(
    host="localhost",
    database="alar",
    user='my_user',
    password='pass')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS member;')
cur.execute('DROP TABLE IF EXISTS permission;')

cur.execute('CREATE TABLE permission (id serial PRIMARY KEY,'
            'name varchar (50) NOT NULL)')


cur.execute('CREATE TABLE member (id serial PRIMARY KEY,'
            'name varchar (50) NOT NULL,'
            'psw_hash varchar (500) NOT NULL,'
            'permission_id INT,'
            'CONSTRAINT fk_permission '
                'FOREIGN KEY(permission_id)'
                    'REFERENCES permission(id))'
            )

# Insert data into the table

cur.execute("INSERT INTO permission (name)"
            "VALUES ('Редактирование')")

cur.execute("INSERT INTO permission (name)"
            "VALUES ('Просмотр')")

cur.execute(f"INSERT INTO member (name, psw_hash, permission_id) "
            f"VALUES ('User', '{generate_password_hash('password')}', 1)")

conn.commit()

cur.close()
conn.close()
