"""
Модуль содержит функции представления для шаблонов.
"""

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, logout_user

from logger import logger
from main import app
from models import DataAccess

# обьект для взаимодействия с базой данных.
dataAccess = DataAccess()


@logger.catch
@app.route('/')
def index():
    """
    Обработчик для главной страницы.

    Returns:
        str: HTML-код главной страницы.
    """
    return render_template('index.html')


@logger.catch
@app.route('/articles')
@login_required
def content():
    """
    Обработчик для страницы со списком статей.

    Returns:
        str: HTML-код страницы со списком статей.
    """
    articles = dataAccess.get_articles()
    return render_template('articles.html', articles=articles)


@logger.catch
@app.route('/article/<int:article_id>')
@login_required
def article(article_id: int) -> object:
    """
    Обработчик для страницы со списком статей.

    Args:
        article_id (int): идентификатор статьи.

    Returns:
        str: HTML-код страницы со списком статей.
        articles: обьект статьи.
    """
    article = dataAccess.get_article(article_id)
    return render_template('article.html', article=article)


@logger.catch
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Обработчик для страницы регистрации пользователей.
    При удачной регистрации перенаправляет на авторизацию.

    Returns:
        str: HTML-код страницы регистрации.
    """
    if request.method == 'GET':
        return render_template('register.html')
    name = request.form.get('name')
    surname = request.form.get('surname')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    post = request.form.get('post')
    if not (name and surname and password and password2 and post):
        flash(
            {'title': "Ошибка",
                'message': "Заполните все поля"}, 'error')
    elif password != password2:
        flash(
            {'title': "Ошибка",
                'message': "Пароли не совпадают"}, 'error')
    else:
        dataAccess.add_user(name, surname, password, post)
        return redirect(url_for('login')), flash(
                                {'title': "Успех",
                                 'message': "Вы зарегестрировались"}, 'success'
                                 )

    return render_template('register.html')


@logger.catch
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обработчик для страницы входа в систему.

    Returns:
        str: HTML-код страницы входа в систему.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        password = request.form.get('password')
        if name and password and surname:
            if dataAccess.get_user(name, surname, password):
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash(
                    {'title': "Ошибка",
                     'message': "Имя, фамилия или пароль не верны"}, 'error')
        else:
            flash(
                    {'title': "Ошибка",
                        'message': "Заполните все поля"}, 'error')
    return render_template('login.html')


@logger.catch
@app.route('/logout')
@login_required
def logout():
    """
    Обработчик для выхода пользователя из системы.

    Returns:
        str: Перенаправление на главную страницу.
    """
    logout_user()
    return redirect(url_for('index'))


@logger.catch
@app.after_request
def redirect_to_sign(response):
    """
    Перенаправление на страницу входа в систему при отказе в доступе.

    Args:
        response: Ответ сервера.

    Returns:
        str: Перенаправление на страницу входа в систему при отказе в доступе.
    """
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response


@logger.catch
@app.route('/repair_information', methods=['GET', 'POST'])
@login_required
def repair_information():
    """
    Обработчик для страницы информации о ремонтах.

    Returns:
        str: HTML-код страницы информации о ремонтах.
        trains: список обьектов поездов.
    """
    trains = dataAccess.get_trains()
    if request.method == 'GET':
        return render_template('repair_inf.html', trains=trains)
    name = request.form.get('name')
    surname = request.form.get('surname')
    train = request.form.get('train')
    defect = request.form.get('defect')
    s_def = request.form.get('sub_defect')
    b_inf = request.form.get('brief_information')
    date = request.form.get('date')
    if name and surname and train and defect and s_def and b_inf and date:
        dataAccess.add_repair_inf(name, surname, train,
                                  defect, s_def, b_inf, date)
        flash(
                                {'title': "Успех",
                                 'message': "Запись добавлена"}, 'success'
                                 )
        return render_template('repair_inf.html', trains=trains)
    flash(
            {'title': "Ошибка",
                'message': "Заполните все поля"}, 'error')
    return render_template('repair_inf.html', trains=trains)


@logger.catch
@app.route('/repair_history', methods=['GET', 'POST'])
@login_required
def repair_history():
    """
    Обработчик для страницы истории ремонтов.

    Returns:
        str: HTML-код страницы истории ремонтов.
        trains: список обьектов поездов.
    """
    trains = dataAccess.get_trains()
    return render_template('repair_history.html', trains=trains)


@logger.catch
@app.route('/repair_history_continion', methods=['GET', 'POST'])
@login_required
def repair_history_continion():
    """
    Обработчик для страницы фильтрации истории ремонтов.

    Returns:
        str: HTML-код страницы фильтрации истории ремонтов.
        repair_inf: список обьектов истории ремонта поездов.
    """
    train = request.form['train']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if start_date and end_date:
        repair_inf = dataAccess.get_repair_inf_with_date(
            train, start_date, end_date)
    else:
        repair_inf = dataAccess.get_repair_inf(train)

    return render_template(
        'repair_history_continion.html',
        repair_inf=repair_inf
        )


@logger.catch
@app.route('/diagnostics/<defect>')
@login_required
def diagnostics(defect: str):
    """
    Обработчик для страницы диагностики.

    Args:
        defect (str): Неисправность.

    Returns:
        str: HTML-код страницы диагностики.
        all_sub_defects: список обьектов неисправностей.
    """
    all_sub_defects = dataAccess.get_all_sub_defets(defect)
    return render_template('diagnostics.html', all_sub_defects=all_sub_defects)


@logger.catch
@app.route('/sub_defect/<int:sub_id>')
@login_required
def diagnostics_sub_defect(sub_id):
    """
    Обработчик для страницы подробной информации о разновидности неисправности.

    Args:
        sub_id (int): идентификатор разновидности неисправности.

    Returns:
        str: HTML-код страницы подробной информации
        о разновидности неисправности.
        sub_defect: обьект описания неисправности.
    """
    sub_defect = dataAccess.get_sub_defet(sub_id)
    return render_template('sub_defect.html', sub_defect=sub_defect)
