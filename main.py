from request import get_link, get_response
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from cfg import access, token


bot = Bot(token=token, parse_mode='html')
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class Jails(StatesGroup):
    date = State()


class Mutes(StatesGroup):
    date = State()


@dp.message_handler(commands=['jails'])
async def get_date(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")

    await Jails.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-день. Пример: 01-30"
    )


@dp.message_handler(state=Jails.date)
async def get_jails(message: types.Message, state: FSMContext):
    await Jails.date.set()
    jails = {}
    offset = 0
    while True:

        link = get_link(date=message.text, description='Посадил в деморган игрока', category=41, offset=offset)
        response = get_response(link)

        for tup in response:
            if tup["player_name"] in jails:
                jails[tup["player_name"]] += 1
            else:
                jails[tup["player_name"]] = 1

        if len(response) == 200:
            offset += 200
            continue
        break

    msg, k = "", 0
    top = dict(sorted(jails.items(), key=lambda item: item[1], reverse=True))

    for key in top:
        k += 1
        msg += f"{k}. {key}: {top[key]}\n"

    await state.finish()
    await message.answer(msg)


@dp.message_handler(commands=['mutes'])
async def get_date(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")

    await Mutes.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: Месяц-День. Пример: 01-30"
    )


@dp.message_handler(state=Mutes.date)
async def get_mutes(message: types.Message, state: FSMContext):
    await Mutes.date.set()
    mutes = {}
    offset = 0
    while True:

        link = get_link(date=message.text, description='Выдал мут игроку', category=41, offset=offset)
        response = get_response(link)

        for tup in response:
            if tup["player_name"] in mutes:
                mutes[tup["player_name"]] += 1
            else:
                mutes[tup["player_name"]] = 1

        if len(response) == 200:
            offset += 200
            continue
        break

    msg, k = "", 0
    top = dict(sorted(mutes.items(), key=lambda item: item[1], reverse=True))

    for key in top:
        k += 1
        msg += f"{k}. {key}: {top[key]}\n"

    await state.finish()
    await message.answer(msg)


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
