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
        await message.answer("Ты успешно зарегистроравн. Открываю меню...")
        await show_menu(message)
        return
    await message.answer("И так, начнем регистрацию!\n\n"
                         "1)Введи свой Ник в игре! \n\n\nили /cancel - для отмены регистрации!")
    # Задаем стейт Test.Nick
    await Test.Nick.set()

@dp.message_handler(commands=['start'], state=None)
async def new_reg(message: types.Message):
    if await checkreg(message):
        await show_menu(message)
        return

    await message.answer("Ты не зарегистрирован !"
                            "Напиши /reg - чтобы начать регистрацию!")



@dp.message_handler(state = None)
async def answersome(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("/start - для заупска бота или /menu - для открытия меню !")



@dp.message_handler(Command("cancel"), state="*")
async def cancel_reg(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Ты успешно отменил регистрацию!")


# Сюда попадает все что человек написал, но только в стейте Test.Nick
@dp.message_handler(state=Test.Nick)
async def answer_nick(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 32:
        await message.answer("Я разрешил только 32 символа! Попробуй снова!")
        return
    else:
        if await checkusername(message):
            # Записываем текст в data answer_nick
            await state.update_data(answer_nick=answer)
            # Задаем вторую строку регистрации
            await message.answer("Ладно! \n\n Теперь введи своё Имя! \n\n\nили /cancel - для отмены регистрации")

            await Test.Name.set()
            return
        else:
            await message.answer("Ой ой ой, такой ник уже существует! Попробуй снова!")
            return


@dp.message_handler(state=Test.Name)
async def answer_name(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 11:
        await message.answer("Я разрешил только 11 символов! Попробуй снова!!")
        return
    else:
        await state.update_data(answer_name=answer)
        await message.answer(
            f"Очень рад познакомиться с тобой {answer}!\n\n Ну и напоследок введи свой Дискорд :    NickName#1902\n\n\nили /cancel - для отмены регисрации!")
        await Test.Discord.set()


@dp.message_handler(state=Test.Discord)
async def answer_discord(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 32:
        await message.answer("Я разрешил только 32 символа! Попробуй снова!")
        return
    else:
        await state.update_data(answer_discord=answer)
        # Проверка на ошибки
        data = await state.get_data()
        NickName = data.get("answer_nick")
        NameOfUser = data.get("answer_name")
        DiscordOfUser = data.get("answer_discord")
        await message.answer(f'''Ну и давай взглянем на твои данные!\n\n\n'''
                             f'''Тебя зовут: {NameOfUser}\n'''
                             f'''Твой Ник: {NickName}\n'''
                             f'''Твой Дискорд: {DiscordOfUser}\n\n\n'''
                             f'''Всё верно?''', reply_markup=yesnomenu)
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
    await message.answer(f"""Спасибо за регистрацию, {NameOfUser}, ну а теперь окунемся в мир для поиска тиммейтов\n /menu - для открытию меню""")


@dp.message_handler(text='No', state=Test.Final)
async def answer_finalNo(message: types.Message, state: FSMContext):
    await state.reset_state()
    await new_reg(message)
