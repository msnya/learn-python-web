import requests

from webapp.db import db
from webapp.news.models import News


def get_html(url):
# Сделаем вид что запрос от браузера
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status() # Отлавливаем ошибку 400, 500
        return result.text # Получаем контент сраницы в виде HTML
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def save_news(title, url, published): # Функция записи новостей в базу
    # Поле News.url должно быть равно url который на входе в функцию. Тогда сработает счетчик
    news_exists = News.query.filter(News.url == url).count() # Возможность сделать выборку с фильтром из модели News
    print(news_exists)
    if not news_exists: # Если такой новости нет - добавляем
        news_news = News(title=title, url=url, published=published) # Создаем объект класса News/ id не задаем, так как он primary_key - задастся базой
        db.session.add(news_news) # Кладем в сессию алхимии
        db.session.commit() # Сохраняем в базу