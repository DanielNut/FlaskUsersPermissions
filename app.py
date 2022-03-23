import json
import time
import asyncio

import flask.app
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from shared.models import db
from flask_seeder import FlaskSeeder

from models.member import Member
from models.permission import Permission
from shared.forms import LoginForm, DeleteForm, AddForm, ChooseForm, EditForm


def create_app(db):
    application = Flask(__name__)

    application.config['SECRET_KEY'] = 'wjabdn91dy187b91db91dbs9dand918'
    application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_user:pass@localhost/alar'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = application
    db.init_app(application)

    seeder = FlaskSeeder()
    seeder.init_app(application, db)

    return application


app = create_app(db)

menu = [{"name": "О сайте", "url": "/about"},
        {"name": "Просмотр", "url": "/user-list"},
        {"name": "Войти", "url": "/login"},
        {"name": "Выйти", "url": "/logout"}]


redact = [{"name": "Добавить", "action": "add"},
          {"name": "Удалить", "action": "delete"},
          {"name": "Редактировать", "action": "choose"}]


@app.route("/")
def index():
    return render_template('index.html', menu=menu, title='Основная страница')


@app.route("/about")
def about():
    return render_template('about.html', menu=menu, title='О сайте')


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('userList', username=session['userLogged']))

    form = LoginForm()

    if form.validate_on_submit():
        user_name = form.name.data
        user = Member.query.filter_by(name=user_name).first()
        if user:
            if user.check_password(form.password.data):
                session['userLogged'] = user_name
                session['permission'] = user.permission_id
                return redirect(url_for('userListRedirect'))
            else:
                flash('Неверный пароль', category='error')
        else:
            flash('Такого пользователя нет', category='error')

    return render_template("login.html", menu=menu, title="Авторизация", form=form)


@app.route("/logout")
def logout():
    if 'userLogged' in session:
        session.pop('userLogged')
        session.pop('permission')
    return redirect(url_for('login'))


@app.route("/user-list")
def userListRedirect():
    if 'userLogged' not in session:
        abort(401)
    return redirect(url_for('userList', username=session['userLogged'], action='view'))


@app.route("/user-list/<username>")
def userList(username):
    if 'userLogged' not in session:
        abort(401)

    is_redactor = True if session['permission'] == 1 else False

    # SHOW MEMBERS
    members = get_members(db)

    return render_template('user-list.html', menu=menu, title='Список пользователей', username=username,
                           members=members, is_redactor=is_redactor, redact=redact)


@app.route("/user-list/<username>/<action>", methods=["POST", "GET"])
def userListAction(username, action):
    user = Member.query.filter_by(name=username).first()
    members = get_members(db)
    if user.permission_id == 1 and action != 'view':
        if action == 'view':
            return redirect(url_for('userList', username=username, action='view'))
        if action == 'choose':
            form_choose = ChooseForm()
            if form_choose.validate_on_submit():
                edit_user_name = form_choose.name.data
                user_to_edit = Member.query.filter_by(name=edit_user_name).first()
                if user_to_edit:
                    return redirect(url_for('userEdit', username=username, edit_user_name=edit_user_name))
                else:
                    flash('Такого пользователя нет', category='error')
            return render_template('user-list-edit.html', menu=menu, username=username, action=action,
                                   form=form_choose, members=members, redact=redact, is_redactor=True)
        elif action == 'add':
            form_add = AddForm()
            if form_add.validate_on_submit():
                user_to_add = Member(name=form_add.name.data, permission_id=form_add.permission_id.data)
                user_to_add.set_password(form_add.password.data)
                add_user(user_to_add, db)
                return redirect(url_for('userList', username=username, action='view'))
            return render_template('user-list-edit.html', menu=menu, username=username, action=action,
                                   form=form_add, members=members, redact=redact, is_redactor=True)
        elif action == 'delete':
            form_delete = DeleteForm()
            if form_delete.validate_on_submit():
                user_to_delete = Member.query.filter_by(name=form_delete.name.data).first()
                delete_user(user_to_delete, db)
                return redirect(url_for('userList', username=username, action='view'))
            return render_template('user-list-edit.html', menu=menu, username=username, action=action, form=form_delete,
                                   members=members, redact=redact, is_redactor=True)
    return redirect(url_for('userList', username=username, action='view'))


@app.route("/user-list/<username>/edit/<edit_user_name>", methods=["POST", "GET"])
def userEdit(username, edit_user_name):
    user = Member.query.filter_by(name=username).first()
    user_to_edit = Member.query.filter_by(name=edit_user_name).first()
    members = get_members(db)
    if user.permission_id == 1:
        form_edit = EditForm()
        if form_edit.validate_on_submit():
            user_to_edit.name = form_edit.name.data
            user_to_edit.set_password(form_edit.password.data)
            user_to_edit.permission_id = form_edit.permission_id.data
            db.session.commit()
            return redirect(url_for('userList', username=username, action='view'))
        return render_template('user-list-edit.html', menu=menu, username=username, action='edit',
                               form=form_edit, members=members, redact=redact, is_redactor=True,
                               edit_user_name=edit_user_name)
    return redirect(url_for('userList', username=username, action='view'))


@app.errorhandler(401)
def unauthorized(error):
    return render_template('page401.html', title='Нет авторизации', menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu)


def delete_user(user, db):
    db.session.delete(user)
    db.session.commit()


def add_user(user, db):
    db.session.add(user)
    db.session.commit()


def get_members(db):
    members = db.session.execute("select m.name as name, p.name as permission"
                                 " from member m, permission p where p.id=m.permission_id;")
    db.session.commit()
    members_dict = {}
    for m in members:
        members_dict[m[0]] = m[1]
    return members_dict


@app.route('/array1')
def arr1():
    arr = []
    for i in range(1, 11):
        x = {"id": f"{i}", "name": f"Test {i}"}
        arr.append(x)
    for i in range(31, 41):
        x = {"id": f"{i}", "name": f"Test {i}"}
        arr.append(x)
    return json.dumps(arr)


@app.route('/array2')
def arr2():
    arr = []
    for i in range(11, 21):
        x = {"id": f"{i}", "name": f"Test {i}"}
        arr.append(x)
    for i in range(41, 51):
        x = {"id": f"{i}", "name": f"Test {i}"}
        arr.append(x)
    return json.dumps(arr)


@app.route('/array3')
def arr3():
    time.sleep(3)
    arr = []
    for i in range(21, 31):
        x = {"id": f"{i}", "name": f"Test {i}"}
        arr.append(x)
    for i in range(51, 61):
        x = {"id": f"{i}", "name": f"Test {i}"}
        arr.append(x)
    return json.dumps(arr)


if __name__ == '__main__':
    app.run(debug=True)
