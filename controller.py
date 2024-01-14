"""
Модуль содержит функции представления для шаблонов.
"""

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, logout_user

from logger import logger
from main import app
from models import DataAccess, Articles, Defects


# обьект для взаимодействия с базой данных.
dataAccess = DataAccess()


@logger.catch
@app.route('/')
def index() -> str:
    """
    Обработчик для главной страницы.

    Returns:
        str: HTML-код главной страницы.
    """
    return render_template('index.html')


@logger.catch
@app.route('/articles')
@login_required
def content() -> tuple[str, list]:
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
def article(article_id: int) -> tuple[str, Articles]:
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
def registration() -> str:
    """
    Обработчик для страницы регистрации пользователей.
    При удачной регистрации перенаправляет на авторизацию.

    Returns:
        str: HTML-код страницы регистрации.
    """
    if request.method == 'GET':
        return render_template('register.html')
    forms = dict(request.form)
    if check_all_fields_are_filled_in(forms, 5):
        flash(
            {'title': "Ошибка",
                'message': "Заполните все поля"}, 'error')
    elif forms['password'] != forms['password2']:
        flash(
            {'title': "Ошибка",
                'message': "Пароли не совпадают"}, 'error')
    else:
        dataAccess.add_user(**forms)
        return redirect(url_for('login')), flash(
                                {'title': "Успех",
                                 'message': "Вы зарегестрировались"}, 'success'
                                 )

    return render_template('register.html')


@logger.catch
@app.route('/login', methods=['GET', 'POST'])
def login() -> str:
    """
    Обработчик для страницы входа в систему.

    Returns:
        str: HTML-код страницы входа в систему.
    """
    if request.method == 'GET':
        return render_template('login.html')
    forms = dict(request.form)
    if check_all_fields_are_filled_in(forms, 3):
        flash(
                {'title': "Ошибка",
                    'message': "Заполните все поля"}, 'error')
        return render_template('login.html')
    if dataAccess.get_user(**forms):
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    else:
        flash(
            {'title': "Ошибка",
                'message': "Имя, фамилия или пароль не верны"}, 'error')
        return render_template('login.html')


@logger.catch
@app.route('/logout')
@login_required
def logout() -> str:
    """
    Обработчик для выхода пользователя из системы.

    Returns:
        str: Перенаправление на главную страницу.
    """
    logout_user()
    return redirect(url_for('index'))


@logger.catch
@app.after_request
def redirect_to_sign(response) -> str:
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
def repair_information() -> tuple[str, list]:
    """
    Обработчик для страницы информации о ремонтах.

    Returns:
        str: HTML-код страницы информации о ремонтах.
        trains: список обьектов поездов.
    """
    trains = dataAccess.get_trains()
    if request.method == 'GET':
        return render_template('repair_inf.html', trains=trains)
    forms = dict(request.form)
    if check_all_fields_are_filled_in(forms, 7):
        flash(
                {'title': "Ошибка",
                    'message': "Заполните все поля"}, 'error')
        return render_template('repair_inf.html', trains=trains)
    dataAccess.add_repair_inf(**forms)
    flash(
                            {'title': "Успех",
                                'message': "Запись добавлена"}, 'success'
                                )
    return render_template('repair_inf.html', trains=trains)


@logger.catch
@app.route('/repair_history', methods=['GET', 'POST'])
@login_required
def repair_history() -> tuple[str, list]:
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
def repair_history_continion() -> tuple[str, list]:
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
def diagnostics(defect: str) -> tuple[str, list]:
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
def diagnostics_sub_defect(sub_id: int) -> tuple[str, Defects]:
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


def check_all_fields_are_filled_in(forms: dict, fields: int) -> bool:
    """
    Функция проверяет что все поля формы заполнены.

    Args:
        forms: словарь, хранит значения, введенные в полях.
        fields: колличество полей.

    Returns:
        bool: True - есть пустые поля.
              False - все поля заполнены.

    """
    all_field = len(list(filter(lambda x: x != '', forms.values())))
    if all_field != fields:
        return True
    return False
