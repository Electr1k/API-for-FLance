from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


# Класс для общей информации по заведениям
class Establishments(db.Model):
    # обьявление в базе данных столбцов: id, name, address, картинка для фона на главной
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    url_preview_img = db.Column(db.String(1000))
    lat_for_map = db.Column(db.Float)
    lng_for_map = db.Column(db.Float)

    def __repr__(self):
        return '<Establishments %r>' % self.id


# Класс для полной информации о заведении
class EstablishmentsFullInfo(db.Model):
    __bind_key__ = "establishments_full_info"  # переключение на другию бд(establishments_full_info.db)
    # обьявление в базе данных столбцов: id, name, address, картинка для фона на главной, url....
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    url_preview_img = db.Column(db.String(1000))
    url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prices = db.Column(db.JSON, nullable=False)
    booking = db.Column(db.JSON, nullable=False)
    wifi = db.Column(db.Boolean)
    battery = db.Column(db.Boolean)
    silence = db.Column(db.Boolean)
    cashless_payment = db.Column(db.Boolean)
    time_work = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Establishments_full_info %r>' % self.id


# Класс для пользователей
class Users(db.Model):
    __bind_key__ = "users"  # переключение на другию бд(users.db)
    # обьявление в базе данных столбцов: id, name, booking(список забронированных мест в JSON формате), ...
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    surname = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(1000), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    booking = db.Column(db.JSON)

    def __repr__(self):
        return '<users %r>' % self.email


def adds(user):
    db.session.add(user)  # обавление юзера в бд


def commits():
    db.session.commit()