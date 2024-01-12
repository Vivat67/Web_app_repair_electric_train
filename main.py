"""
Модуль содержит конфиг flask проекта.
Запускает приложение.
"""
import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr

from uuid import uuid4

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB')
app.config['SECRET_KEY'] = str(uuid4())

# База данных.
db = SQLAlchemy(app)
manager = LoginManager(app)

# Уведомления.
toastr = Toastr(app)


if __name__ == '__main__':
    load_dotenv()
    from controller import app
    app.run(debug=True, port=5678)
