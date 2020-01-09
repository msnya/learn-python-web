from datetime import datetime, date, time, timedelta
import locale
import platform
import pymorphy2

from bs4 import BeautifulSoup

from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news


# Тут зададим региональный параметр для любой ОС
if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')


def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегдня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    try:
        m = pymorphy2.MorphAnalyzer()
        day, month, year, qw2ewq, qwe2eewq = date_str.split(' ')
        # преобразуем название месяца в именительный падеж с заглавной буквы
        new_month = m.parse(month)[0].inflect({'nomn'}).word.title()
        return datetime.strptime(' '.join([day, new_month, year]), '%d %B %Y')
    except ValueError:
        return datetime.now()


def get_news_snippets():
    html = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html:
        soup = BeautifulSoup(html, 'html.parser') # Бреобразует наш HTML в дерево элементов с которым удобнее работать фунциям этой библиотеки
        all_news = soup.find("ul", class_="content-list_posts").findAll('li', class_='content-list__item_post') # Делаем выборку элементов страницы при помощи поиска
        #result_news = []
        for news in all_news:
            title = news.find('a', class_="post__title_link").text  # Выбираем текст заголовка
            url = news.find('a', class_="post__title_link")["href"]  # Выбираем ссылку заголовка (к атрибутам обращаемся как к элементам славаря)
            published = news.find('span', class_="post__time").text  # Выбираем время
            published = parse_habr_date(published)
            save_news(title, url, published) # После формирования, вызываем запись в базу


def get_news_content():
    news_without_texh = News.query.filter(News.text.is_(None))
    for news in news_without_texh:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # .decode_contents() позволяет получить html вместо текста
            article = soup.find('div', class_='post__text-html').decode_contents()
            if article:
                news.text = article
                db.session.add(news)
                db.session.commit()
