import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    submit = SubmitField("Войти")


class DeleteForm(FlaskForm):
    name = StringField("Имя: ")
    submit = SubmitField("Удалить")


class AddForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    permission_id = IntegerField("Доступ(1 - редактирование, 2 - просмотр)")
    submit = SubmitField("Добавить")


class ChooseForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired()])
    submit = SubmitField("Выбрать для редактирования")


class EditForm(FlaskForm):
    name = StringField("Имя: ")
    password = StringField("Пароль: ")
    permission_id = IntegerField("Доступ(1 - редактирование, 2 - просмотр)")
    submit = SubmitField("Редактировать")
