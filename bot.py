import datetime
import re

import telebot
from telebot import types

import config
from data import track_information_output
from menu import keyboard_menu
from sql import delete_track, read_all_user_tracks

bot = telebot.TeleBot(config.TOKEN)

track_number = ''
description = ''


def removing_spaces_in_track_number(track_number: str) -> str:
    """ Удаляет пробелы в треке"""
    return re.sub(r'\s+', '', track_number, flags=re.UNICODE)


def date_formatting(date: str):
    """ Форматирует дату """
    date_format = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    day = date_format.day
    month = date_format.month
    year = date_format.year
    hour = date_format.hour
    minute = date_format.minute
    return f'{day}.{month}.{year} {hour}:{minute}'


def filtering_messages(message: str) -> bool:
    """ Фильтрует ключевые слова """
    result = False
    messages_list = [
        '/start', '➕ Добавить', '⚙ Управлять', '⛔ Отменить'
    ]
    if message in messages_list:
        result = True
    return result


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Выберите действие 👇', reply_markup=keyboard_menu('menu'))


@bot.message_handler(content_types='text')
def message_reply_start(message):
    if filtering_messages(message.text):
        userId = message.from_user.id
        if message.text == "➕ Добавить":
            bot.send_message(message.chat.id, 'Введите трек:', reply_markup=keyboard_menu('cancel'))
            bot.register_next_step_handler(message, track_description)
        if message.text == "⚙ Управлять":
            records = read_all_user_tracks(userId)
            bot.send_message(message.chat.id, 'Список треков:', reply_markup=keyboard_menu('menu'))
            for row in records:
                track_num = row[0]
                track_desc = row[1]
                track_date = date_formatting(row[2])
                otvet = types.InlineKeyboardMarkup(row_width=2)
                button1 = types.InlineKeyboardButton("ℹ", callback_data='inf_' + track_num)
                button2 = types.InlineKeyboardButton("❌", callback_data='del_' + track_num)
                otvet.add(button1, button2)
                bot.send_message(message.chat.id, f'Номер: {track_num}\nОписание: {track_desc}\nСоздано: {track_date}',
                                 reply_markup=otvet)
    else:
        bot.send_message(message.chat.id, 'Неверная команда.', reply_markup=keyboard_menu('menu'))


def track_description(message):
    global track_number
    track_number = removing_spaces_in_track_number(message.text)
    if message.text == "⛔ Отменить":
        bot.send_message(message.chat.id, 'Действие отменено.', reply_markup=keyboard_menu('menu'))
    else:
        bot.send_message(message.chat.id, 'Введите описание:', reply_markup=keyboard_menu('cancel'))
        bot.register_next_step_handler(message, track_info)


def track_info(message):
    global description
    description = message.text
    if message.text == "⛔ Отменить":
        bot.send_message(message.chat.id, 'Действие отменено.', reply_markup=keyboard_menu('menu'))
    else:
        user_id = message.from_user.id
        text = track_information_output(track_number, user_id, description)
        bot.send_message(user_id, text, reply_markup=keyboard_menu('menu'))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    command = str(call.data)[0:3]
    trackNumber = str(call.data)[4:]
    user_id = call.from_user.id
    if command == 'del':
        delete_track(trackNumber, user_id)
        bot.send_message(call.message.chat.id, "Отправление " + trackNumber + " удалено.")
    if command == 'inf':
        data = track_information_output(trackNumber, user_id, description)
        bot.send_message(call.message.chat.id, data)
