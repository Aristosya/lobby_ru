from aiogram.dispatcher.filters.state import StatesGroup,State

class Test(StatesGroup):
    Nick = State()
    Name = State()
    Discord = State()
    Final = State()