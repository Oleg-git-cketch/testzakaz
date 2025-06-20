import telebot
from telebot import types
import threading
import time
from keyboard import start_kb, start_quiz_kb, ans1_kb, ans2_kb, ans3_kb

bot = telebot.TeleBot('7750734085:AAE4ezbZYWqDczqUujLntkV7H7HBI6nGjII')

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(chat_id="@test13242325", user_id=user_id).status
        return status in ['member', 'creator', 'administrator']
    except:
        return False

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    if is_subscribed(user_id):
        bot.send_message(user_id, "🎉 Отлично! Вы подписаны. Вот ваш материал.")
    else:
        bot.send_message(user_id, "❗ Вы еще не подписались. Подпишитесь и нажмите кнопку снова.")

def send_quiz_message_later(chat_id):
    def task():
        time.sleep(10)  # 10 минут
        text = "🎯 Ответьте на вопросы и получите скидку 500₽ за каждый правильный ответ:"
        bot.send_message(chat_id, text, reply_markup=start_quiz_kb())
    threading.Thread(target=task).start()

def send_delayed_message(user_id, delay_seconds, text, button_text, button_url):
    def task():
        time.sleep(delay_seconds)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(button_text, url=button_url))
        bot.send_message(user_id, text, reply_markup=markup)
    threading.Thread(target=task).start()

def message_later(user_id, delay_seconds, text, button_text, button_url):
    def task():
        time.sleep(delay_seconds)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(button_text, url=button_url))
        bot.send_message(user_id, text, reply_markup=markup)
    threading.Thread(target=task).start()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    # Проверяем подписку
    if is_subscribed(user_id):
        bot.send_message(user_id, "Спасибо за подписку! Вот ваш подарок 🎁")
        # Можно отправить файл, ссылку и т.д.
        send_delayed_message(
            user_id,
            delay_seconds=10,  # 10 минут
            text="🎓 Вот дополнительный материал, который поможет вам поступить в вуз:",
            button_text="✅ Записаться на урок",
            button_url="https://wa.me/79281138117"
        )
        send_quiz_message_later(
            user_id

        )
    else:
        bot.send_message(user_id,
                         "Пожалуйста, подпишитесь на канал, чтобы продолжить:\n👉 https://t.me/test13242325",
                         reply_markup=start_kb())


# вопросы
@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def start_quiz(call):
    # bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Вопрос 1:\n\nКакие вузы стоит рассматривать для поступления на бюджет, кроме самых известных?',
        reply_markup=ans1_kb()
    )

@bot.callback_query_handler(func=lambda call: call.data == "true1")
def ans2(call):
    # bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Вопрос 2:\n\nЧто важно знать о проходных баллах для поступления?',
        reply_markup=ans2_kb()
    )

@bot.callback_query_handler(func=lambda call: call.data == "true2")
def ans3(call):
    # bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Вопрос 3:\n\nЧто важно при выборе вуза для сдачи ЕГЭ по английскому на бюджет?',
        reply_markup=ans3_kb()
    )

@bot.callback_query_handler(func=lambda call: call.data == "true3")
def complete_quiz(call):
    # bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='🎉 Вы успешно прошли квиз!\n\nВаша общая сумма скидки — 1500₽ 🎁'
    )
    send_delayed_message(
        call.from_user.id,
        delay_seconds=10,  # 10 минут
        text="После прохождения квиза мы выражаем вам искреннюю благодарность за уделенное время и подтверждаем ценность вашего участия. В качестве бонуса вы получаете 1500 бонусных рублей на наши программы – это ваша заслуженная скидка!",
        button_text="Записаться со скидкой",
        button_url="https://wa.me/79281138117"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("false"))
def handle_wrong_answer(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id


    if call.data == 'false1':
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='❌ Неверно! Попробуйте ещё раз:\n\nВопрос 1:\nКакие вузы стоит рассматривать для поступления на бюджет, кроме самых известных?',
            reply_markup=ans1_kb()
        )
    elif call.data == 'false2':
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='❌ Неверно! Попробуйте ещё раз:\n\nВопрос 2:\nЧто важно знать о проходных баллах для поступления?',
            reply_markup=ans2_kb()
        )
    elif call.data == 'false3':
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='❌ Неверно! Попробуйте ещё раз:\n\nВопрос 3:\nЧто важно при выборе вуза для сдачи ЕГЭ по английскому на бюджет?',
            reply_markup=ans3_kb()
        )


bot.polling()