from aiogram.dispatcher import FSMContext # хендлеры машины состояний
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from function import deltatime, cwt
from aiogram.dispatcher.filters import Text
from re import fullmatch
import string
from keyboards import kb_dc
from date_base.sqlite_db import sql_add_command

class FSMadmin (StatesGroup):
    date_1 = State() #состояние бота
    date_2 = State()
    result = State()
    count_peopl = State()

# Начало диалога подсчета даты
#@dp.message_handler(commands='Считать', state=None)
async def cm_start(message: types.Message):
    await FSMadmin.date_1.set()
    await message.reply('Введие первую дату в формате дд.мм.гггг\n\
Если хотите начать заново введите "Отмена"', reply_markup=kb_dc)

# функция для инлайт кнопки
async def cm_start2(message: types.Message):
    await FSMadmin.date_1.set()
    await message.message.answer('Введие первую дату в формате дд.мм.гггг\n\
Если хотите начать заново введите "Отмена"', reply_markup=kb_dc)
    await message.answer()

# вывод из состояний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=types.ReplyKeyboardRemove())

# ловим первую дату
#@dp.message_handler(content_types=['date_1'], state=FSMadmin.date_1)
async def load_1date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not fullmatch(r"(?<!\d)(?:0?[1-9]|[12][0-9]|3[01]).(?:0?[1-9]|1[0-2]).(?:19[0-9][0-9]|20[0-9][0-9])(?!\d)", message.text):
            await message.reply('Пожалуйста. Введие дату в формате дд.мм.гггг')
            return
        data['user_name'] = message.from_user.id
        data['date_1'] = message.text
    await FSMadmin.next()
    await message.reply('Введие вторую дату в формате дд.мм.гггг\n\
Если хотите начать заново введите "Отмена"', reply_markup=kb_dc)

# ловим вторую дату
#@dp.message_handler(state=FSMadmin.date_2)
async def load_2date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not fullmatch(r"(?<!\d)(?:0?[1-9]|[12][0-9]|3[01]).(?:0?[1-9]|1[0-2]).(?:19[0-9][0-9]|20[0-9][0-9])(?!\d)", message.text):
            await message.reply('Пожалуйста. Введие дату в формате дд.мм.гггг')
            return
        data['date_2'] = message.text
    await FSMadmin.result.set()
    await message.reply('Если хотите узнать результат введиете "/Результат"\n\
Если хотите посчитать чел/дни (чел/час) введите "/Продолжить"', reply_markup=kb_dc)

async def reset(message: types.Message, state: FSMContext):
    if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(['результат']) != set():
        async with state.proxy() as data:
            data['result_1'] = deltatime(str(data['date_1']), str(data['date_2']))
            await message.reply(data['result_1'])
        # await FSMadmin.count_peopl.set()
        await message.reply('Если хотите посчитать чел/дни (чел/час) введите "Продолжить"\n\
Если хотите начать заново введите "Отмена"', reply_markup=kb_dc)
    else:
        await FSMadmin.count_peopl.set()
        await message.reply('Введие количество людей')


#@dp.message_handler(state=FSMadmin.count_peopl)
async def load_result2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not fullmatch(r"\b\d{1,2}\b", message.text):
            await message.reply('Пожалуйста, введие количестово людей целым числом не более 2х знаков')
            return
        data['count_peopl'] = message.text
        data['result_2'] = cwt(str(data['date_1']), str(data['date_2']), int(data['count_peopl']))
        await message.reply(data['result_2'])

    # await sql_add_command(state)
    await state.finish()



# регстрируем хендлеры
def register_handlers_dc(dp: Dispatcher):
    dp.register_callback_query_handler(cm_start2, text='Считать', state=None)
    dp.register_message_handler(cm_start, commands='Считать', state=None)
    dp.register_message_handler(cm_start, Text(equals='считать', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_1date, state=FSMadmin.date_1)
    dp.register_message_handler(load_2date, state=FSMadmin.date_2)
    dp.register_message_handler(reset, commands=['Результат', 'Продолжить'], state=FSMadmin.result)
    dp.register_message_handler(reset, Text(equals=['результат', 'продолжить'], ignore_case=True), state=FSMadmin.result)
    dp.register_message_handler(load_result2, state=FSMadmin.count_peopl)

