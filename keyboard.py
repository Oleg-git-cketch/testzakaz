import telebot



def start_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")

    kb.add(but1)

    return kb

def lesson_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton("Записаться на урок", callback_data="check_sub")

    kb.add(but1)

    return kb

def start_quiz_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('Начать квиз', callback_data='start_quiz')

    kb.add(but1)

    return kb

def ans1_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('Топовые университеты в столице', callback_data='false1')
    but2 = telebot.types.InlineKeyboardButton('Сильные региональные вузы', callback_data='true1')
    but3 = telebot.types.InlineKeyboardButton('Вузы с высоким проходным', callback_data='false12')

    kb.add(but1)
    kb.add(but2)
    kb.add(but3)

    return kb


def ans2_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('Остаются неизменными каждый год', callback_data='false2')
    but2 = telebot.types.InlineKeyboardButton('Могут меняться, нужна статистика за 2+ года',callback_data='true2')
    but3 = telebot.types.InlineKeyboardButton('С высокими результатами неважно', callback_data='false22')

    kb.add(but1)
    kb.add(but2)
    kb.add(but3)

    return kb


def ans3_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('Обязательно наличие общих предметов', callback_data='false3')
    but2 = telebot.types.InlineKeyboardButton('Только высокие проходные баллы',callback_data='false32')
    but3 = telebot.types.InlineKeyboardButton('Возможность перевода с платного на бюджет',callback_data='true3')

    kb.add(but1)
    kb.add(but2)
    kb.add(but3)

    return kb

def dop1_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('✅Подобрать подходящий вуз', callback_data='dop1')

    kb.add(but1)


def dop2_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('✅Найти своего учителя', callback_data='dop2')

    kb.add(but1)

def case_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('✅Повторить успех', callback_data='case')

    kb.add(but1)

def final_kb():
    kb = telebot.types.InlineKeyboardMarkup()

    but1 = telebot.types.InlineKeyboardButton('✅Успеть занять место', callback_data='final')

    kb.add(but1)