from request import get_link, get_response
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from cfg import access, token, req_types


bot = Bot(token=token, parse_mode='html')
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class Date(StatesGroup):
    date = State()


@dp.message_handler(commands=['jails', 'mutes', 'kicks', 'events', 'reports'])
async def get_date(message: types.Message, state: FSMContext):

    if not(message.from_user.id in access):
        return await message.answer("У вас нет доступа к использованию бота!")

    async with state.proxy() as data:
        data['request'] = req_types[message.text]

    await Date.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-день. Пример: 01-30"
    )


@dp.message_handler(commands=['online'])
async def get_date(message: types.Message, state: FSMContext):

    if not(message.from_user.id in access):
        return await message.answer("У вас нет доступа к использованию бота!")

    async with state.proxy() as data:
        data['request'] = req_types[message.text]

    await Date.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-деньTчас:минуты Пример: 01-30T23:30"
    )


@dp.message_handler(state=Date.date)
async def get_jails(message: types.Message, state: FSMContext):
    await Date.date.set()
    dictionary = {}
    offset = 0

    async with state.proxy() as data:
        req = data['request']

    while True:

        link = await get_link(date=message.text, **req, offset=offset)
        response = await get_response(link)

        for tup in response:
            if tup["player_name"] in dictionary:
                dictionary[tup["player_name"]] += 1
            else:
                dictionary[tup["player_name"]] = 1

        if len(response) == 200:
            offset += 200
            continue
        break

    msg, k = "", 0
    top = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))

    for key in top:
        k += 1
        msg += f"{k}. {key}: {top[key]}\n"

    await state.finish()
    await message.answer(f"{msg}\nВсего за день: {sum(top.values())}")


@dp.message_handler(commands=['farm'])
async def farm(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")
    ...


@dp.message_handler(commands=['search'])
async def search(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")
    ...


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
