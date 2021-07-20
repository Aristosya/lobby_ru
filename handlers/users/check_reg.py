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


async def checkreg (message: types.Message):
    # Проверка Id IdTelegramofUser на уже существующий в базе.
    IdTelegramofUser = str(message.from_user.id)
    founding_users = await Users.select('users_id_telegram').where(
        Users.users_id_telegram == IdTelegramofUser).gino.scalar()

    if founding_users is not None:
        return True
    return False