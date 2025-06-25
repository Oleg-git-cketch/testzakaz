import telebot
from telebot import types

TOKEN = '8076429427:AAGTg5v3q2iGvITebSaX8SgdrMVvPaJDOOo'
CHANNEL_ID = '@sksjdjddh'  # Например, @mychannel

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['post'])
def send_post(message):
    # Текст сообщения
    text = "Это сообщение с кнопкой. Нажми на кнопку, чтобы перейти к боту!"

    # Создаём клавиатуру с одной кнопкой
    markup = types.InlineKeyboardMarkup()
    bot_link = f"https://t.me/AIchatPythonBot?start=start"
    btn = types.InlineKeyboardButton("Перейти к боту", url=bot_link)
    markup.add(btn)

    # Отправляем сообщение в канал
    bot.send_message(CHANNEL_ID, text, reply_markup=markup)

    # Подтверждаем пользователю
    bot.reply_to(message, "Сообщение отправлено в канал.")

bot.polling()
