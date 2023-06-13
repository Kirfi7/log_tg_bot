from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from crud import get_top, true_value, true_params, get_online, get_stats_text
from cfg import access, token, req_types, top_commands
from table import get_admin_list


bot = Bot(token=token, parse_mode='html')
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class Date(StatesGroup):
    date = State()
    params = State()


class Online(StatesGroup):
    date = State()
    time = State()


class Ban(StatesGroup):
    date = State()


class StatsDate(StatesGroup):
    date = State()


@dp.message_handler(commands=['jails', 'mutes', 'kicks', 'events', 'reports', 'questions'] + top_commands)
async def get_date(message: types.Message, state: FSMContext):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")

    async with state.proxy() as data:
        data['request'] = req_types[message.text]

    if message.text[1:] in top_commands:
        await Date.params.set()
        return await message.answer("Укажите параметры в следующем формате: первое_место-вычет | Пример: 500-100")

    await Date.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-день | Пример: 01-30"
    )


@dp.message_handler(state=Date.params)
async def get_params(message: types.Message, state: FSMContext):
    await Date.params.set()

    if not await true_params(message.text):
        return await message.answer("Указаны недопустимые значения.")

    async with state.proxy() as data:
        data['params'] = message.text.split('-')

    await Date.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-день | Пример: 01-30"
    )


@dp.message_handler(state=Date.date)
async def get_list(message: types.Message, state: FSMContext):
    await Date.date.set()

    if not await true_value(message.text, "-"):
        await state.finish()
        return await message.answer("Указаны недопустимые значения.")

    async with state.proxy() as data:
        req = data['request']
        params = data['params'] if "params" in data else False

    await state.finish()
    await message.answer(await get_top(date=message.text, **req, params=params))


@dp.message_handler(commands=['bans', 'top_bans'])
async def get_bans(message: types.Message, state: FSMContext):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")

    async with state.proxy() as data:
        data['request'] = req_types[message.text]

    await Ban.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-день | Пример: 01-30"
    )


@dp.message_handler(commands=['online'])
async def get_date(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")

    await Online.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-день | Пример: 01-30"
    )


@dp.message_handler(state=Online.date)
async def get_time(message: types.Message, state: FSMContext):
    await Online.date.set()

    if not await true_value(message.text, "-"):
        await state.finish()
        return await message.answer("Указаны недопустимые значения.")

    async with state.proxy() as data:
        data['date'] = message.text

    await Online.time.set()
    await message.answer("Укажите время, за которое хотите получить выгрузку в формате часы:минуты | Пример: 23:59")


@dp.message_handler(state=Online.time)
async def get_list(message: types.Message, state: FSMContext):
    await Online.time.set()

    if not await true_value(message.text, ":"):
        await state.finish()
        return await message.answer("Указаны недопустимые значения.")

    async with state.proxy() as data:
        date = data['date']

    online_list = await get_online(await get_admin_list(), date=date, time=message.text)

    await state.finish()
    await message.answer("Список админов онлайн:\n\n" + "\n".join(online_list))


@dp.message_handler(commands=['stats'])
async def server_info(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")

    await StatsDate.date.set()
    await message.answer(
        "Укажите дату, за которую хотите получить выгрузку в следующем формате: месяц-день | Пример: 01-30"
    )


@dp.message_handler(state=StatsDate.date)
async def server_info(message: types.Message, state: FSMContext):
    await StatsDate.date.set()
    await state.finish()
    await message.answer(await get_stats_text(message.text))


@dp.message_handler(commands=['casino'])
async def check_casino(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")
    ...


@dp.message_handler(commands=['search'])
async def search(message: types.Message):

    if message.from_user.id not in access:
        return await message.answer("У вас нет доступа к использованию бота!")
    ...


@dp.message_handler(commands=['farm'])
async def farm(message: types.Message):

    if message.from_user.id not in [1831358099, 777198928]:
        return
    ...


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
