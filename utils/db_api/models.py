from sqlalchemy import (Column, Integer, String, Sequence)
from sqlalchemy import sql
from utils.db_api.database import db


# Создаем класс таблицы товаров
class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select

    # Уникальный идентификатор товара
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    # Код категории (для отображения в колбек дате)
    category_code = Column(String(20))

    # Название категории (для отображения в кнопке)
    category_name = Column(String(50))

    # Код подкатегории (для отображения в колбек дате)
    subcategory_code = Column(String(50))

    # Название подкатегории (для отображения в кнопке)
    subcategory_name = Column(String(20))

    # Название, фото и цена товара
    name = Column(String(50))


class Users(db.Model):
    __tablename__ = 'users'
    query: sql.Select

    # Уникальный идентификатор User'a
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    # id Telegram чата
    users_id_telegram = Column(String(30))

    # Nick name usera в БД
    nick_name = Column(String(50))

    # name usera в БД
    name_of_user = Column(String(50))

    # Статистика usera в БД
    statistic = Column(Integer, default=0)

    # Дискорд usera в БД
    discord = Column(String(50))

    # Username @Telegram
    username = Column(String(50))

    #Если в лобби, он в лобби с ммр или нет ? 0-нет - 1да
    online_mmr = Column(Integer, default=None)

    #Если в лобби, он в лобби в какой игре ?
    online_game = Column(String(10), default=None)

    #Если в лобби, какой Id lobby ?
    online_lobby = Column(String(10), default=None)

    #Если в лобби, в какой час ?
    online_h = Column(Integer, default=None)

    # Если в лобби, в какую минуту ?
    online_m = Column(Integer, default=None)

    csmmr = Column(Integer, default=0)

    rainbowmmr = Column(Integer, default=0)

    dotammr = Column(Integer, default=0)




    def __repr__(self):
        return f""" """
