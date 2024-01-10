from flask_login import UserMixin
from main import app, manager, db
from flask_migrate import Migrate
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash

migrate = Migrate(app, db)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    password = db.Column(db.String(300))
    post = db.Column(db.String(32))

    def __repr__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Пароль: {self.password}\n'
            f'Должность: {self.post}'
            )


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train = db.Column(db.String(32), unique=True)
    location = db.Column(db.String(32))
    production = db.Column(db.Date)
    last_repair = db.Column(db.Date)

    def __repr__(self):
        return (
            f'Наименование: {self.train}\n'
            f'Расположение: {self.location}\n'
            f'Последний ремонт: {self.last_repair}'
            )


class Defects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    defect = db.Column(db.String(64))
    subspecies_defect = db.Column(db.String(100))
    repair = db.Column(db.Text)

    def __repr__(self):
        return (f'Неисправность: {self.defect}\n'
                f'Разновидность неисправности: {self.subspecies_defect}\n'
                f'Ремонт: {self.repair}'
                )


class Repair_information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    executer = db.Column(db.String(32))
    defect = db.Column(db.String(64))
    subspecies_defect = db.Column(db.Text)
    brief_information = db.Column(db.Text)
    train = db.Column(db.String(20))
    date = db.Column(db.Date)

    def __repr__(self):
        return (
            f'Иполнитель: {self.executer}\n'
            f'Неисправность: {self.defect}\n'
            f'Разновидность неисправности: {self.subspecies_defect}\n'
            f'Поезд: {self.train}\n'
            f'Дата: {self.date}'
            )


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)

    def __repr__(self):
        return (f'Статья: {self.name}')


class DataAccess:
    """
    Класс служит для извлечения данных из БД.
    """

    def get_articles(self):
        articles = Articles.query.all()
        return articles

    def get_article(self, article_id):
        article = Articles.query.filter_by(id=article_id).first()
        return article

    def add_user(self, name, surname, password, post):
        new_user = Users(
            name=name,
            surname=surname,
            password=generate_password_hash(password),
            post=post
            )
        db.session.add(new_user)
        db.session.commit()

    def get_user(self, name, surname, password):
        user = Users.query.filter_by(name=name, surname=surname).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return True

    def get_trains(self):
        trains = Train.query.all()
        return trains

    def add_repair_inf(self,
                       name,
                       surname,
                       train,
                       defect,
                       s_def,
                       b_inf,
                       date
                       ):
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

    def get_repair_inf_with_date(self, train, start_date, end_date):
        repair_inf = Repair_information.query.filter_by(
            train=train).filter(
                Repair_information.date.between(start_date, end_date)).all()
        return repair_inf

    def get_repair_inf(self, train):
        repair_inf = Repair_information.query.filter_by(train=train).all()
        return repair_inf

    def get_all_sub_defets(self, defect):
        all_sub_defect = Defects.query.filter_by(defect=defect).all()
        return all_sub_defect

    def get_sub_defet(self, sub_id):
        sub_defect = Defects.query.filter_by(id=sub_id).first()
        return sub_defect


with app.app_context():
    db.create_all()


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
