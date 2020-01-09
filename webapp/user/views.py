from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user # Отвечает за авторизацию пользователей

from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users') # Все URLы в этом блюпринте будут начинаться с /users


@blueprint.route('/login')  # Добавляем роут который будет отображать нашу форму
def login():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
    title = 'Авторизация'
    login_form = LoginForm()  # Создаем экземпляр нашего класса
    return render_template('user/login.html', page_title=title,
                           form=login_form)  # Берет шаблон, подставляет туда данные и отображает


@blueprint.route('/process-login', methods=['POST'])  # Реализуем обработку формы логина
def process_login():
    form = LoginForm()

    if form.validate_on_submit(): # Если нам пришли данные формы и они валидируются
        user = User.query.filter(User.username == form.username.data).first() # можем запросить такого пользователя из БД
        if user and user.check_password(form.password.data): # Если такой пользователь есть и пароль правильный(проверелся)
            # rmember=form.remember_me.data - если пользователь был запомнин (в кукис)
            login_user(user, remember=form.remember_me.data)  # Залогиниваем этого пользователя при помощи волшебной функции (запоминаем пользователя)
            flash('Вы успешно вошли на сайт!')  # Оповещаем
            return redirect(get_redirect_target())  # Делаем редирект на главную страницу

    flash('Неправильное имя или пароль!')  # Покажет если не прошло
    return redirect(url_for('user.login'))  # И перенаправит на страницу логина


@blueprint.route('/logout')
def logout(): # Если пользователь зашел на логаут
    logout_user() # Делаем логаут
    flash('Вы успешно разлогинились')  # Выводим сообщение
    return redirect(url_for('news.index'))  # Перенаправляем


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))  # Если пользователь авторизован - на главную
    title = 'Регистрация'
    form = RegistrationForm()  # Создаем экземпляр нашего класса
    return render_template('user/registration.html', page_title=title,
                           form=form)  # Берет шаблон, подставляет туда данные и отображает


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, role='user', email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Ошибка в поле {}: - {}".format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.register'))

