from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db


class User(db.Model, UserMixin):  # Множественное наследование класса, берет и из db.Model и из UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True) # Те колонки по которым буем часто искать помечаем unique=True - будет быстрее
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))

    def set_password(self, password): # Заменяет пароль на хеш пароля перед записью в БД
        self.password = generate_password_hash(password)

    def check_password(self, password): # Сверяем хеш из базы с хешем получиным от введенного пароля. Получим Тру или Фолс.
        return check_password_hash(self.password, password)

    @property # Декоратор. Помогает методу вести себя как атрибут
    def is_admin(self): # можно вызывать без скобочек
        return self.role == 'admin'

    def __repr__(self):
        return '<User name: {}, id: {}>'.format(self.username, self.id) # Что бы выводить имя пользователя в формате