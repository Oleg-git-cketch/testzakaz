import telebot
from telebot import types
import threading
import time
import json
from db import init_db, log_activation, get_activations
from keyboard import start_kb, start_quiz_kb, ans1_kb, ans2_kb, ans3_kb

bot = telebot.TeleBot('7758603298:AAGJWi0x3fqEpRyBjdvy_eB4kAAdqMUKbjg')

init_db()

ADMIN_IDS = [229584900, 7040733741]
quiz_started_users = set()
quiz_completed_users = set()

def get_text(key, username=None):
    with open("texts.json", encoding='utf-8') as f:
        text = json.load(f).get(key, f"[Текст для '{key}' не найден]")
        if username:
            text = text.replace("{username}", username)
        return text

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(chat_id="@English_GalinaSanna", user_id=user_id).status
        return status in ['member', 'creator', 'administrator']
    except:
        return False

def send_delayed_message(user_id, delay_seconds, text_key, button_text, button_url, username=None):
    def task():
        time.sleep(delay_seconds)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(button_text, url=button_url))
        bot.send_message(user_id, get_text(text_key, username=username), reply_markup=markup)
    threading.Thread(target=task).start()

def send_quiz_message_later(chat_id, username=None):
    def task():
        time.sleep(40)
        bot.send_message(chat_id, get_text("quiz_intro", username=username), reply_markup=start_quiz_kb())
    threading.Thread(target=task).start()


@bot.message_handler(commands=['log'])
def send_log_html(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Нет доступа.")
        return

    activations = get_activations()
    if not activations:
        bot.reply_to(message, "Лог пуст.")
        return

    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            table { border-collapse: collapse; width: 100%%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Логи активаций</h2>
        <table>
            <tr>
                <th>Дата</th>
                <th>ID</th>
                <th>Пользователь</th>
                <th>UTM</th>
            </tr>
    """

    for dt, user_id, username, utm in activations[-50:]:
        html += f"""
        <tr>
            <td>{dt}</td>
            <td>{user_id}</td>
            <td>{username}</td>
            <td>{utm or '-'}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as tmpfile:
        tmpfile.write(html)
        tmpfile.flush()
        bot.send_document(message.chat.id, open(tmpfile.name, 'rb'), caption="Логи активаций (HTML)")



def start_sales_funnel(user_id, username=None):
    def task():
        send_delayed_message(user_id, 0, "bonus_text", "✅ Записаться со скидкой", "https://t.me/EGE_BOOST100", username)
        send_delayed_message(user_id, 20, "dop1_text", "✅ Подобрать подходящий вуз", "https://t.me/EGE_BOOST100", username)
        send_delayed_message(user_id, 40, "dop2_text", "✅ Найти своего учителя", "https://t.me/EGE_BOOST100", username)
        send_delayed_message(user_id, 60, "case_text", "✅ Повторить успех", "https://t.me/EGE_BOOST100", username)
        send_delayed_message(user_id, 80, "final", "✅ Зафиксировать условия", "https://t.me/EGE_BOOST100", username)
    threading.Thread(target=task).start()

def start_quiz_watchdog(user_id, username=None):
    def task():
        time.sleep(60)
        if user_id not in quiz_completed_users:
            start_sales_funnel(user_id, username)
    threading.Thread(target=task).start()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name or message.from_user.username or "Уважаемый пользователь"

    utm = ''
    if message.text and len(message.text.split()) > 1:
        utm = ' '.join(message.text.split()[1:])

    log_activation(user_id, username, utm)

    if is_subscribed(user_id):
        send_delayed_message(user_id, 0, "welcome", "✅Забрать подарок", "https://drive.google.com/file/d/1JhS6i9fxFe7ajXjAqXL-_rGkExEwNYym/view?usp=sharing", username)
        send_delayed_message(user_id, 20, "material", "✅ Записаться на урок", "https://t.me/EGE_BOOST100", username)
        send_quiz_message_later(user_id, username)
        start_quiz_watchdog(user_id, username)
    else:
        bot.send_message(user_id, get_text("ask_sub", username=username), reply_markup=start_kb())


@bot.message_handler(commands=['edit'])
def edit_text(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ У вас нет прав для изменения текстов.")
        return
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.reply_to(message, "⚠ Формат: /edit <ключ> <новый текст>")
            return

        _, key, raw_text = parts

        new_text = raw_text.replace("\\n", "\n")

        with open("texts.json", encoding='utf-8') as f:
            data = json.load(f)

        if key in data:
            data[key] = new_text
            with open("texts.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            bot.reply_to(message, f"✅ Текст для ключа '{key}' обновлён.\n\n📄 Новый текст:\n{new_text}")
        else:
            bot.reply_to(message, f"❗ Ключ '{key}' не найден в файле.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при редактировании: {e}")


@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    username = call.from_user.first_name or call.from_user.username or "Уважаемый пользователь"
    if is_subscribed(user_id):
        send_delayed_message(user_id, 10, "welcome", "✅ Записаться на урок", "https://wa.me/79281138117", username)
        send_quiz_message_later(user_id, username)
        start_quiz_watchdog(user_id, username)
    else:
        bot.send_message(user_id, get_text("sub_fail", username=username))

@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def start_quiz(call):
    quiz_started_users.add(call.from_user.id)
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_text("quiz1"),
            reply_markup=ans1_kb()
        )
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e):
            raise

@bot.callback_query_handler(func=lambda call: call.data == "true1")
def ans2(call):
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_text("quiz2"),
            reply_markup=ans2_kb()
        )
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e):
            raise

@bot.callback_query_handler(func=lambda call: call.data == "true2")
def ans3(call):
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_text("quiz3"),
            reply_markup=ans3_kb()
        )
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e):
            raise

@bot.callback_query_handler(func=lambda call: call.data == "true3")
def complete_quiz(call):
    user_id = call.from_user.id
    quiz_started_users.add(call.from_user.id)
    quiz_completed_users.add(call.from_user.id)
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_text("quiz_complete")
        )
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e):
            raise
    username = call.from_user.first_name or call.from_user.username or "Уважаемый пользователь"
    start_sales_funnel(call.from_user.id, username)


@bot.callback_query_handler(func=lambda call: call.data.startswith("false"))
def handle_wrong_answer(call):
    chat_id = call.message.chat.id
    try:
        if call.data == 'false1':
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=get_text("wrong1"), reply_markup=ans1_kb())
        elif call.data == 'false12':
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=get_text("wrong12"), reply_markup=ans1_kb())
        elif call.data == 'false2':
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=get_text("wrong2"), reply_markup=ans2_kb())
        elif call.data == 'false22':
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=get_text("wrong22"), reply_markup=ans2_kb())
        elif call.data == 'false3':
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=get_text("wrong3"), reply_markup=ans3_kb())
        elif call.data == 'false32':
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=get_text("wrong32"), reply_markup=ans3_kb())
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e):
            raise

while True:
    try:
        bot.polling(non_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"⚠ Ошибка polling: {e}")
        time.sleep(5)

