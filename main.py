import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.methods import SendMessage, SendPhoto
from aiogram.types import URLInputFile

from aiogram.fsm.state import State, StatesGroup
from aiogram import F


START_MESSAGE = '''Привет! Я виртуальный помощник сообщества KIR AVTO.
Добро пожаловать в наши ряды! Я задам тебе пару вопросов и напишу приветствие, с которым ты сможешь зайти в общий чат. Готов?'''


class Questions(StatesGroup):
    name = 'Твои фамилия и имя?'
    city = 'Из какого ты города?'
    company = 'Как называется твоя компания?'
    spec = 'Основная специализация твоей компании?'
    years_in_business = 'Сколько лет ты в автобизнесе?'
    auto_on_storage = 'Сколько автомобилей у тебя на складе?'
    people_in_team = 'Сколько человек у тебя в команде?'
    strong_sides = 'В чем твои сильные стороны? Какие основные компетенции ты можешь выделить, которыми готов делиться с другими участниками?'
    main_courses = 'Твои основные цели на Мастермайнд?'
    phone_number = 'Поделись контактами! Твой номер телефона?'
    telegram = 'Твой телеграм?'
    instagram = 'Твой инст?'
    photo = 'Почти готово, осталось только фото'
    final = 'Большое тебе спасибо за ответы на мои вопросы! Твое приветствие почти готово'


class Answers(StatesGroup):
    name = State()
    city = State()
    company = State()
    spec = State()
    years_in_business = State()
    auto_on_storage = State()
    people_in_team = State()
    strong_sides = State()
    main_courses = State()
    phone_number = State()
    telegram = State()
    instagram = State()
    photo = State()


BOT_TOKEN = '6949295099:AAEOZnpy5D3A_fLS-hRiFx5e0JDBBZ8N834'
dp = Dispatcher()

START_BUTTON = [[InlineKeyboardButton(text="Да", callback_data='start')]]


@dp.message(CommandStart())
async def start_handler(message: Message):
    """
    This handler receives messages with `/start` command
    """

    reply_markup = InlineKeyboardMarkup(
                            inline_keyboard=[[
                                InlineKeyboardButton(text="Да",
                                                     callback_data=f'start {message.chat.id}')]])

    await bot(SendPhoto(chat_id=message.chat.id,
                        photo=URLInputFile("https://i.imgur.com/qR3EAV6.png"),
                        caption=START_MESSAGE,
                        reply_markup=reply_markup))


@dp.callback_query()
async def ask(callback: types.CallbackQuery, state: FSMContext) -> None:
    '''
    This function gets callback
    And starts to ask a questions
    '''

    # Get the current channel id to send message
    channel_id = callback.data.split()[1]

    # Set name state to FSM
    await state.set_state(Answers.name)

    # Sends message from Questions FSM
    await bot(SendMessage(chat_id=channel_id, text=Questions.name))


@dp.message(Answers.name)
async def process_name(message: Message, state: FSMContext) -> None:
    '''
    Process name from message
    '''

    # Update data in Answers with current state (name)
    await state.update_data(name=message.text)

    # Set next state (city)
    await state.set_state(Answers.city)

    # Send message to user, with question from Questions FSM
    await message.reply(text=Questions.city)


@dp.message(Answers.city)
async def process_city(message: Message, state: FSMContext) -> None:
    '''
    Process city from message
    '''
    await state.update_data(city=message.text)
    await state.set_state(Answers.company)
    await message.reply(text=Questions.company)


@dp.message(Answers.company)
async def process_company(message: Message, state: FSMContext) -> None:
    '''
    Process company from message
    '''
    await state.update_data(company=message.text)
    await state.set_state(Answers.spec)
    await message.reply(text=Questions.spec)


@dp.message(Answers.spec)
async def process_spec(message: Message, state: FSMContext) -> None:
    '''
    Process company spec from message
    '''
    await state.update_data(spec=message.text)
    await state.set_state(Answers.years_in_business)
    await message.reply(text=Questions.years_in_business)


@dp.message(Answers.years_in_business)
async def process_years_in_business(message: Message, state: FSMContext) -> None:
    '''
    Process years in business from message
    '''
    try:
        int(message.text)
        await state.update_data(years_in_business=message.text)
        await state.set_state(Answers.auto_on_storage)
        await message.reply(text=Questions.auto_on_storage)
    except ValueError as e:
        print(e)
        await message.reply(text='Введите коректное значение')



@dp.message(Answers.auto_on_storage)
async def process_auto_on_storage(message: Message, state: FSMContext) -> None:
    '''
    Process auto on storage from message
    '''
    try:
        int(message.text)
        await state.update_data(auto_on_storage=message.text)
        await state.set_state(Answers.people_in_team)
        await message.reply(text=Questions.people_in_team)
    except ValueError as e:
        print(e)
        await message.reply(text='Введите коректное значение')


@dp.message(Answers.people_in_team)
async def process_people_in_team(message: Message, state: FSMContext):
    '''
    Process people in team from message
    '''
    try:
        int(message.text)
        await state.update_data(people_in_team=message.text)
        await state.set_state(Answers.strong_sides)
        await message.reply(text=Questions.strong_sides)
    except ValueError as e:
        print(e)
        await message.reply(text='Введите коректное значение')


@dp.message(Answers.strong_sides)
async def process_strong_sides(message: Message, state: FSMContext):
    '''
    Process strong sides from message
    '''
    await state.update_data(strong_sides=message.text)
    await state.set_state(Answers.main_courses)
    await message.reply(text=Questions.main_courses)


@dp.message(Answers.main_courses)
async def process_main_courses(message: Message, state: FSMContext):
    '''
    Process main courses from message
    '''
    await state.update_data(main_courses=message.text)
    await state.set_state(Answers.phone_number)
    await message.reply(text=Questions.phone_number)


@dp.message(Answers.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    '''
    Process phone number from message
    '''
    await state.update_data(phone_number=message.text)
    await state.set_state(Answers.telegram)
    await message.reply(text=Questions.telegram)


@dp.message(Answers.telegram)
async def process_telegram(message: Message, state: FSMContext):
    '''
    Process telegram from message
    '''
    await state.update_data(telegram=message.text)
    await state.set_state(Answers.instagram)
    await message.reply(text=Questions.instagram)


@dp.message(Answers.instagram)
async def process_instagram(message: Message, state: FSMContext):
    '''
    Process instagram from message
    '''
    await state.update_data(instagram=message.text)
    await state.set_state(Answers.photo)
    await message.reply(text=Questions.photo)


@dp.message(Answers.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    '''
    Process photo from message
    '''

    photos = message.photo

    await state.update_data(photo=photos)
    try:
        await process_final(message, state)
        await bot(SendMessage(chat_id=message.chat.id,
                              text='''Отлично!

Добавляйся в чат сообщества и размещай свою визитку в теме "Представления резидентов".
https://t.me/+KkAHWL-GzM03YjQy'''))
    except ValueError as e:
        print(e)
        await message.reply(
            text='Возникла ошибка ввода')


async def process_final(message: Message, state: FSMContext):
    '''
    Creating of final message
    '''

    final_message = '''
Всем привет!

Меня зовут name. Я из city.
Моя компания называется company, основная специализация - spec.
Я в автобизнесе years_in_business, у меня на складе auto_on_storage, в моей команде работает people_in_team сотрудников.

Мои основные компетенции: strong_sides
Мои цели: main_courses

Мои контакты:
phone_number
telegram
instagram
'''
    user_data = await state.get_data()

    if int(user_data['years_in_business']) in [1, 21, 31, 41, 51,
                                               61, 71, 81, 91, 101]:
        user_data['years_in_business'] += ' год'
    elif int(user_data['years_in_business']) in (list(range(2, 5)),
                                                 list(range(22, 25)),
                                                 list(range(32, 35)),
                                                 list(range(42, 45)),
                                                 list(range(52, 55)),
                                                 list(range(62, 65)),
                                                 list(range(72, 75)),
                                                 list(range(82, 85)),
                                                 list(range(92, 95)),
                                                 list(range(102, 105))):
        user_data['years_in_business'] += ' года'
    else:
        user_data['years_in_business'] += ' лет'

    if int(user_data['auto_on_storage']) in [1, 21, 31, 41, 51,
                                             61, 71, 81, 91, 101]:
        user_data['auto_on_storage'] += ' машина'
    elif int(user_data['auto_on_storage']) in (list(range(2, 5)),
                                               list(range(22, 25)),
                                               list(range(32, 35)),
                                               list(range(42, 45)),
                                               list(range(52, 55)),
                                               list(range(62, 65)),
                                               list(range(72, 75)),
                                               list(range(82, 85)),
                                               list(range(92, 95)),
                                               list(range(102, 105))):
        user_data['auto_on_storage'] += ' машины'
    else:
        user_data['auto_on_storage'] += ' машин'

    for key in list(user_data.keys())[:-1]:
        final_message = final_message.replace(str(key), user_data[key])
    print(final_message)
    await bot.send_photo(message.chat.id, 
                         photo=message.photo[0].file_id,
                         caption=final_message)


async def main() -> None:
    '''Initialize Bot instance with a default
    parse mode which will be passed to all API calls '''

    global bot
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Start logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Start bot running
    asyncio.run(main())
