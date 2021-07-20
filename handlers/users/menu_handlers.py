from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, message
from aiogram.dispatcher import FSMContext
from states.mmr_states import Question

from keyboards.inline.menu_keyboards import menu_cd, categories_keyboard, subcategories_keyboard, \
    items_keyboard, sure_choise  # , item_keyboard это для нового ЛВЛа
from loader import dp
from utils.db_api.db_commands import get_item
from .check_reg import checkreg
from .AfterChoise import sure_12
from .AfterChoise import sure_5
from .AfterChoise import sure_18
from .AfterChoise import sure_24
from .AfterChoise import sure_25
from .AfterChoise import sure_26
from .AfterChoise import sure_27
from .AfterChoise import sure_28
from .AfterChoise import sure_29
from .AfterChoise import sure_30
from .AfterChoise import sure_31
from .AfterChoise import sure_32
from .AfterChoise import sure_33
from .AfterChoise import sure_34
from .AfterChoise import sure_37
from .AfterChoise import sure_19
from .AfterChoise import leavefromthelobby
from .AfterChoise import checkregisterlobby
from .AfterChoise import findlobbycsgo
from .AfterChoise import findlobbyrainbow
from .AfterChoise import findlobbyapex
from .AfterChoise import findlobbydota


# Хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    # Проверка на регистрацию
    if await checkreg(message):
        # Выполним функцию, которая отправит пользователю кнопки с доступными категориями
        await list_categories(message)
    else:
        await message.answer("Вы обязаны быть зарегистрированным пользователем. /reg для начала регистрации !")
        return


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await categories_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Что Вы хотите выбрать ?", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        text = f'Что Вы хотите выбрать ?'
        await call.message.edit_text(text=text, reply_markup=markup)


# Функция, которая отдает кнопки с подкатегориями, по выбранной пользователем категории
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    text = f'Выберите действие'
    await callback.message.edit_text(text=text, reply_markup=markup)


# Функция, которая отдает кнопки с Названием и ценой товара, по выбранной категории и подкатегории
async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category, subcategory)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    text = f'Выберите действие'
    await callback.message.edit_text(text=text, reply_markup=markup)


# # Функция, которая отдает уже кнопку Купить товар по выбранному товару
# async def show_item(callback: CallbackQuery, category, subcategory, item_id):
#     markup = item_keyboard(category, subcategory, item_id)
#
#     # Берем запись о нашем товаре из базы данных
#     item = await get_item(item_id)
#     text = f'Are you sure ? You choosed {item.name}'
#     await callback.message.edit_text(text=text, reply_markup=markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """

    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category = callback_data.get("category")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    subcategory = callback_data.get("subcategory")

    # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    item_id = int(callback_data.get("item_id"))

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_categories,  # Отдаем категории
        "1": list_subcategories,  # Отдаем подкатегории
        "2": list_items,  # Отдаем товары
        # "3": show_item  # Предлагаем купить товар для нового ЛВЛа
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        category=category,
        subcategory=subcategory,
        item_id=item_id
    )


@dp.callback_query_handler(sure_choise.filter())
async def sure(call: CallbackQuery, callback_data: dict):
    sureid = int(callback_data.get("item_id"))

    if sureid == 12:  # 12-Id изменения ММР в Радуге по БД
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_12(call, sureid)
        return
    elif sureid == 5:  # 5-Id изменения ММР в CS по БД
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_5(call, sureid)
        return
    elif sureid == 18:  # 18-Id изменения ММР в Dota 2 по БД
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_18(call, sureid)
        return
    elif sureid == 25:  # change nick name
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_25(call, sureid)
        return
    elif sureid == 26:  # change name
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_26(call, sureid)
        return

    elif sureid == 27:  # change discord username
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_27(call, sureid)
        return
    elif sureid == 28:  # commend players
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_28(call, sureid)
        return
    elif sureid == 29:  # report
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_29(call, sureid)
        return
    elif sureid == 30:  # link discord
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_30(call, sureid)
        return
    elif sureid == 31:  # link VK
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_31(call, sureid)
        return
    elif sureid == 32:  # link Telegram Group
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_32(call, sureid)
        return
    elif sureid == 33:  # link developers
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_33(call, sureid)
        return
    elif sureid == 34:  # Donate 1$
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_34(call, sureid, 7320, None)
        return
    elif sureid == 35:  # Donate 5$
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_34(call, sureid, 7320 * 5, None)
        return
    elif sureid == 36:  # Donate 10$
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_34(call, sureid, 7320 * 10, None)
        return
    elif sureid == 37:  # Donate ? $
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_37(call, sureid)
        return
    elif sureid == 19:  # find lobby minecraft
        await call.message.delete()
        await call.answer(cache_time=60)
        await sure_19(call, sureid)
        return
    elif sureid == 24 or sureid == 2 or sureid == 9 or sureid == 15 or sureid == 21:  # 24-Выход из лобби
        await call.message.delete()
        await call.answer(cache_time=60)
        await leavefromthelobby(call, sureid)
        return
    elif sureid == 38 or sureid == 4 or sureid == 11 or sureid == 17 or sureid == 23:#check register lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await checkregisterlobby(call, sureid)
        return
    elif sureid == 6: # with out MMR csgo Lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await findlobbycsgo(call, sureid)
        return
    elif sureid == 8:#with out MMR rainbow Lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await findlobbyrainbow(call, sureid)
        return
    elif sureid == 20:#with out MMR apex Lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await findlobbyapex(call, sureid)
        return
    elif sureid == 14:#with out MMR dota Lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await findlobbydota(call, sureid)
        return
    elif sureid == 7:#with MMR r6 Lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await findlobbyrainbow(call, sureid)
        return
    elif sureid == 13:#with MMR dota Lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await findlobbydota(call, sureid)
        return
    elif sureid == 1:#with MMR csgo Lobby
        await call.message.delete()
        await call.answer(cache_time=60)
        await findlobbycsgo(call, sureid)
        return




    else:
        pass
