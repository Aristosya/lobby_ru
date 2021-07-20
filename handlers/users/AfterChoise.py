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
from .Check_Username import checkusername

from aiogram.utils.markdown import link
from data.config import PAYMENT_TOKEN
from utils.db_api.database import db

from collections import Counter


@dp.message_handler(Command("cancel"), state="*")
async def cancel_reg(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили изменения! /menu - для перехода в меню")
    await state.finish()


async def sure_12(call: CallbackQuery, sureid):
    await call.message.answer("Напишите ваш mmr в Rainbow 6 Siege. Пример : 2465 или /cancel - чтобы отменить.")
    await Question.rainbow.set()


async def sure_5(call: CallbackQuery, sureid):
    await call.message.answer("Выберите ваше звание: \n\n\n"
                              "1 - Серебро 1\n"
                              "2 - Серебро 2\n"
                              "3 - Серебро 3\n"
                              "4 - Серебро 4\n"
                              "5 - Серебро Элита\n"
                              "6 - Серебро Великий Магистр\n"
                              "7 - Золотая Звезда 1\n"
                              "8 - Золотая Звезда 2\n"
                              "9 - Золотая Звезда 3\n"
                              "10 - Золотая Звезда Магистр\n"
                              "11 - Магистр Хранитель 1\n"
                              "12 - Магистр Хранитель 2\n"
                              "13 - Магистр Хранитель Элита\n"
                              "14 - Заслуженный Магистр Хранитель\n"
                              "15 - Легендарный Беркут\n"
                              "16 - Легендарный Беркут Магистр\n"
                              "17 - Великий Магистр Высшего Ранга\n"
                              "18 - Всемирная Элита\n"
                              " или /cancel - чтобы отменить."
                              )
    await Question.csgo.set()


async def sure_18(call: CallbackQuery, sureid):
    await call.message.answer("Напишите ваш mmr в Dota 2. Пример : 2465 или /cancel - чтобы отменить.")
    await Question.dota.set()


async def sure_24(call: CallbackQuery, sureid):
    pass


async def sure_25(call: CallbackQuery, sureid):
    await call.message.answer("Напишите ваш новый Ник или /cancel - чтобы отменить.")
    await Question.change_nick.set()


async def sure_26(call: CallbackQuery, sureid):
    await call.message.answer("Напишите ваше новое Имя или /cancel.")
    await Question.change_name.set()


async def sure_27(call: CallbackQuery, sureid):
    await call.message.answer("Напишите ваш новый Discord. Пример : ЛоГин#1932 или /cancel - чтобы отменить.")
    await Question.change_discord.set()


async def sure_28(call: CallbackQuery, sureid):
    await call.message.answer("Напишите ник игрока которго хотите похвалить или /cancel - чтобы отменить.")
    await Question.commendplayer.set()


async def sure_29(call: CallbackQuery, sureid):
    await call.message.answer("Напишите ник игрока на которого хотите пожаловаться или /cancel - чтобы отменить.")
    await Question.reportlayer.set()


async def sure_30(call: CallbackQuery, sureid):
    await call.message.answer('<a href="https://discord.gg/sA2KCkw6Bm">Discord</a>  \n/menu', parse_mode="HTML")
    return


async def sure_31(call: CallbackQuery, sureid):
    await call.message.answer('<a href="https://vk.me/join/AJQ1d8lnYxwCcMuVuzIct6Vz">ВК Группа</a>  \n/menu',
                              parse_mode="HTML")
    return


async def sure_32(call: CallbackQuery, sureid):
    await call.message.answer('<a href="https://t.me/joinchat/iMSjRq04IpVmNWY0">Телеграм Группа</a>  \n/menu',
                              parse_mode="HTML")
    return


async def sure_33(call: CallbackQuery, sureid):
    await call.message.answer('1.Роман - <a href="https://vk.com/walomisrael">Тимлид, Программист</a>\n'
                              '2.Данил - <a href="https://vk.com/themarzipane">Дебагер, Переводчик Русского бота, Помощник</a>\n'
                              '3.Юрий - <a href="https://vk.com/dreadwolf_98">Тестер, Переводчик, Помощник</a>\n  /menu',
                              parse_mode="HTML")
    return


async def sure_37(call: CallbackQuery, sureid):
    await call.message.answer('Введите сумму в Рублях или /cancel - чтобы отменить')
    await Question.Payment_newValue.set()
    return


async def sure_34(call: CallbackQuery, sureid, ammount, state: FSMContext):
    currency = "RUB"
    need_name = True
    need_phone_number = False
    need_email = False
    need_shipping_address = False

    await bot.send_invoice(chat_id=call.from_user.id,
                           title=f"Донат {ammount/100} в Рублях",
                           description=f"Донат денег суммой {ammount/100} в Рублях",
                           payload=str(ammount),
                           start_parameter=str(ammount),
                           currency=currency,
                           prices=[
                               LabeledPrice(label=ammount, amount=ammount)
                           ],
                           provider_token=PAYMENT_TOKEN,
                           need_name=need_name,
                           need_phone_number=need_phone_number,
                           need_email=need_email,
                           need_shipping_address=need_shipping_address
                           )
    await Question.Payment.set()
    try:
        await call.message.answer("Или /cancel - чтобы отменить.")
    except:
        pass


async def sure_19(call: CallbackQuery, sureid):
    if (await Users.select('online_lobby').where(Users.users_id_telegram == str(
            call.from_user.id)).gino.scalar()) is None:  # Если пусто, то создаем, если нет  пишем

        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        await Users.update.values(online_lobby="AAALOBBY", online_mmr=0, online_game="minecraft",
                                  online_h=int(now.hour), online_m=int(now.minute)).where(
            Users.users_id_telegram == str(call.from_user.id)).gino.status()
        await call.message.answer("Вы были направлены в Маинкрафт лобби. /menu")
        await asyncio.sleep(7200)
        await Users.update.values(online_lobby=None, online_mmr=None, online_game=None, online_h=None,
                                  online_m=None).where(Users.users_id_telegram == str(call.from_user.id)).where(
            Users.online_h == hour).where(Users.online_m == minute).gino.status()
    else:
        gamelobby = await Users.select('online_game').where(
            Users.users_id_telegram == str(call.from_user.id)).gino.scalar()
        await call.message.answer(f"Вы уже находитесь в {gamelobby} лобби ! Сначала выйдете с него. /menu")
        return


async def leavefromthelobby(call: CallbackQuery, sureid):
    await Users.update.values(online_lobby=None, online_mmr=None, online_game=None, online_h=None, online_m=None).where(
        Users.users_id_telegram == str(call.from_user.id)).gino.status()
    await call.message.answer('Вы успешно вышли с лобби. /menu')
    return


async def findlobbycsgo(call: CallbackQuery, sureid):
    if (await Users.select('online_lobby').where(Users.users_id_telegram == str(
            call.from_user.id)).gino.scalar()) is None:
        await call.message.answer(
            "Какое время удобно для вашей игры ? \nНапишите его в формате ЧЧ:ММ. Пример: 18:32\nили /cancel - чтобы отменить.")
        if sureid == 1:
            await Question.timecsgommr.set()
        if sureid == 6:
            await Question.timecsgo.set()
    else:
        gamelobby = await Users.select('online_game').where(
            Users.users_id_telegram == str(call.from_user.id)).gino.scalar()
        await call.message.answer(f"Вы уже находитесь в {gamelobby} лобби ! Сначала выйдете с него. /menu")
        return


async def findlobbyrainbow(call: CallbackQuery, sureid):
    if (await Users.select('online_lobby').where(Users.users_id_telegram == str(
            call.from_user.id)).gino.scalar()) is None:
        await call.message.answer(
            "Какое время удобно для вашей игры ? \nНапишите его в формате ЧЧ:ММ. Пример: 18:32\nили /cancel - чтобы отменить.")
        if sureid == 7:
            await Question.timerainbowmmr.set()
        if sureid == 8:
            await Question.timerainbow.set()
    else:
        gamelobby = await Users.select('online_game').where(
            Users.users_id_telegram == str(call.from_user.id)).gino.scalar()
        await call.message.answer(f"Вы уже находитесь в {gamelobby} лобби ! Сначала выйдете с него. /menu")
        return

async def findlobbyapex(call: CallbackQuery, sureid):
    if (await Users.select('online_lobby').where(Users.users_id_telegram == str(
            call.from_user.id)).gino.scalar()) is None:
        await call.message.answer(
            "Какое время удобно для вашей игры ? \nНапишите его в формате ЧЧ:ММ. Пример: 18:32\nили /cancel - чтобы отменить.")
        await Question.timeapex.set()
    else:
        gamelobby = await Users.select('online_game').where(
            Users.users_id_telegram == str(call.from_user.id)).gino.scalar()
        await call.message.answer(f"Вы уже находитесь в {gamelobby} лобби ! Сначала выйдете с него. /menu")
        return



async def findlobbydota(call: CallbackQuery, sureid):
    if (await Users.select('online_lobby').where(Users.users_id_telegram == str(
            call.from_user.id)).gino.scalar()) is None:
        await call.message.answer(
            "Какое время удобно для вашей игры ? \nНапишите его в формате ЧЧ:ММ. Пример: 18:32\nили /cancel - чтобы отменить.")
        if sureid == 13:
            await Question.timedotammr.set()
        if sureid == 14:
            await Question.timedota.set()
    else:
        gamelobby = await Users.select('online_game').where(
            Users.users_id_telegram == str(call.from_user.id)).gino.scalar()
        await call.message.answer(f"Вы уже находитесь в {gamelobby} лобби ! Сначала выйдете с него. /menu")
        return


async def checkregisterlobby(call: CallbackQuery, sureid):
    reg_lobby = (
        await Users.select('online_lobby').where(Users.users_id_telegram == str(call.from_user.id)).gino.scalar())
    if reg_lobby is None:
        await call.message.answer("Вы не зарегистрированны в лобби! /menu")
        return
    else:
        async with db.transaction():
            number = 0
            gamelobby = await Users.select('online_game').where(
                Users.users_id_telegram == str(call.from_user.id)).gino.scalar()
            ismmr = int(await Users.select('online_mmr').where(Users.users_id_telegram == str(call.from_user.id)).gino.scalar())

            if ismmr == 0:
                text = f"Вы зарегистрированы в {gamelobby} лобби!\n\nТелеграм | Ник | Имя | Дискорд | Стат"
                async for row in Users.select('nick_name', 'name_of_user', 'discord', 'username',
                                              'statistic','dotammr','csmmr','rainbowmmr').where(Users.online_lobby == reg_lobby).gino.iterate():
                    number += 1
                    username = str(row['username'])
                    nick_name = str(row['nick_name'])
                    name_of_user = str(row['name_of_user'])
                    discord = str(row['discord'])
                    statistics = str(row['statistic'])
                    text += f'\n\n{number} | {username} | {nick_name} | {name_of_user} | {discord} | {statistics} |'
                text += "\n\n /menu"
                await call.message.answer(text)
                return
            else:
                text = f"Вы зарегистрированы в {gamelobby} лобби!\n\nТелеграм | Ник | Имя | Дискорд | Стат | Ммр "
                async for row in Users.select('nick_name', 'name_of_user', 'discord', 'username',
                                              'statistic','dotammr','csmmr','rainbowmmr').where(Users.online_lobby == reg_lobby).gino.iterate():
                    number += 1
                    username = str(row['username'])
                    nick_name = str(row['nick_name'])
                    name_of_user = str(row['name_of_user'])
                    discord = str(row['discord'])
                    statistics = str(row['statistic'])
                    if gamelobby == 'dota':
                        MMR = str(row['dotammr'])
                    elif gamelobby == 'rainbow':
                        MMR = str(row['rainbowmmr'])
                    elif gamelobby == 'csgo':
                        MMR = str(row['csmmr'])
                    text += f'\n\n{number} | {username} | {nick_name} | {name_of_user} | {discord} | {statistics} | {MMR}'
                text += "\n\n /menu"
                await call.message.answer(text)
                return


@dp.message_handler(state=Question.Payment_newValue)
async def newvaluepayment(message: types.Message, state: FSMContext):
    try:
        ammount = int(message.text)
    except:
        await message.answer("Что то пошло не так! Попробуйте снова или /cancel - чтобы отменить.")
        return

    await state.reset_state()
    await sure_34(message, 37, ammount*100, None)
    await message.answer("Или /cancel его! - чтобы отменить.")


@dp.pre_checkout_query_handler(state=Question.Payment)
async def checkout(query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(query.id, True)
    data = await state.get_data()
    success = await check_payment(Question)

    if success:
        await state.update_data(
            successful=True
            if query.order_info.shipping_address
            else None,
            phone_number=query.order_info.phone_number,
            receiver=query.order_info.name,
            email=query.order_info.email
        )
        await state.reset_state()
        await bot.send_message(query.from_user.id, ("Спасибо за вашу поддержку! /menu"))
    else:
        await bot.send_message(query.from_user.id, ("Неудачная покупка, попробуйте снова позже! /menu"))


async def check_payment(purchase: Question):
    return True


@dp.message_handler(state=Question.rainbow)
async def answer_mmrrainbow(message: types.Message, state: FSMContext):
    try:
        newmmr = int(message.text)
    except Exception as err:
        await message.answer("Что то пошло не так! Попробуйте снова или  - чтобы отменить.")

    if newmmr < 0 or newmmr > 6000:
        await message.answer("У вас не может быть MMR больше 6000 xD! Try again or /cancel - чтобы отменить.")
        return
    IdTelegramofUser = str(message.from_user.id)
    await Users.update.values(rainbowmmr=newmmr).where(Users.users_id_telegram == IdTelegramofUser).gino.status()
    await message.answer("Ваш MMR был изменен! /menu")
    await state.reset_state()
    return


@dp.message_handler(state=Question.csgo)
async def answer_mmrcsgo(message: types.Message, state: FSMContext):
    try:
        newmmr = int(message.text)
    except Exception as err:
        await message.answer("Что то пошло не так! Попробуйте снова или /cancel - чтобы отменить.")

    if newmmr < 0 or newmmr > 18:
        await message.answer("Вы ввели неверный ранг! Попробуйте снова или /cancel - чтобы отменить.")
        return

    IdTelegramofUser = str(message.from_user.id)
    await Users.update.values(csmmr=newmmr).where(Users.users_id_telegram == IdTelegramofUser).gino.status()
    await message.answer("Ваш MMR был изменен! /menu")
    await state.reset_state()
    return


@dp.message_handler(state=Question.dota)
async def answer_mmrdota(message: types.Message, state: FSMContext):
    try:
        newmmr = int(message.text)
    except Exception as err:
        await message.answer("Что то пошло не так! Попробуйте снова или /cancel- чтобы отменить.")

    if newmmr < 0 or newmmr > 13000:
        await message.answer("У вас не может быть MMR больше 13000 xD! Try again or /cancel- чтобы отменить. ")
        return

    IdTelegramofUser = str(message.from_user.id)
    await Users.update.values(dotammr=newmmr).where(Users.users_id_telegram == IdTelegramofUser).gino.status()
    await message.answer("Ваш MMR был изменен! /menu")
    await state.reset_state()
    return


@dp.message_handler(state=Question.change_nick)
async def answer_nick(message: types.Message, state: FSMContext):
    newnick = str(message.text)
    if len(newnick) > 32:
        await message.answer("Максимальная длина - 32 символа. Попробуйте снова! Or /cancel- чтобы отменить.")
        return
    else:
        if await checkusername(message):
            IdTelegramofUser = str(message.from_user.id)
            await Users.update.values(nick_name=newnick).where(
                Users.users_id_telegram == IdTelegramofUser).gino.status()
            await message.answer(f"Ваш ник был изменен на {newnick}! /menu")
            await state.reset_state()
            return
        else:
            await message.answer("Такой ник уже существует! Try again or /cancel- чтобы отменить.")
            await answer_nick(message)


@dp.message_handler(state=Question.change_name)
async def answer_name(message: types.Message, state: FSMContext):
    newname = str(message.text)
    if len(newname) > 11:
        await message.answer("Максимальная длина - 11 символов. Попробуйте снова! Or /cancel- чтобы отменить.")
        return
    else:
        IdTelegramofUser = str(message.from_user.id)
        await Users.update.values(name_of_user=newname).where(Users.users_id_telegram == IdTelegramofUser).gino.status()
        await message.answer(f"Ваше имя было изменено на {newname} ! /menu")
        await state.reset_state()
        return


@dp.message_handler(state=Question.change_discord)
async def answer_diskord(message: types.Message, state: FSMContext):
    newds = str(message.text)
    if len(newds) > 32:
        await message.answer("Максимальная длина - 32 символа. Попробуйте снова! Or /cancel- чтобы отменить.")
        return
    else:
        IdTelegramofUser = str(message.from_user.id)
        await Users.update.values(discord=newds).where(Users.users_id_telegram == IdTelegramofUser).gino.status()
        await message.answer(f"Ваш Дискорд был изменен на {newds} ! /menu")
        await state.reset_state()
        return


@dp.message_handler(state=Question.commendplayer)
async def answer_comendplayer(message: types.Message, state: FSMContext):
    player = message.text
    if await checkusername(message):  # проверяем есть ли такой ник вообще. Если тру - его нет, если фалсе - то есть
        await message.answer(f'Игрок с ником {player} не найден! Попробуйте снова или /cancel- чтобы отменить.')
        return

    else:
        old_statistic = int(await Users.select('statistic').where(Users.nick_name == player).gino.scalar())
        await Users.update.values(statistic=old_statistic + 1).where(Users.nick_name == player).gino.status()
        await message.answer(f"Вы похвалили игрока {player}! /menu")
        await state.reset_state()
        return


@dp.message_handler(state=Question.reportlayer)
async def answer_reportlayer(message: types.Message, state: FSMContext):
    player = message.text
    if await checkusername(message):  # проверяем есть ли такой ник вообще. Если тру - его нет, если фалсе - то есть
        await message.answer(f'Игрок с ником {player} не найден! Попробуйте снова или /cancel- чтобы отменить.')
        return

    else:
        old_statistic = int(await Users.select('statistic').where(Users.nick_name == player).gino.scalar())
        await Users.update.values(statistic=old_statistic - 1).where(Users.nick_name == player).gino.status()
        await message.answer(f"Вы пожаловались на игрока {player}! /menu")
        await state.reset_state()
        return


@dp.message_handler(state=Question.timecsgo)
async def lookingcsgo(message: types.Message, state: FSMContext):
    async with db.transaction():  # это что бы работал gino.iterate()
        time = message.text
        successroom = ''
        try:
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[-1])
        except:
            await message.answer("Что то пошло не так! Формат: ЧЧ:ММ \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if hours > 23:
            await message.answer("Вы ввели неверное количество часов!  \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if minutes > 59:
            await message.answer("Вы ввели неверное количество минут! \nПопробуйте снова или - чтобы отменить.")
            return

        findtime = datetime.timedelta(hours=hours, minutes=minutes)
        findtimeinmin = datetime.timedelta.total_seconds(findtime) / 60

        if hours == 00:
            findhoursmin = 23
            findhoursmax = 1
        elif hours == 23:
            findhoursmin = 22
            findhoursmax = 0
        else:
            findhoursmin = hours - 1
            findhoursmax = hours + 1




        min = findtime - datetime.timedelta(minutes=30)
        max = findtime + datetime.timedelta(minutes=30)
        mininmin = datetime.timedelta.total_seconds(min) / 60
        maxinmin = (datetime.timedelta.total_seconds(max) / 60)
        if mininmin < 0:
            mininmin = mininmin + 1440
            maxinmin = maxinmin + 1440
            findtimeinmin = findtimeinmin + 1440

        print(mininmin, maxinmin)

        allrooms = []
        async for row in Users.select('online_lobby').where(and_((Users.online_mmr == 0), (Users.online_game == "csgo"),
                                                                 (or_(Users.online_h == findhoursmin,
                                                                      Users.online_h == findhoursmax,
                                                                      Users.online_h == hours)))).gino.iterate():
            allrooms.append(row['online_lobby'])
            print(row['online_lobby'])
            minimumtime = 60
            successroom = ''
            successhour = 0
            successminute = 0

        b = Counter(allrooms)
        try:
            allroomsset = list(set(allrooms)) # Убираем повторяющиеся комнаты
            allrooms = list (allroomsset)
        except:
            pass

        for rooms in allroomsset:  # Максимальное кол-во игроков в лобби
            if b[rooms] >= 5:
                allrooms.remove(rooms)

        for rooms in allrooms:
            async with db.transaction():
                async for info in Users.select('online_h', 'online_m').where(
                        Users.online_lobby == rooms).gino.iterate():
                    playerhours = info['online_h']
                    playerminutes = info['online_m']
                    print(playerhours, playerminutes)
                    playertime = datetime.timedelta(hours=playerhours, minutes=playerminutes)
                    playertimeinmin = datetime.timedelta.total_seconds(playertime) / 60
                    print(playertimeinmin)
                    playertimeinmin_plus = playertimeinmin + 1440
                    print(playertimeinmin_plus)

                    if (playertimeinmin <= maxinmin and playertimeinmin >= mininmin):
                        temp = abs(playertimeinmin - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    elif (playertimeinmin_plus <= maxinmin and playertimeinmin_plus >= mininmin):
                        temp = abs(
                            playertimeinmin_plus - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    else:
                        break
        if successroom != '':
            await message.answer(f"Вы успешно подключились к лобби! /menu")
            await Users.update.values(online_lobby=successroom, online_mmr=0, online_game="csgo",
                                      online_h=successhour, online_m=successminute).where(
                Users.users_id_telegram == str(message.from_user.id)).gino.status()
            await state.reset_state()
            return
        else:
            await message.answer("Я не нашел подходящее лобби. Создаю лобби...")

    await state.reset_state()
    await newlobbygame(message, hours, minutes, 'csgo')


@dp.message_handler(state=Question.timerainbow)
async def lookingrainbow(message: types.Message, state: FSMContext):
    async with db.transaction():  # это что бы работал gino.iterate()
        time = message.text
        successroom = ''
        try:
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[-1])
        except:
            await message.answer("You wrote something wrong ! FORMAT: HH:MM \nTry again or /cancel- чтобы отменить. ")
            return
        if hours > 23:
            await message.answer("Вы ввели неверное количество минут! \nПопробуйте снова или - чтобы отменить. ")
            return
        if minutes > 59:
            await message.answer("Вы ввели неверное количество часов!  \nПопробуйте снова или /cancel- чтобы отменить.")
            return

        findtime = datetime.timedelta(hours=hours, minutes=minutes)
        findtimeinmin = datetime.timedelta.total_seconds(findtime) / 60

        if hours == 00:
            findhoursmin = 23
            findhoursmax = 1
        elif hours == 23:
            findhoursmin = 22
            findhoursmax = 0
        else:
            findhoursmin = hours - 1
            findhoursmax = hours + 1

        min = findtime - datetime.timedelta(minutes=30)
        max = findtime + datetime.timedelta(minutes=30)
        mininmin = datetime.timedelta.total_seconds(min) / 60
        maxinmin = (datetime.timedelta.total_seconds(max) / 60)
        if mininmin < 0:
            mininmin = mininmin + 1440
            maxinmin = maxinmin + 1440
            findtimeinmin = findtimeinmin + 1440

        print(mininmin, maxinmin)

        allrooms = []
        async for row in Users.select('online_lobby').where(
                and_((Users.online_mmr == 0), (Users.online_game == "rainbow"), (
                or_(Users.online_h == findhoursmin, Users.online_h == findhoursmax,
                    Users.online_h == hours)))).gino.iterate():
            allrooms.append(row['online_lobby'])
            print(row['online_lobby'])
            minimumtime = 60
            successroom = ''
            successhour = 0
            successminute = 0

        b = Counter(allrooms)
        try:
            allroomsset = list(set(allrooms))  # Убираем повторяющиеся комнаты
            allrooms = list(allroomsset)
        except:
            pass

        for rooms in allroomsset:  # Максимальное кол-во игроков в лобби
            if b[rooms] >= 5:
                allrooms.remove(rooms)
        for rooms in allrooms:
            async with db.transaction():
                async for info in Users.select('online_h', 'online_m').where(
                        Users.online_lobby == rooms).gino.iterate():
                    playerhours = info['online_h']
                    playerminutes = info['online_m']
                    print(playerhours, playerminutes)
                    playertime = datetime.timedelta(hours=playerhours, minutes=playerminutes)
                    playertimeinmin = datetime.timedelta.total_seconds(playertime) / 60
                    print(playertimeinmin)
                    playertimeinmin_plus = playertimeinmin + 1440
                    print(playertimeinmin_plus)

                    if (playertimeinmin <= maxinmin and playertimeinmin >= mininmin):
                        temp = abs(playertimeinmin - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    elif (playertimeinmin_plus <= maxinmin and playertimeinmin_plus >= mininmin):
                        temp = abs(
                            playertimeinmin_plus - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    else:
                        break
        if successroom != '':
            await message.answer(f"Вы успешно подключились к лобби! /menu")
            await Users.update.values(online_lobby=successroom, online_mmr=0, online_game="rainbow",
                                      online_h=successhour, online_m=successminute).where(
                Users.users_id_telegram == str(message.from_user.id)).gino.status()
            await state.reset_state()
            return
        else:
            await message.answer("Я не нашел подходящее лобби. Создаю лобби...")

    await state.reset_state()
    await newlobbygame(message, hours, minutes, 'rainbow')




@dp.message_handler(state=Question.timeapex)
async def lookingapex(message: types.Message, state: FSMContext):
    async with db.transaction():  # это что бы работал gino.iterate()
        time = message.text
        successroom = ''
        try:
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[-1])
        except:
            await message.answer("Что то пошло не так! Формат: ЧЧ:ММ \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if hours > 23:
            await message.answer("Вы ввели неверное количество часов!  \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if minutes > 59:
            await message.answer("Вы ввели неверное количество минут! \nПопробуйте снова или /cancel- чтобы отменить.")
            return

        findtime = datetime.timedelta(hours=hours, minutes=minutes)
        findtimeinmin = datetime.timedelta.total_seconds(findtime) / 60

        if hours == 00:
            findhoursmin = 23
            findhoursmax = 1
        elif hours == 23:
            findhoursmin = 22
            findhoursmax = 0
        else:
            findhoursmin = hours - 1
            findhoursmax = hours + 1

        min = findtime - datetime.timedelta(minutes=30)
        max = findtime + datetime.timedelta(minutes=30)
        mininmin = datetime.timedelta.total_seconds(min) / 60
        maxinmin = (datetime.timedelta.total_seconds(max) / 60)
        if mininmin < 0:
            mininmin = mininmin + 1440
            maxinmin = maxinmin + 1440
            findtimeinmin = findtimeinmin + 1440

        print(mininmin, maxinmin)

        allrooms = []
        async for row in Users.select('online_lobby').where(
                and_((Users.online_mmr == 0), (Users.online_game == "apex"), (
                or_(Users.online_h == findhoursmin, Users.online_h == findhoursmax,
                    Users.online_h == hours)))).gino.iterate():
            allrooms.append(row['online_lobby'])
            print(row['online_lobby'])
            minimumtime = 60
            successroom = ''
            successhour = 0
            successminute = 0

        b = Counter(allrooms)
        try:
            allroomsset = list(set(allrooms))  # Убираем повторяющиеся комнаты
            allrooms = list(allroomsset)
        except:
            pass

        for rooms in allroomsset:  # Максимальное кол-во игроков в лобби
            if b[rooms] >= 3:
                allrooms.remove(rooms)

        for rooms in allrooms:
            async with db.transaction():
                async for info in Users.select('online_h', 'online_m').where(
                        Users.online_lobby == rooms).gino.iterate():
                    playerhours = info['online_h']
                    playerminutes = info['online_m']
                    print(playerhours, playerminutes)
                    playertime = datetime.timedelta(hours=playerhours, minutes=playerminutes)
                    playertimeinmin = datetime.timedelta.total_seconds(playertime) / 60
                    print(playertimeinmin)
                    playertimeinmin_plus = playertimeinmin + 1440
                    print(playertimeinmin_plus)

                    if (playertimeinmin <= maxinmin and playertimeinmin >= mininmin):
                        temp = abs(playertimeinmin - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    elif (playertimeinmin_plus <= maxinmin and playertimeinmin_plus >= mininmin):
                        temp = abs(
                            playertimeinmin_plus - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    else:
                        break
        if successroom != '':
            await message.answer(f"Вы успешно подключились к лобби! /menu")
            await Users.update.values(online_lobby=successroom, online_mmr=0, online_game="apex",
                                      online_h=successhour, online_m=successminute).where(
                Users.users_id_telegram == str(message.from_user.id)).gino.status()
            await state.reset_state()
            return
        else:
            await message.answer("Я не нашел подходящее лобби. Создаю лобби...")

    await state.reset_state()
    await newlobbygame(message, hours, minutes, 'apex')









@dp.message_handler(state=Question.timedota)
async def lookingdota(message: types.Message, state: FSMContext):
    async with db.transaction():  # это что бы работал gino.iterate()
        time = message.text
        successroom = ''
        try:
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[-1])
        except:
            await message.answer("Что то пошло не так! Формат: ЧЧ:ММ \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if hours > 23:
            await message.answer("Вы ввели неверное количество часов!  \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if minutes > 59:
            await message.answer("Вы ввели неверное количество минут! \nПопробуйте снова или /cancel- чтобы отменить.")
            return

        findtime = datetime.timedelta(hours=hours, minutes=minutes)
        findtimeinmin = datetime.timedelta.total_seconds(findtime) / 60

        if hours == 00:
            findhoursmin = 23
            findhoursmax = 1
        elif hours == 23:
            findhoursmin = 22
            findhoursmax = 0
        else:
            findhoursmin = hours - 1
            findhoursmax = hours + 1

        min = findtime - datetime.timedelta(minutes=30)
        max = findtime + datetime.timedelta(minutes=30)
        mininmin = datetime.timedelta.total_seconds(min) / 60
        maxinmin = (datetime.timedelta.total_seconds(max) / 60)
        if mininmin < 0:
            mininmin = mininmin + 1440
            maxinmin = maxinmin + 1440
            findtimeinmin = findtimeinmin + 1440

        print(mininmin, maxinmin)

        allrooms = []
        async for row in Users.select('online_lobby').where(
                and_((Users.online_mmr == 0), (Users.online_game == "dota"), (
                or_(Users.online_h == findhoursmin, Users.online_h == findhoursmax,
                    Users.online_h == hours)))).gino.iterate():
            allrooms.append(row['online_lobby'])
            print(row['online_lobby'])
            minimumtime = 60
            successroom = ''
            successhour = 0
            successminute = 0

        b = Counter(allrooms)
        try:
            allroomsset = list(set(allrooms))  # Убираем повторяющиеся комнаты
            allrooms = list(allroomsset)
        except:
            pass

        for rooms in allroomsset:  # Максимальное кол-во игроков в лобби
            if b[rooms] >= 5:
                allrooms.remove(rooms)

        for rooms in allrooms:
            async with db.transaction():
                async for info in Users.select('online_h', 'online_m').where(
                        Users.online_lobby == rooms).gino.iterate():
                    playerhours = info['online_h']
                    playerminutes = info['online_m']
                    print(playerhours, playerminutes)
                    playertime = datetime.timedelta(hours=playerhours, minutes=playerminutes)
                    playertimeinmin = datetime.timedelta.total_seconds(playertime) / 60
                    print(playertimeinmin)
                    playertimeinmin_plus = playertimeinmin + 1440
                    print(playertimeinmin_plus)

                    if (playertimeinmin <= maxinmin and playertimeinmin >= mininmin):
                        temp = abs(playertimeinmin - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    elif (playertimeinmin_plus <= maxinmin and playertimeinmin_plus >= mininmin):
                        temp = abs(
                            playertimeinmin_plus - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        break
                    else:
                        break
        if successroom != '':
            await message.answer(f"Вы успешно подключились к лобби! /menu")
            await Users.update.values(online_lobby=successroom, online_mmr=0, online_game="dota",
                                      online_h=successhour, online_m=successminute).where(
                Users.users_id_telegram == str(message.from_user.id)).gino.status()
            await state.reset_state()
            return
        else:
            await message.answer("Я не нашел подходящее лобби. Создаю лобби...")

    await state.reset_state()
    await newlobbygame(message, hours, minutes, 'dota')









@dp.message_handler(state=Question.timerainbowmmr)
async def lookingrainbowmmr(message: types.Message, state: FSMContext):
    async with db.transaction():  # это что бы работал gino.iterate()
        time = message.text
        successroom = ''
        try:
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[-1])
        except:
            await message.answer("Что то пошло не так! Формат: ЧЧ:ММ \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if hours > 23:
            await message.answer("Вы ввели неверное количество часов!  \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if minutes > 59:
            await message.answer("Вы ввели неверное количество минут! \nПопробуйте снова или /cancel- чтобы отменить.")
            return

        findtime = datetime.timedelta(hours=hours, minutes=minutes)
        findtimeinmin = datetime.timedelta.total_seconds(findtime) / 60

        if hours == 00:
            findhoursmin = 23
            findhoursmax = 1
        elif hours == 23:
            findhoursmin = 22
            findhoursmax = 0
        else:
            findhoursmin = hours - 1
            findhoursmax = hours + 1

        min = findtime - datetime.timedelta(minutes=30)
        max = findtime + datetime.timedelta(minutes=30)
        mininmin = datetime.timedelta.total_seconds(min) / 60
        maxinmin = (datetime.timedelta.total_seconds(max) / 60)
        if mininmin < 0:
            mininmin = mininmin + 1440
            maxinmin = maxinmin + 1440
            findtimeinmin = findtimeinmin + 1440

        print(mininmin, maxinmin)
        mymmr = int(await (Users.select('rainbowmmr').where(Users.users_id_telegram == str(message.from_user.id))).gino.scalar())
        allrooms = []
        async for row in Users.select('online_lobby').where(
                and_((Users.online_mmr == 1), (Users.online_game == "rainbow"), (
                or_(Users.online_h == findhoursmin, Users.online_h == findhoursmax,
                    Users.online_h == hours)),and_((Users.rainbowmmr <= mymmr + 700),(Users.rainbowmmr >= mymmr - 700)))).gino.iterate():
            allrooms.append(row['online_lobby'])
            print(row['online_lobby'])
            minimumtime = 60
            successroom = ''
            successhour = 0
            successminute = 0

        b = Counter(allrooms)
        try:
            allroomsset = list(set(allrooms))  # Убираем повторяющиеся комнаты
            allrooms = list(allroomsset)
        except:
            pass



        for rooms in allroomsset:  # Максимальное кол-во игроков в лобби
            if b[rooms] >= 5:
                allrooms.remove(rooms)
        for rooms in allrooms:
            async with db.transaction():
                async for info in Users.select('online_h', 'online_m','rainbowmmr').where(
                        Users.online_lobby == rooms).gino.iterate():
                    playerhours = info['online_h']
                    playerminutes = info['online_m']
                    print(playerhours, playerminutes)
                    playertime = datetime.timedelta(hours=playerhours, minutes=playerminutes)
                    playertimeinmin = datetime.timedelta.total_seconds(playertime) / 60
                    print(playertimeinmin)
                    playertimeinmin_plus = playertimeinmin + 1440
                    print(playertimeinmin_plus)
                    playermmr = info['rainbowmmr']
                    print (playermmr)
                    print (mymmr)

                    if (playermmr > mymmr + 700) or (playermmr < mymmr - 700):
                        if successroom == rooms:
                            minimumtime = 60
                            successroom = ''
                            successhour = 0
                            successminute = 0
                        break

                    if (playertimeinmin <= maxinmin and playertimeinmin >= mininmin):
                        temp = abs(playertimeinmin - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        continue
                    elif (playertimeinmin_plus <= maxinmin and playertimeinmin_plus >= mininmin):
                        temp = abs(
                            playertimeinmin_plus - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        continue
                    else:
                        break
        if successroom != '':
            await message.answer(f"Вы успешно подключились к лобби! /menu")
            await Users.update.values(online_lobby=successroom, online_mmr=1, online_game="rainbow",
                                      online_h=successhour, online_m=successminute).where(
                Users.users_id_telegram == str(message.from_user.id)).gino.status()
            await state.reset_state()
            return
        else:
            await message.answer("Я не нашел подходящее лобби. Создаю лобби...")

    await state.reset_state()
    await newlobbygamemmr(message, hours, minutes, 'rainbow')





@dp.message_handler(state=Question.timedotammr)
async def lookingdotammr(message: types.Message, state: FSMContext):
    async with db.transaction():  # это что бы работал gino.iterate()
        time = message.text
        successroom = ''
        try:
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[-1])
        except:
            await message.answer("Что то пошло не так! Формат: ЧЧ:ММ \nПопробуйте снова или /cancel- чтобы отменить.")
            return
        if hours > 23:
            await message.answer("Вы ввели неверное количество часов!  \nПопробуйте снова или /cancel- чтобы отменить. ")
            return
        if minutes > 59:
            await message.answer("Вы ввели неверное количество минут! \nПопробуйте снова или /cancel- чтобы отменить. ")
            return

        findtime = datetime.timedelta(hours=hours, minutes=minutes)
        findtimeinmin = datetime.timedelta.total_seconds(findtime) / 60

        if hours == 00:
            findhoursmin = 23
            findhoursmax = 1
        elif hours == 23:
            findhoursmin = 22
            findhoursmax = 0
        else:
            findhoursmin = hours - 1
            findhoursmax = hours + 1

        min = findtime - datetime.timedelta(minutes=30)
        max = findtime + datetime.timedelta(minutes=30)
        mininmin = datetime.timedelta.total_seconds(min) / 60
        maxinmin = (datetime.timedelta.total_seconds(max) / 60)
        if mininmin < 0:
            mininmin = mininmin + 1440
            maxinmin = maxinmin + 1440
            findtimeinmin = findtimeinmin + 1440

        print(mininmin, maxinmin)
        mymmr = int(await (Users.select('dotammr').where(Users.users_id_telegram == str(message.from_user.id))).gino.scalar())
        allrooms = []
        async for row in Users.select('online_lobby').where(
                and_((Users.online_mmr == 1), (Users.online_game == "dota"), (
                or_(Users.online_h == findhoursmin, Users.online_h == findhoursmax,
                    Users.online_h == hours)),and_((Users.dotammr <= mymmr + 2000),(Users.dotammr >= mymmr - 2000)))).gino.iterate():
            allrooms.append(row['online_lobby'])
            print(row['online_lobby'])
            minimumtime = 60
            successroom = ''
            successhour = 0
            successminute = 0

        b = Counter(allrooms)
        try:
            allroomsset = list(set(allrooms))  # Убираем повторяющиеся комнаты
            allrooms = list(allroomsset)
        except:
            pass



        for rooms in allroomsset:  # Максимальное кол-во игроков в лобби
            if b[rooms] >= 5:
                allrooms.remove(rooms)
        for rooms in allrooms:
            async with db.transaction():
                async for info in Users.select('online_h', 'online_m','dotammr').where(
                        Users.online_lobby == rooms).gino.iterate():
                    playerhours = info['online_h']
                    playerminutes = info['online_m']
                    print(playerhours, playerminutes)
                    playertime = datetime.timedelta(hours=playerhours, minutes=playerminutes)
                    playertimeinmin = datetime.timedelta.total_seconds(playertime) / 60
                    print(playertimeinmin)
                    playertimeinmin_plus = playertimeinmin + 1440
                    print(playertimeinmin_plus)
                    playermmr = info['dotammr']
                    print (playermmr)
                    print (mymmr)

                    if (playermmr > mymmr + 2000) or (playermmr < mymmr - 2000):
                        if successroom == rooms:
                            minimumtime = 60
                            successroom = ''
                            successhour = 0
                            successminute = 0
                        break

                    if (playertimeinmin <= maxinmin and playertimeinmin >= mininmin):
                        temp = abs(playertimeinmin - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        continue
                    elif (playertimeinmin_plus <= maxinmin and playertimeinmin_plus >= mininmin):
                        temp = abs(
                            playertimeinmin_plus - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        continue
                    else:
                        break
        if successroom != '':
            await message.answer(f"Вы успешно подключились к лобби! /menu")
            await Users.update.values(online_lobby=successroom, online_mmr=1, online_game="dota",
                                      online_h=successhour, online_m=successminute).where(
                Users.users_id_telegram == str(message.from_user.id)).gino.status()
            await state.reset_state()
            return
        else:
            await message.answer("Я не нашел подходящее лобби. Создаю лобби...")

    await state.reset_state()
    await newlobbygamemmr(message, hours, minutes, 'dota')

@dp.message_handler(state=Question.timecsgommr)
async def lookingcsgommr(message: types.Message, state: FSMContext):
    async with db.transaction():  # это что бы работал gino.iterate()
        time = message.text
        successroom = ''
        try:
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[-1])
        except:
            await message.answer("Что то пошло не так! Формат: ЧЧ:ММ \nПопробуйте снова или /cancel- чтобы отменить. ")
            return
        if hours > 23:
            await message.answer("Вы ввели неверное количество часов!  \nПопробуйте снова или /cancel- чтобы отменить. ")
            return
        if minutes > 59:
            await message.answer("Вы ввели неверное количество минут! \nПопробуйте снова или /cancel- чтобы отменить. ")
            return

        findtime = datetime.timedelta(hours=hours, minutes=minutes)
        findtimeinmin = datetime.timedelta.total_seconds(findtime) / 60

        if hours == 00:
            findhoursmin = 23
            findhoursmax = 1
        elif hours == 23:
            findhoursmin = 22
            findhoursmax = 0
        else:
            findhoursmin = hours - 1
            findhoursmax = hours + 1

        min = findtime - datetime.timedelta(minutes=30)
        max = findtime + datetime.timedelta(minutes=30)
        mininmin = datetime.timedelta.total_seconds(min) / 60
        maxinmin = (datetime.timedelta.total_seconds(max) / 60)
        if mininmin < 0:
            mininmin = mininmin + 1440
            maxinmin = maxinmin + 1440
            findtimeinmin = findtimeinmin + 1440

        print(mininmin, maxinmin)
        mymmr = int(await (Users.select('csmmr').where(Users.users_id_telegram == str(message.from_user.id))).gino.scalar())
        allrooms = []
        async for row in Users.select('online_lobby').where(
                and_((Users.online_mmr == 1), (Users.online_game == "csgo"), (
                or_(Users.online_h == findhoursmin, Users.online_h == findhoursmax,
                    Users.online_h == hours)),and_((Users.dotammr <= mymmr + 4),(Users.dotammr >= mymmr - 4)))).gino.iterate():
            allrooms.append(row['online_lobby'])
            print(row['online_lobby'])
            minimumtime = 60
            successroom = ''
            successhour = 0
            successminute = 0

        b = Counter(allrooms)
        try:
            allroomsset = list(set(allrooms))  # Убираем повторяющиеся комнаты
            allrooms = list(allroomsset)
        except:
            pass



        for rooms in allroomsset:  # Максимальное кол-во игроков в лобби
            if b[rooms] >= 5:
                allrooms.remove(rooms)
        for rooms in allrooms:
            async with db.transaction():
                async for info in Users.select('online_h', 'online_m','csmmr').where(
                        Users.online_lobby == rooms).gino.iterate():
                    playerhours = info['online_h']
                    playerminutes = info['online_m']
                    print(playerhours, playerminutes)
                    playertime = datetime.timedelta(hours=playerhours, minutes=playerminutes)
                    playertimeinmin = datetime.timedelta.total_seconds(playertime) / 60
                    print(playertimeinmin)
                    playertimeinmin_plus = playertimeinmin + 1440
                    print(playertimeinmin_plus)
                    playermmr = info['csmmr']
                    print (playermmr)
                    print (mymmr)

                    if (playermmr > mymmr + 4) or (playermmr < mymmr - 4):
                        if successroom == rooms:
                            minimumtime = 60
                            successroom = ''
                            successhour = 0
                            successminute = 0
                        break

                    if (playertimeinmin <= maxinmin and playertimeinmin >= mininmin):
                        temp = abs(playertimeinmin - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        continue
                    elif (playertimeinmin_plus <= maxinmin and playertimeinmin_plus >= mininmin):
                        temp = abs(
                            playertimeinmin_plus - findtimeinmin)  # Это было придумано для поиска ближайшей комнаты
                        if minimumtime > temp:
                            minimumtime = temp
                            successroom = rooms
                            successhour = playerhours
                            successminute = playerminutes
                        continue
                    else:
                        break
        if successroom != '':
            await message.answer(f"Вы успешно подключились к лобби! /menu")
            await Users.update.values(online_lobby=successroom, online_mmr=1, online_game="csgo",
                                      online_h=successhour, online_m=successminute).where(
                Users.users_id_telegram == str(message.from_user.id)).gino.status()
            await state.reset_state()
            return
        else:
            await message.answer("Я не нашел подходящее лобби. Создаю лобби...")

    await state.reset_state()
    await newlobbygamemmr(message, hours, minutes, 'csgo')











async def newlobbygame(message: types.Message, hours, minutes, online_game):
    newlobby = secrets.token_hex(5)

    h = datetime.datetime.now().time().hour
    m = datetime.datetime.now().time().minute
    nowtime = datetime.timedelta(hours=h, minutes=m)
    findtime = datetime.timedelta(hours=hours, minutes=minutes)
    total = findtime - nowtime

    checknewcode = (
        await Users.select('online_lobby').where(Users.online_lobby == str(newlobby)).gino.scalar())

    if checknewcode is None:
        await Users.update.values(online_lobby=newlobby, online_mmr=0, online_game=online_game,
                                  online_h=hours, online_m=minutes).where(
            Users.users_id_telegram == str(message.from_user.id)).gino.status()
        await message.answer(
            f"Вы подключилсь к {online_game} лобби. \n Лобби будет удалено через 2 часа после начала! /menu")
        await asyncio.sleep(total.seconds + 7200)
        await Users.update.values(online_lobby=None, online_mmr=None, online_game=None, online_h=None,
                                  online_m=None).where(Users.online_lobby == newlobby).gino.status()
        return
    else:
        await newlobbygame(message, hours, minutes, online_game)


async def newlobbygamemmr(message: types.Message, hours, minutes, online_game):
    newlobby = secrets.token_hex(5)

    h = datetime.datetime.now().time().hour
    m = datetime.datetime.now().time().minute
    nowtime = datetime.timedelta(hours=h, minutes=m)
    findtime = datetime.timedelta(hours=hours, minutes=minutes)
    total = findtime - nowtime




    checknewcode = (
        await Users.select('online_lobby').where(Users.online_lobby == str(newlobby)).gino.scalar())

    if checknewcode is None:
        await Users.update.values(online_lobby=newlobby, online_mmr=1, online_game=online_game,
                                  online_h=hours, online_m=minutes).where(
            Users.users_id_telegram == str(message.from_user.id)).gino.status()
        await message.answer(
            f"Вы подключилсь к {online_game} лобби. \n Лобби будет удалено через 2 часа после начала! /menu")
        await asyncio.sleep(total.seconds + 7200)
        await Users.update.values(online_lobby=None, online_mmr=None, online_game=None, online_h=None,
                                  online_m=None).where(Users.online_lobby == newlobby).gino.status()
        return
    else:
        await newlobbygame(message, hours, minutes, online_game)
