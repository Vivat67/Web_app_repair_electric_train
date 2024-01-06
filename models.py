from flask_login import UserMixin
from main import db, app, manager
from flask_migrate import Migrate

migrate = Migrate(app, db)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    password = db.Column(db.String(100))
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


with app.app_context():
    db.create_all()


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
