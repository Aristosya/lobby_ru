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

from .menu_handlers import show_menu

import asyncio

from utils.db_api.database import create_db

from .check_reg import checkreg
from .Check_Username import checkusername


from keyboards.default import yesnomenu


# запускаем машину состояний из команды /reg - в любом стейте
@dp.message_handler(commands=["reg", "register","registration"], state=None)
async def new_reg(message: types.Message):
    if await checkreg(message):
        await message.answer("You are registered. Open the menu...")
        await show_menu(message)
        return
    await message.answer("You started the registration\n\n"
                         "1) Write your nickname in the game\n\n\nOr /cancel - to cancel the registration")
    # Задаем стейт Test.Nick
    await Test.Nick.set()

@dp.message_handler(commands=['start'], state=None)
async def new_reg(message: types.Message):
    if await checkreg(message):
        await show_menu(message)
        return

    await message.answer("You are not registered !"
                            "Write /reg to start a registration")



@dp.message_handler(state = None)
async def answersome(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("/start or /menu !")



@dp.message_handler(Command("cancel"), state="*")
async def cancel_reg(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("You canceled registration")


# Сюда попадает все что человек написал, но только в стейте Test.Nick
@dp.message_handler(state=Test.Nick)
async def answer_nick(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 32:
        await message.answer("Maximum 32 characters allowed. Try again!")
        return
    else:
        if await checkusername(message):
            # Записываем текст в data answer_nick
            await state.update_data(answer_nick=answer)
            # Задаем вторую строку регистрации
            await message.answer("Ok!\n\n Now write your Name \n\n\nOr /cancel - to cancel the registration")

            await Test.Name.set()
            return
        else:
            await message.answer("This Nick Name already exists ! Try again !")
            return


@dp.message_handler(state=Test.Name)
async def answer_name(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 11:
        await message.answer("Maximum 11 characters allowed. Try again!")
        return
    else:
        await state.update_data(answer_name=answer)
        await message.answer(
            f"Nice to meet you {answer}!\n\n At the end write your Discord like this :    ExamPle#1902\n\n\nOr /cancel - to cancel the registration ")
        await Test.Discord.set()


@dp.message_handler(state=Test.Discord)
async def answer_discord(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 32:
        await message.answer("Maximum 32 characters allowed. Try again!")
        return
    else:
        await state.update_data(answer_discord=answer)
        # Проверка на ошибки
        data = await state.get_data()
        NickName = data.get("answer_nick")
        NameOfUser = data.get("answer_name")
        DiscordOfUser = data.get("answer_discord")
        await message.answer(f'''Let's to check it !\n\n\n'''
                             f'''Yor name is: {NameOfUser}\n'''
                             f'''Your nick name is: {NickName}\n'''
                             f'''Your Discord is: {DiscordOfUser}\n\n\n'''
                             f'''Is it true ?''', reply_markup=yesnomenu)
        await Test.Final.set()


@dp.message_handler(text='Yes', state=Test.Final)
async def answer_final(message: types.Message, state: FSMContext):
    # Запись в БД
    data = await state.get_data()
    NickName = data.get("answer_nick")
    NameOfUser = data.get("answer_name")
    DiscordOfUser = data.get("answer_discord")
    IdTelegramofUser = str(message.from_user.id)
    username = f'@{types.User.get_current().username}'

    await add_user(users_id_telegram=IdTelegramofUser,
                   nick_name=NickName,
                   name_of_user=NameOfUser,
                   discord=DiscordOfUser,
                   username=username
                   )

    await state.reset_state(with_data=False)
    await message.answer(f"""Thank you for the registration, {NameOfUser}  /menu""")


@dp.message_handler(text='No', state=Test.Final)
async def answer_finalNo(message: types.Message, state: FSMContext):
    await state.reset_state()
    await new_reg(message)
