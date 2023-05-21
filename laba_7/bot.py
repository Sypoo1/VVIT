import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message

from cfg import Bot_Token
from database import get_schedule
from logic import get_date, sort_data, which_day_logic

TOKEN = Bot_Token

router = Router()

@router.message(Command(commands=["start"]))
async def command_start_handler(message):

    await message.answer(f"Здравствуйте, <b>{message.from_user.full_name}!</b> Чтобы узнать больше о боте, воспользуйтесь командой /help")
    
@router.message(Command(commands=["Commands"]))
async def command_Commands_handler(message):
    
    kb = [
        [
            types.KeyboardButton(text="Понедельник"),
            types.KeyboardButton(text="Вторник")
        ],
        [
            types.KeyboardButton(text="Среда"),
            types.KeyboardButton(text="Четверг")
        ],
        [
            types.KeyboardButton(text="Пятница"),
            types.KeyboardButton(text="Суббота")
        ],
        [
            types.KeyboardButton(text="Расписание на текущую неделю", ),
            types.KeyboardButton(text="Расписание на следующую неделю")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите период, на который хотите узнать расписание"
    )
    await message.answer("На какой период вывести расписание?", reply_markup=keyboard)


    
@router.message(Command(commands=['week']))
async def command_week_handler(message):
    
    week = get_date()
    await message.answer(week)
    
@router.message(Command(commands=['mtuci']))
async def command_mtuci_handler(message):

    await message.answer('https://mtuci.ru/')
    
@router.message(Command(commands=['help']))
async def command_help_handler(message):
    ans = 'Приветствую вас, я - бот для просмотра расписания, написанный на aiogram.' + '\n' 
    ans += 'Структура проекта состоит из 4 файлов, cfp.py содержит токен и пароль от бд, в database.py находится подключение к бд и работа с ней,\
        в logic.py написаны вспомогательные функции для работы с данными и датой и в файле bot.py собраны все основные функции,\
            а также импортированы модули из предыдуших файлов, для запуска бота нужно запустить файл bot.py \n'
    ans += 'Нажав /Commands появится клавиатура с днями недели, нажмите на интересующий вас период времени и получите расписание на него,\
        /mtuci выведет ссылку на сайт МТУСИ, /week подскажет какая сейчас неделя'
    await message.answer(ans)


@router.message()
async def msg_handler(message):
    
    try:
        if message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Расписание на текущую неделю', 'Расписание на следующую неделю']:
            await command_shedule_handler(message)
        else:
            await message.answer('Извините, я Вас не понял')
    except TypeError:
        await message.answer("Nice try!")

@router.message()
async def command_shedule_handler(message):
    
    week = get_date()
    data = sort_data(get_schedule())
    msg = message.text
    ans = which_day_logic(week, data, msg)
    
    await message.answer(ans)


async def main():

    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())