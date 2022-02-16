from aiogram.dispatcher import FSMContext # хендлеры машины состояний
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from function import deltatime, cwt
from aiogram.dispatcher.filters import Text

class FSMadmin (StatesGroup):
    date_1 = State() #состояние бота
    date_2 = State()
    result = State()
    result_2 = State()
    count_peopl = State()

# Начало диалога подсчета даты
#@dp.message_handler(commands='Считать', state=None)
async def cm_start(message: types.Message):
    await FSMadmin.date_1.set()
    await message.reply('Введие первую дату')

# ловим первую дату
#@dp.message_handler(content_types=['date_1'], state=FSMadmin.date_1)
async def load_1date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date_1'] = message.text
    await FSMadmin.next()
    await message.reply('Введие вторую дату.')

# ловим вторую дату
#@dp.message_handler(state=FSMadmin.date_2)
async def load_2date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date_2'] = message.text
    await FSMadmin.result.set()
    await message.reply('Если хотите узнать результат введиете "/Результат"\n\
Если хотите посчитать чел/дни (чел/час) введите "/Продолжить"')

async def reset(message: types.Message, state: FSMContext):
    if message.text == '/Результат': # Text(equals='/Результат', ignore_case=True):
        async with state.proxy() as data:
            await message.reply(deltatime(str(data['date_1']), str(data['date_2'])))
        await FSMadmin.result_2.set()
        await message.reply('Если хотите посчитать чел/дни (чел/час) введите "Продолжить"\n\
        Если хотите начать заново введите "Считать"')
    elif message.text == '/Продолжить': # Text(equals='/Продолжить', ignore_case=True):
        await FSMadmin.count_peopl.set()
        await message.reply('Введие количество людей')

# ловим хендлер для "Результата"
#@dp.message_handler(commands='Результат', state=FSMadmin.result)
# async def load_result(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         await message.reply(str(data))
#
#     async with state.proxy() as data:
#         await message.reply(deltatime(str(data['date_1']), str(data['date_2'])))
#     await state.reset_state(with_data=False)
#     await message.reply('Если хотите начать заново введите "/Считать"')
#
#
# # ловим ловим хендлер "Продолжить"
# #@dp.message_handler(commands='Продолжить', state=FSMadmin.result)
async def cm_count(message: types.Message):
    await FSMadmin.count_peopl.set()
    await message.reply('Введие количество людей')


#@dp.message_handler(state=FSMadmin.count_peopl)
async def load_result2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count_peopl'] = message.text
        await message.reply(cwt(str(data['date_1']), str(data['date_2']), int(data['count_peopl'])))
    await state.finish()

# вывод из состояний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')

# регстрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Считать', state="*")
    dp.register_message_handler(load_1date, state=FSMadmin.date_1)
    dp.register_message_handler(load_2date, state=FSMadmin.date_2)
    dp.register_message_handler(reset, commands=['Результат', 'Продолжить'], state=FSMadmin.result)
    # dp.register_message_handler(load_result, commands='Результат', state=FSMadmin.result)
    dp.register_message_handler(cm_count, commands='Продолжить', state=FSMadmin.result_2)
    dp.register_message_handler(load_result2, state=FSMadmin.count_peopl)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
