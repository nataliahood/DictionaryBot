# В google colab добавить: !pip install pyTelegramBotAPI

import telebot
from telebot import types
import json
import random

bot = telebot.TeleBot(token='Вставь_токен', parse_mode='html')

with open('dict.json', "r", encoding="utf-8") as json_file:
    DEFINITIONS = json.load(json_file)

listDEFINITIONS = list(DEFINITIONS.values())

newDEFINITIONS = []

@bot.message_handler(commands=['start'])
def start_command_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Случайные термины✨')
    item2 = types.KeyboardButton('Кто тебя создал?')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я помогу тебе разобраться с базовыми понятиями в тестировании сервисов Яндекса 🤓 \nВведи интересующий термин, например, <u><b>регресс</b></u>", parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text != "Случайные термины✨" and message.text != "Кто тебя создал?":
        definition = DEFINITIONS.get(message.text.lower())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Случайные термины✨')
        item2 = types.KeyboardButton('Кто тебя создал?')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, text=f'Определение:\n<code>{definition}</code>')
        bot.send_message(message.chat.id, text=f'Хочешь узнать что нибудь другое?', reply_markup=markup)
        if definition is None and message.text != "Случайные термины✨" and message.text != "Кто тебя создал?":
            newDEFINITIONS.append(message.text)
            with open('newdict.txt', "a", encoding="utf-8") as txt_file:
                print(*newDEFINITIONS, file=txt_file, sep="\n")
            bot.send_message(message.chat.id, f'Кажется, этого определения у меня еще нет🤔\nЯ добавлю термин <u><b>{message.text}</b></u> в свой список и обязательно узнаю что это такое🤓')

    elif message.text == "Случайные термины✨":
        bot.send_message(message.chat.id, random.choice(listDEFINITIONS))
        bot.send_message(message.chat.id, random.choice(listDEFINITIONS))
        bot.send_message(message.chat.id, random.choice(listDEFINITIONS))
        bot.send_message(message.chat.id, random.choice(listDEFINITIONS))
        bot.send_message(message.chat.id, random.choice(listDEFINITIONS))

    elif message.text == "Кто тебя создал?":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Сайт-визитка', url='https://nataliahood.ru/')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Тебе правда интересно?☺ Переходи по ссылке!'.format(message.from_user), reply_markup=markup)

def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
