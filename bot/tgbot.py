import os
import telebot
import random
import sqlite3
import time

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import apihelper

API_TOKEN = "7749352058:AAHYoc1Ku-3_1RvKcRY9r1qtmpc_xk_xgc0"
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(
        message,
        f"💬 Привет, сладенький! Я твой личный клубничный помощник 🍓 Чтобы узнать больше, введи команду /info"
    )

@bot.message_handler(commands=['info'])
def info_handler(message):
    msg = bot.reply_to(
        message,
        "✨ StrawberryBest — сообщество вдохновлённых жизнью людей... ⚠️"
    )
    
    time.sleep(0.5)
    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text="✨ StrawberryBest — сообщество вдохновлённых жизнью людей. Мы влюблены в клубнику... ⚠️"
        )
        time.sleep(0.5)
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text="✨ StrawberryBest — сообщество вдохновлённых жизнью людей. Мы верим в личностный рост, саморазвитие, красоту и добро. Присоединяйся! Введи команду /join 🎀"
        )
    except:
        pass


@bot.message_handler(commands=['join'])
def start_handler(message):
    bot.reply_to(
        message,
        f"Ты только что сделал(а) шаг, который точно перевернет твою жизнь! В скором времени с тобой свяжется наш менеджер по встречам. Мы рады, что ты теперь с нами 💖"
    )


@bot.message_handler(commands=['faq'])
def faq_handler(message):
    bot.reply_to(
        message,
        "❓ Часто задаваемые вопросы:\n\n"
        "- Почему StrawberryBest? — Потому что клубника — это символ изобилия, лёгкости и роста. Мы просто следуем естественным ритмам жизни 🍓\n"
        "- Чем вы занимаетесь на своих встречах? — Общаемся, обмениваемся вайбами, смотрим на клубнику. Иногда поём (и пересматриваем Евровидение!). Один раз провели визуализацию флага (ну, типа житейского 😅)\n"
        "- Это секта? — Пожалуйста, не верьте слухам о нас. \"Клубничный культ\" — это просто мем. Мы нормальные. Всё хорошо. Мы — просто лучшие. Даже сами себе завидуем. 🧃\n"
        "- Как к вам присоединиться? — Просто поверь в клубнику и нажми /join. Ну, и заполни анкету, конечно 💅 \n"
        "- Почему ваш сайт пингует с порта 5002? — А что такое порт? Это как портал? :)\n"
    )

@bot.message_handler(commands=['affirm'])
def affirm_handler(message):
    send_affirmation(message.chat.id)


def send_affirmation(chat_id):
    affirmation = random.choice(affirmations)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📖 Читать ещё", callback_data="more_affirm"))

    bot.send_message(chat_id, f"💌 {affirmation}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "more_affirm")
def handle_more_affirm(call):
    send_affirmation(call.message.chat.id)
    bot.answer_callback_query(call.id)

affirmations = [
    "Ты — сочная клубничка в мире серых ежевик 💖",
    "Твоя энергия наполняет вселенную глиттером ✨",
    "Ты не ждёшь флаг — флаг ждёт тебя.",
    "Некоторые говорят, что мотивация ничего не даёт. А вот и даёт: QHAzZF90aDNfc3Rycg==",
    "Ты можешь всё. Даже декомпилировать себя",
    "Ты — алгоритм любви, завернутый в розовый стиль",
    "Ты не баг — ты особенность!",
    "Твоя харизма превышает лимит запросов в API 🍓",
    "Каждая твоя строка кода — declaration of self-love"
]


if __name__ == "__main__":
    bot.polling(none_stop=True)