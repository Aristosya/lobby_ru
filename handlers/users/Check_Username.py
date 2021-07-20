from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Command

from loader import dp
from states.reg_test import Test

from utils.db_api.models import Users
from utils.db_api.db_commands import add_user
from utils.db_api.database import db
from gino import Gino

from sqlalchemy import (Column, Integer, String, Sequence)
from sqlalchemy import sql

import asyncio

from utils.db_api.database import create_db


async def checkusername (message: types.Message):
    # Проверка username на уже существующий в базе.
    NewUsername = message.text
    founding_username = await Users.select('users_id_telegram').where(
        Users.nick_name == NewUsername).gino.scalar()
    if founding_username is not None:
        return False#Если нет такого ника в базе = тру
    return True