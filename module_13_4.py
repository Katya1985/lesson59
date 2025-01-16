from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = " "
bot = Bot(token= api)
dp = Dispatcher(bot, storage = MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight =State()
    gender = State()
    norma = State()


@dp.message_handler(text= "Calories")
async def set_age(message):
    await message.answer("Введите свой возраст: ")
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(first= message.text)
    await message.answer("Введите свой рост: ")
    await UserState.growth.set()


@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(second= message.text)
    await message.answer("Введите свой вес: ")
    await UserState.weight.set()


@dp.message_handler(state= UserState.gender)
async def if_calories(message, state):
    data = await state.get_data()
    if UserState.gender == "мужской":
        norma = int(10 * data(int['third']) + 6.25 * data(int['second']) - 5 * data(int['first']) + 5)
        await message.answer(f"Ваша норма калорий {norma}")
    else:
        norma = 10 * int(data['third']) + 6.25 * int(data['second']) - 5 * int(data['first']) - 161
        await message.answer(f"Ваша норма калорий {norma} ккал")
    await UserState.if_calories.set()
    await state.finish()


@dp.message_handler(commands= ['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью. \n"
                         "Введите слово Calories")


@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= True)


