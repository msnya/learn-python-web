from getpass import getpass # getpass для того что бы небыло видно вводимые символы
import sys # Модуль взаимодействия с системными функциями

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app() # Создаем апликейшн

with app.app_context(): # Запрашиваем имя
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count(): # Проверяем нет ли такого имени
        print('Пользователь с тамим именем уже существует')
        sys.exit(0)
    password1 = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')

    if not password1 == password2: # Проверяем одинаковый ли пароль
        print('Пароли не одинаковые')
        sys.exit(0)

    new_user = User(username=username, role='admin')  # Роль задаем по умолчанию админ, можно изменить
    new_user.set_password(password1) # Делаем из пароля хэш

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))
