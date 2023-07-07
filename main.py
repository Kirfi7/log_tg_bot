from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from crud import *
from buttons import *
from cfg import *
# 1

bot = Bot(token=token, parse_mode='html')
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class TopState(StatesGroup):
    date = State()
    param = State()
    top_type = State()


class MainStats(StatesGroup):
    param = State()
    logs = State()
    online = State()
    helpers = State()
    stats_date = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id in access:
        await bot.send_message(message.from_user.id, "Выберите действие", reply_markup=menu)


@dp.message_handler(commands=['session'])
async def set_session(message: types.Message):
    if message.from_user.id not in access:
        return
    array = message.text.split()
    if len(array) == 2:
        await set_session_id(array[1])
        return await message.reply("ID сессии успешно установлен!")
    await message.reply("Укажите ID сессии через пробел после команды.")


@dp.message_handler(content_types=['text'])
async def select_type(message: types.Message, state: FSMContext):

    text, user = message.text, message.from_user.id
    if user not in access:
        return

    if text == "Основные выгрузки":
        await message.answer("Выберите тип выгрузки", reply_markup=main_markup)
        await MainStats.param.set()
    if text in ["Сформировать топ", "Поощрение по топу"]:
        await message.answer("Выберите тип выгрузки", reply_markup=top_markup)
        await TopState.top_type.set()
        async with state.proxy() as data:
            data['type'] = text


@dp.message_handler(state=MainStats.param)
async def get_main_date(message: types.Message, state: FSMContext):
    await MainStats.param.set()
    text = message.text

    if text == "Статистика по серверу":
        await MainStats.stats_date.set()
        await message.reply(date_message, reply_markup=get_keyboard())
    elif text == "Количество логов":
        await MainStats.logs.set()
        await message.reply(logs_message, reply_markup=get_logs_keyboard())
    elif text == "Агенты поддержки":
        await message.answer("Статистика агентов поддержки:\n\n" + await get_helpers_stats(), reply_markup=menu)
        await state.finish()
    elif text == "Онлайн админов":
        await MainStats.online.set()
        await message.reply(datetime_message, reply_markup=types.ReplyKeyboardRemove())
    elif text == "В главное меню":
        await state.finish()
        await start(message)
    else:
        await message.reply("Указан некорректный тип!")
        await state.finish()
        await start(message)


@dp.message_handler(state=MainStats.stats_date)
async def get_stats(message: types.Message, state: FSMContext):
    await MainStats.stats_date.set()
    if not await true_date(message.text):
        if message.text == "В главное меню":
            await start(message)
            return await state.finish()
        await message.reply("Указаны неверные значения!", reply_markup=menu)
        return await state.finish()
    await message.answer(await get_stats_text(message.text), reply_markup=menu)
    await state.finish()


@dp.message_handler(state=MainStats.logs)
async def get_logs(message: types.Message, state: FSMContext):
    await MainStats.logs.set()
    if not await true_date(message.text):
        await message.reply("Указаны неверные значения!", reply_markup=menu)
        return await state.finish()
    await message.answer(await get_chief_logs(message.text), reply_markup=menu)
    await state.finish()


@dp.message_handler(state=MainStats.online)
async def get_admins_online(message: types.Message, state: FSMContext):
    await MainStats.online.set()
    if not await true_time(message.text):
        await message.reply("Указаны неверные значения!", reply_markup=menu)
        return await state.finish()
    await message.answer("Список админов онлайн:\n\n" + "\n".join(await get_online(*message.text.split())), reply_markup=menu)
    await state.finish()


@dp.message_handler(state=TopState.top_type)
async def get_top_type(message: types.Message, state: FSMContext):
    await TopState.top_type.set()
    if message.text not in req_types:
        if message.text == "В главное меню":
            await start(message)
            return await state.finish()
        await state.finish()
        return await message.reply("Указан неверный тип выгрузки!")
    async with state.proxy() as data:
        data['request'] = req_types[message.text]
        is_top = True if data['type'] == "Поощрение по топу" else False
    if is_top and message.text != "Баны":
        await message.reply(param_message, reply_markup=param_markup)
        return await TopState.param.set()
    elif is_top and message.text == "Баны":
        ...
    await message.reply(date_message, reply_markup=get_keyboard())
    await TopState.date.set()


@dp.message_handler(state=TopState.param)
async def get_param(message: types.Message, state: FSMContext):
    await TopState.param.set()
    if not await true_params(message.text):
        if message.text == "В главное меню":
            await start(message)
            return await state.finish()
        await message.reply("Указаны неверные значения!", reply_markup=menu)
        return await state.finish()
    async with state.proxy() as data:
        data['params'] = message.text.split()
    await message.answer(date_message, reply_markup=get_keyboard())
    await TopState.date.set()


@dp.message_handler(state=TopState.date)
async def get_date(message: types.Message, state: FSMContext):
    await TopState.param.set()
    if not await true_date(message.text):
        if message.text == "В главное меню":
            await start(message)
            return await state.finish()
        await message.reply("Указаны неверные значения!", reply_markup=menu)
        return await state.finish()
    async with state.proxy() as data:
        params = data['params'] if "params" in data else False
        req = data['request']
    await message.answer(await get_top(date=message.text, **req, params=params), reply_markup=menu)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
