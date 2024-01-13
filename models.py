"""
В данном модуле создаются метаданные для БД.
"""

from flask_login import UserMixin, login_user
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash

from logger import logger
from main import app, db, manager

migrate = Migrate(app, db)


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)


class Users(db.Model, UserMixin, BaseModel):
    """
    Табличка 'Пользователь'
    """
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    password = db.Column(db.String(300))
    post = db.Column(db.String(32))

    def __repr__(self) -> str:
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Пароль: {self.password}\n'
            f'Должность: {self.post}'
            )


class Train(db.Model, BaseModel):
    """
    Табличка 'Поезд'
    """
    train = db.Column(db.String(32), unique=True)
    location = db.Column(db.String(32))
    production = db.Column(db.Date)
    last_repair = db.Column(db.Date)

    def __repr__(self) -> str:
        return (
            f'Наименование: {self.train}\n'
            f'Расположение: {self.location}\n'
            f'Последний ремонт: {self.last_repair}'
            )


class Defects(db.Model, BaseModel):
    """
    Табличка 'Неисправности'
    """
    defect = db.Column(db.String(64))
    subspecies_defect = db.Column(db.String(100))
    repair = db.Column(db.Text)

    def __repr__(self) -> str:
        return (f'Неисправность: {self.defect}\n'
                f'Разновидность неисправности: {self.subspecies_defect}\n'
                f'Ремонт: {self.repair}'
                )


class Repair_information(db.Model, BaseModel):
    """
    Табличка 'Информация ремонта'
    """
    executer = db.Column(db.String(32))
    defect = db.Column(db.String(64))
    subspecies_defect = db.Column(db.Text)
    brief_information = db.Column(db.Text)
    train = db.Column(db.String(20))
    date = db.Column(db.Date)

    def __repr__(self) -> str:
        return (
            f'Иполнитель: {self.executer}\n'
            f'Неисправность: {self.defect}\n'
            f'Разновидность неисправности: {self.subspecies_defect}\n'
            f'Поезд: {self.train}\n'
            f'Дата: {self.date}'
            )


class Articles(db.Model, BaseModel):
    """
    Табличка 'Статьи'
    """
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)

    def __repr__(self) -> str:
        return (f'Статья: {self.name}')


class DataAccess:
    """
    Класс служит для извлечения данных из БД.
    """

    @logger.catch
    def get_articles(self) -> list:
        """
        Получение списка всех статей из базы данных.

        Returns:
            articles: список объектов статей.
        """
        articles = Articles.query.all()
        return articles

    @logger.catch
    def get_article(self, article_id: int) -> Articles:
        """
        Получение статьи из базы данных по ее идентификатору.

        Args:
            article_id (int): идентификатор статьи.

        Returns:
            article: объект статьи.
        """
        article = Articles.query.filter_by(id=article_id).first()
        return article

    @logger.catch
    def add_user(self,
                 name: str,
                 surname: str,
                 password: str,
                 post: str) -> None:
        """
        Добавление нового пользователя в базу данных.

        Args:
            name (str): Имя пользователя.
            surname (str): Фамилия пользователя.
            password (str): Нехешированный пароль пользователя.
            post (str): Должность пользователя.
        """
        new_user = Users(
            name=name,
            surname=surname,
            password=generate_password_hash(password),
            post=post
            )
        db.session.add(new_user)
        db.session.commit()

    @logger.catch
    def get_user(self, name: str, surname: str, password: str) -> bool | None:
        """
        Получение пользователя из базы данных и проверка введенного пароля.

        Args:
            name (str): имя пользователя.
            surname (str): фамилия пользователя.
            password (str): пароль пользователя.

        Returns:
            bool: True, если пользователь найден и пароль верен,
                  None в противном случае.
        """
        user = Users.query.filter_by(name=name, surname=surname).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return True

    @logger.catch
    def get_trains(self) -> list:
        """
        Получение списка всех поездов из базы данных.

        Returns:
            trains: список объектов поездов.
        """
        trains = Train.query.all()
        return trains

    @logger.catch
    def add_repair_inf(self,
                       name: str,
                       surname: str,
                       train: str,
                       defect: str,
                       s_def: str,
                       b_inf: str,
                       date: str
                       ) -> None:
        """
        Добавление новой информации о ремонте в базу данных.

        Args:
            name (str): имя исполнителя.
            surname (str): фамилия исполнителя.
            train (str): наименование поезда.
            defect (str): неисправность.
            s_def (str): разновидность неисправности.
            b_inf (str): краткая информация о ремонте.
            date (date): дата ремонта.
        """
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

    @logger.catch
    def get_repair_inf_with_date(self, train: str,
                                 start_date: str,
                                 end_date: str) -> list:
        """
        Получение информации о ремонте для определенного поезда
        в указанный период.

        Args:
            train (str): наименование поезда.
            start_date (date): начальная дата периода.
            end_date (date): конечная дата периода.

        Returns:
            repair_inf: список объектов информации о ремонте.
        """
        repair_inf = Repair_information.query.filter_by(
            train=train).filter(
                Repair_information.date.between(start_date, end_date)).all()
        return repair_inf

    @logger.catch
    def get_repair_inf(self, train: str) -> list:
        """
        Получение информации о ремонте за все время.

        Args:
            train (str): наименование поезда.

        Returns:
            repair_inf: список объектов информации о ремонте.
        """
        repair_inf = Repair_information.query.filter_by(train=train).all()
        return repair_inf

    @logger.catch
    def get_all_sub_defets(self, defect: str) -> list:
        """
        Получение всех разновидностей неисправности
        для указанной неисправности.

        Args:
            defect (str): неисправность.

        Returns:
             all_sub_defect: список объектов разновидностей неисправности.
        """
        all_sub_defect = Defects.query.filter_by(defect=defect).all()
        return all_sub_defect

    @logger.catch
    def get_sub_defet(self, sub_id: int) -> Defects:
        """
        Получение разновидности неисправности по ее идентификатору.

        Args:
            sub_id (int): идентификатор разновидности неисправности.

        Returns:
            sub_defect: объект разновидности неисправности.
        """
        sub_defect = Defects.query.filter_by(id=sub_id).first()
        return sub_defect


# Добавление метаданных в базу.
with app.app_context():
    db.create_all()


# Стандартная функция flask-login, для извлечения обьекта пользователя.
@logger.catch
@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
