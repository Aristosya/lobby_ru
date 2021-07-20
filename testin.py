import asyncio
import secrets
from loader import dp, bot
from typing import Union
from data import config
import datetime
from sqlalchemy import and_, or_

from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery, LabeledPrice, PreCheckoutQuery)
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, message
from aiogram.dispatcher import FSMContext
from utils.db_api.models import Users

from aiogram.dispatcher.filters import Command

from states.mmr_states import Question

from aiogram.utils.markdown import link
from data.config import PAYMENT_TOKEN
from utils.db_api.database import db

from collections import Counter

nowtime = datetime.timedelta(hours =22, minutes = 40)
findtime = datetime.timedelta(hours = 23, minutes = 00)
total = findtime - nowtime

print(total.seconds)