from aiogram.dispatcher.filters.state import StatesGroup, State


class Question(StatesGroup):
    rainbow = State()
    csgo = State()
    dota = State()
    apex = State()
    change_nick = State()
    change_name = State()
    change_discord = State()
    commendplayer = State()
    reportlayer = State()
    Payment = State()
    Payment_newValue = State()
    timecsgo = State()
    timerainbow = State()
    timeapex = State()
    timedota = State()
    timerainbowmmr = State()
    timedotammr = State()
    timecsgommr = State()

