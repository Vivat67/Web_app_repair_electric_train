from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user


from main import app, db
from models import Users, Articles, Repair_information


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/articles')
@login_required
def content():
    articles = Articles.query.all()
    return render_template('articles.html', articles=articles)


@app.route('/article/<int:article_id>')
@login_required
def article(article_id):
    article = Articles.query.filter_by(id=article_id).first()
    return render_template('article.html', article=article)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
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
        new_user = Users(
            name=name,
            surname=surname,
            password=password,
            post=post
            )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login')), flash(
                                {'title': "Успех",
                                 'message': "Вы зарегестрировались"}, 'success'
                                 )

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        password = request.form.get('password')
        if name and password and surname:
            user = Users.query.filter_by(name=name, surname=surname).first()

            if user and user.password == password:
                login_user(user)

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


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response


@app.route('/repair_information', methods=['GET', 'POST'])
def repair_information():
    if request.method == 'GET':
        return render_template('repair_inf.html')
    name = request.form.get('name')
    surname = request.form.get('surname')
    train = request.form.get('train')
    defect = request.form.get('defect')
    s_def = request.form.get('sub_defect')
    b_inf = request.form.get('brief_information')
    date = request.form.get('date')
    if name and surname and train and defect and s_def and b_inf and date:
        new_repair_information = Repair_information(
            executer=name + ' ' + surname,
            train=train,
            defect=defect,
            subspecies_defect=s_def,
            brief_information=b_inf,
            date=date
            )
        db.session.add(new_repair_information)
        db.session.commit()
        return redirect(url_for('index')), flash(
                                {'title': "Успех",
                                 'message': "Запись добавлена"}, 'success'
                                 )
    else:
        flash(
                {'title': "Ошибка",
                    'message': "Заполните все поля"}, 'error')
    return render_template('repair_inf.html')
