from datetime import datetime
from sqlalchemy.orm import relationship

from webapp.db import db


# Создаем модель БД - это ласс который наследуется от db.model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False) # String - короткая строка, nullable=False - данные не могут отсутствовать
    url = db.Column(db.String, unique=True, nullable=False) # nullable=False - данные не могут отсутствовать, unique=True - каждая ссылка уникальна
    published = db.Column(db.DateTime, nullable=False) # nullable=False - данные не могут отсутствовать
    text = db.Column(db.Text,  nullable=True) # Text - длинная строка

    # Подсчет количества комментариев
    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()

    def __repr__(self): # Магическая хуйня/ salf указывает что обращаться будем к конкретному объекту класса(каждая новость)
        return '<News {} {}>'.format(self.title, self.url)


# onedelete='CDACADE' - удаляет связанные объекты из бд
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    # Сваяжем поля Комент через новость и пользователя
    news = relationship('News', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self): # Магическая хуйня/ salf указывает что обращаться будем к конкретному объекту класса
        return '<Comment {}>'.format(self.id)

