import telebot
from telebot import types
import threading
import time
import json
from keyboard import start_kb, start_quiz_kb, ans1_kb, ans2_kb, ans3_kb

bot = telebot.TeleBot('7750734085:AAE4ezbZYWqDczqUujLntkV7H7HBI6nGjII')

ADMIN_ID = 7040733741  # Замените на свой Telegram ID


def get_text(key):
    with open("texts.json", encoding='utf-8') as f:
        return json.load(f).get(key, f"[Текст для '{key}' не найден]")


def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(chat_id="@test13242325", user_id=user_id).status
        return status in ['member', 'creator', 'administrator']
    except:
        return False


@bot.message_handler(commands=['edit'])
def edit_text(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ У вас нет прав для изменения текстов.")
        return

    try:
        _, key, *value = message.text.split()
        new_text = ' '.join(value)

        with open("texts.json", encoding='utf-8') as f:
            data = json.load(f)

        if key in data:
            data[key] = new_text
            with open("texts.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            bot.reply_to(message, f"✅ Текст для '{key}' обновлён.")
        else:
            bot.reply_to(message, f"❗ Ключ '{key}' не найден в файле.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")


@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_message(user_id, get_text("sub_success"))
    else:
        bot.send_message(user_id, get_text("sub_fail"))


def send_quiz_message_later(chat_id):
    def task():
        time.sleep(10)
        bot.send_message(chat_id, get_text("quiz_intro"), reply_markup=start_quiz_kb())
    threading.Thread(target=task).start()


def send_delayed_message(user_id, delay_seconds, text_key, button_text, button_url):
    def task():
        time.sleep(delay_seconds)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(button_text, url=button_url))
        bot.send_message(user_id, get_text(text_key), reply_markup=markup)
    threading.Thread(target=task).start()


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if is_subscribed(user_id):
        bot.send_message(user_id, get_text("welcome"))
        send_delayed_message(user_id, 10, "material", "✅ Записаться на урок", "https://wa.me/79281138117")
        send_quiz_message_later(user_id)
    else:
        bot.send_message(user_id, get_text("ask_sub"), reply_markup=start_kb())


@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def start_quiz(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=get_text("quiz1"),
        reply_markup=ans1_kb()
    )


@bot.callback_query_handler(func=lambda call: call.data == "true1")
def ans2(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=get_text("quiz2"),
        reply_markup=ans2_kb()
    )


@bot.callback_query_handler(func=lambda call: call.data == "true2")
def ans3(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=get_text("quiz3"),
        reply_markup=ans3_kb()
    )


@bot.callback_query_handler(func=lambda call: call.data == "true3")
def complete_quiz(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=get_text("quiz_complete")
    )
    send_delayed_message(
        call.from_user.id,
        delay_seconds=10,
        text_key="bonus_text",
        button_text="Записаться со скидкой",
        button_url="https://wa.me/79281138117"
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("false"))
def handle_wrong_answer(call):
    chat_id = call.message.chat.id
    if call.data == 'false1':
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text("wrong1"), reply_markup=ans1_kb())
    elif call.data == 'false2':
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text("wrong2"), reply_markup=ans2_kb())
    elif call.data == 'false3':
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text("wrong3"), reply_markup=ans3_kb())


bot.polling()