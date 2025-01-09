from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = '7871547121:AAGRL7UiWIcLuazGuA8gZ32KdbQ7_E9NVhE'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'),
     KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить')]
], resize_keyboard=True)

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий',
                          callback_data='calories'),
     InlineKeyboardButton(text='Формулы расчёта',
                          callback_data='formulas')]
])

goods_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Product1',
                         callback_data='product_buying'),
    InlineKeyboardButton(text='Product2',
                         callback_data='product_buying'),
    InlineKeyboardButton(text='Product3',
                         callback_data='product_buying'),
    InlineKeyboardButton(text='Product4',
                         callback_data='product_buying')
]])

gen_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Для мужчин'),
     KeyboardButton(text='Для женщин')]
    ], resize_keyboard=True)


class UserState(StatesGroup):
    '''
    UserState  для определения группы состояний пользователя в Telegram-боте
    Объекты класса State
    age возраст
    groth рост
    weght вес
    '''
    age: int = State()
    growth: int = State()
    weight: int = State()
    gender: str = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий вашему здоровью.'
                         ' Нажмите "Рассчитать", чтобы узнать вашу суточную норму'
                         ' потребления килокалорий', reply_markup=kb)


@dp.message_handler(text=['Информация'])
async def info(message):
    await message.answer('Бот подсчитывает норму потребления калорий для мужчин/женщин по'
                         ' упрощённой формуле Миффлина - Сан Жеора'
                         ' (https://www.calc.ru/Formula-Mifflinasan-Zheora.html).')


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=inline_kb)


@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer(f'Для мужчин:\n\t'
                                 f'10*вес + 6.25*рост - 5*возраст + 5\n'
                                 f'Для женщин:\n\t'
                                 f'10*вес + 6.25*рост - 5*возраст -161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def calories(call):
    await call.message.answer('Введите свой возраст (полных лет):')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_age(message, state):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await message.answer('Введите свой рост (см):')
        await UserState.growth.set()
    else:
        await message.answer('Пожалуйста, введите число.')


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    if message.text.isdigit():
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес (кг):')
        await UserState.weight.set()
    else:
        await message.answer('Пожалуйста, введите корректное число.')


@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Выбрать категорию',reply_markup=gen_menu)
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    await state.update_data(gender=message.text)
    data_quest = await state.get_data()

    if data_quest['gender'] == 'Для мужчин':
        result = 10 * int(data_quest['weight']) + \
                 6.25 * int(data_quest['growth']) - \
                 5 * int(data_quest['age']) + 5
        gend = data_quest['gender'].lower()

    elif data_quest['gender'] == 'Для женщин':
        result = 10 * int(data_quest['weight']) + \
        6.25 * int(data_quest['growth']) - \
        5 * int(data_quest['age']) - 161

        gend = data_quest['gender'].lower()

    await message.answer(f'Ваша норма калорий: {result} ккал в сутки {gend}',
                         reply_markup=ReplyKeyboardRemove())

    await state.finish()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f'Название: Product{i} | '
                             f'Описание: описание {i} | '
                             f'Цена: {i * 100}')
        with open(f'{i}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:',
                         reply_markup=goods_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)