from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required # Отвечает за авторизацию пользователей
from flask_migrate import Migrate

from webapp.db import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')  # Говорим откуда подтягивать конфигурацию
    db.init_app(app)  # Делаем это после строчки с конфигом, так как ДБ обращается к конфигу
    migrate = Migrate(app, db)  # Создаем объект аласса

    login_manager = LoginManager()  # Создаем экземпляр логин менеджера
    login_manager.init_app(app)  # Делаем инит передавая ему апликейшн
    login_manager.login_view = 'user.login'  # говорим как будет названа функция которая занимается логином пользователя (login():)

    app.register_blueprint(user_blueprint)  # Регистрируем блюпринт
    app.register_blueprint(admin_blueprint)  # Регистрируем блюпринт
    app.register_blueprint(news_blueprint)  # Регистрируем блюпринт


# Сверка id пользователя с куки
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id) # Запрос к базе данных

    return app
