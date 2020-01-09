from flask import abort, Blueprint, render_template, current_app, flash, redirect, request, url_for
from flask_login import current_user, login_required


from webapp.db import db
from webapp.news.forms import CommentForm
from webapp.news.models import News, Comment
from webapp.weather import weather_by_city
from webapp.utils import get_redirect_target

blueprint = Blueprint('news', __name__)

# Так называемый декоратор, / - url означает корень сайта
@blueprint.route('/')
def index():
    title = 'Вести Богучар'
    w_Moscow = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    # Верни нам все новости из БД, упорядочим по дате order_by(News.published.desc()
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()
    print(news_list)
    return render_template('news/index.html', page_title=title, weather=w_Moscow, news_list=news_list)

@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()
    if not my_news:
        abort(404)
    comment_form = CommentForm(news_id=my_news.id)
    return render_template('news/single_news.html', page_title=my_news.title, news=my_news, comment_form=comment_form)

@blueprint.route('/news/comment', methods=['POST'])
@login_required  # Защита от неавторизованных комментаторов
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment_text.data, news_id=form.news_id.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash("Комментарий успешно дабавлен")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Ошибка в поле {}: - {}".format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())

# request.referer redirect(request.referer)
