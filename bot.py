# import os
# import json
# from dotenv import load_dotenv
# import telebot
# from telebot import types

# load_dotenv()
# TOKEN = os.getenv('BOT_TOKEN')
# if not TOKEN:
#     print("❌ Добавь BOT_TOKEN в .env файл!")
#     exit()

# bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# # ====================== ХРАНИЛИЩЕ ПОЛЬЗОВАТЕЛЕЙ ======================
# USERS_FILE = "users.json"
# try:
#     with open(USERS_FILE, "r", encoding="utf-8") as f:
#         users = set(json.load(f))
# except:
#     users = set()

# def save_users():
#     with open(USERS_FILE, "w", encoding="utf-8") as f:
#         json.dump(list(users), f)

# # ====================== КЛАВИАТУРЫ ======================
# def main_keyboard():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     btn1 = types.KeyboardButton('👋 О нас')
#     btn2 = types.KeyboardButton('💅 Услуги')
#     btn3 = types.KeyboardButton('☕🍹 Угощения')
#     btn4 = types.KeyboardButton('📅 Записаться')
#     btn5 = types.KeyboardButton('📞 Контакты')
#     btn6 = types.KeyboardButton('❓ Помощь')
#     markup.add(btn1, btn2)
#     markup.add(btn3, btn4)
#     markup.add(btn5, btn6)
#     return markup

# def services_categories():
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     markup.add(
#         types.InlineKeyboardButton('💅 Маникюр и педикюр', callback_data='cat_nails'),
#         types.InlineKeyboardButton('🌟 Брови и ресницы', callback_data='cat_brows'),
#         types.InlineKeyboardButton('💇‍♀️ Волосы', callback_data='cat_hair'),
#         types.InlineKeyboardButton('💄 Макияж', callback_data='cat_makeup')
#     )
#     markup.row(types.InlineKeyboardButton('« Назад в меню', callback_data='back_to_main'))
#     return markup

# def back_to_services_markup():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     markup.add(
#         types.InlineKeyboardButton('📅 Записаться', url='https://n757778.yclients.com/company/712716/personal/menu?o='),
#         types.InlineKeyboardButton('« Назад к категориям', callback_data='back_to_categories')
#     )
#     return markup

# def drinks_menu_markup():
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     markup.add(
#         types.InlineKeyboardButton('🍵 Чай', callback_data='drink_tea'),
#         types.InlineKeyboardButton('☕ Кофе', callback_data='drink_coffee'),
#         types.InlineKeyboardButton('🥛 Молоко на выбор', callback_data='drink_milk'),
#         types.InlineKeyboardButton('🍯 Сиропы', callback_data='drink_syrup'),
#         types.InlineKeyboardButton('🍋 Дополнения', callback_data='drink_add'),
#         types.InlineKeyboardButton('🥤 Вода', callback_data='drink_water'),
#         types.InlineKeyboardButton('🥂 Для настроения', callback_data='drink_mood')
#     )
#     markup.add(types.InlineKeyboardButton('« Назад в меню', callback_data='back_to_main'))
#     return markup

# # ====================== ОБРАБОТЧИКИ ======================
# @bot.message_handler(commands=['start'])
# def start(message):
#     users.add(message.chat.id)
#     save_users()
#     welcome = (
#         "👋 <b>Добро пожаловать в студию красоты Бьютилаб!</b>\n\n"
#         "📍 Москва, ул. Щепкина 28, м. Проспект Мира\n"
#         "📞 <a href='tel:+79774498581'>+7 (977) 449-85-81</a>\n"
#         "🕒 Ежедневно 10:00–22:00\n\n"
#         "💅 Запишитесь на услугу за 30 секунд — без очередей и лотереи с мастером ✨"
#     )
#     bot.send_message(message.chat.id, welcome, reply_markup=main_keyboard())

# @bot.message_handler(commands=['update'])
# def broadcast_update(message):
#     if message.from_user.id != 6177817315:
#         return
#     sent = 0
#     for uid in list(users):
#         try:
#             bot.send_message(uid, "🔄 Бот обновлён!\n\nМы добавили новые удобства и улучшения ❤️\nЧтобы увидеть все свежие изменения — пожалуйста, просто отправьте боту команду\n\n/start\n\nЭто займёт 2 секунды, и дальше всё будет обновляться автоматически ✨\nСпасибо, что вы с нами!")
#             sent += 1
#         except:
#             pass
#     bot.send_message(message.chat.id, f"✅ Сообщение отправлено {sent} пользователям!")

# @bot.message_handler(func=lambda m: m.text and m.text.lower() in ['привет', 'здравствуй', 'добрый день', 'доброе утро', 'добрый вечер', 'хай', 'hello', 'hi', 'здрасьте'])
# def hello(message):
#     users.add(message.chat.id)
#     save_users()
#     start(message)

# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     users.add(message.chat.id)
#     save_users()
#     text = message.text
#     if text == '👋 О нас':
#         about = "✨ <b>Бьютилаб</b> — студия красоты у метро Проспект Мира.\n\n📍 Адрес: Москва, ул. Щепкина, 28\n\nМы создаём пространство, где каждая девушка чувствует заботу, комфорт и результат.\nСтерильность, современные материалы, опытные мастера и никакого стресса."
#         bot.send_message(message.chat.id, about, reply_markup=main_keyboard())
#         bot.send_location(message.chat.id, 55.77393, 37.63198)
#     elif text == '💅 Услуги':
#         bot.send_message(message.chat.id, "🛍️ <b>Выберите категорию услуг:</b>", reply_markup=services_categories())
#     elif text == '☕🍹 Угощение':
#         bot.send_message(message.chat.id, "🎁 <b>Угощение для наших любимых гостей</b>\n\nВыберите, что хотите попробовать 👇", reply_markup=drinks_menu_markup())
#     elif text == '📅 Записаться':
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('🚀 Записаться онлайн', url='https://n757778.yclients.com/company/712716/personal/menu?o='))
#         bot.send_message(message.chat.id, "💫 Переходи в онлайн-запись — выбери мастера, услугу и удобное время за 30 секунд!", reply_markup=markup)
#     elif text == '📞 Контакты':
#         contacts = "📍 <b>Бьютилаб</b>\nул. Щепкина 28, Москва\nм. Проспект Мира\n\n📞 <a href='tel:+79774498581'>+7 (977) 449-85-81</a>\n🕒 Ежедневно 10:00–22:00\n\nНапиши нам в любой момент — ответим максимально быстро ❤️"
#         bot.send_message(message.chat.id, contacts, reply_markup=main_keyboard())
#     elif text == '❓ Помощь':
#         help_text = "❓ <b>Нужна помощь?</b>\n\nЕсли бот глючит, не открывается запись, не приходят сообщения или есть любые вопросы/пожелания — пиши напрямую администратору:\n\n👉 @ScreamLulzz\n\nМы ответим максимально быстро ❤️\nТакже можешь позвонить: +7 (933) 205-88-10"
#         bot.send_message(message.chat.id, help_text, reply_markup=main_keyboard())

# # ====================== CALLBACK ======================
# @bot.callback_query_handler(func=lambda call: True)
# def callback_handler(call):
#     if call.data == 'back_to_main':
#         try: bot.delete_message(call.message.chat.id, call.message.message_id)
#         except: pass
#         bot.send_message(call.message.chat.id, "Главное меню:", reply_markup=main_keyboard())

#     elif call.data == 'back_to_categories':
#         bot.edit_message_text("🛍️ <b>Выберите категорию услуг:</b>", call.message.chat.id, call.message.message_id, reply_markup=services_categories())

#     elif call.data.startswith('cat_'):
#         if call.data == 'cat_nails':
#             text = "<b>💅 Маникюр и педикюр</b>\n\n• Комплексный маникюр — 3100 ₽\n• Маникюр без покрытия — 1700 ₽\n• Наращивание ногтей — от 3990 ₽\n• Педикюр с покрытием Luxio — от 2550 ₽\n• Smart педикюр — 2300 ₽\n• Мужской/детский маникюр — от 800 ₽\n\nВсе цены актуальны на март 2026."
#         elif call.data == 'cat_brows':
#             text = "<b>🌟 Брови и ресницы</b>\n\n• Архитектура бровей — 1990 ₽\n• Окрашивание бровей — 1300 ₽\n• Ламинирование бровей — 3000 ₽\n• Наращивание ресниц 1D — 2490 ₽\n• Наращивание ресниц 2D–4D — от 3790 ₽"
#         elif call.data == 'cat_hair':
#             text = "<b>💇‍♀️ Волосы</b>\n\n• Стрижка + укладка — 2490 ₽\n• Комплексный уход — 3490 ₽\n• Прикорневое окрашивание — от 4490 ₽\n• Сложное окрашивание Airtouch — 29900 ₽"
#         elif call.data == 'cat_makeup':
#             text = "<b>💄 Макияж</b>\n\n• Дневной макияж — 3500 ₽\n• Вечерний макияж — 5000 ₽"
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_to_services_markup())

#     # ==================== УГОЩЕНИЕ ====================
#     elif call.data == 'drink_tea':
#         text = "🍵 <b>Чай</b>\n\n• Зелёный: классический / с мелиссой\n• Чёрный: с бергамотом / классический\n• Травяной: гибискус с малиной\n\nЧтобы заказать чай нажмите кнопку ниже 👇"
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
#         markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

#     elif call.data == 'drink_coffee':
#         text = "☕ <b>Кофе</b>\n\n• Эспрессо / Американо / Капучино / Латте\n\nЧтобы заказать кофе нажмите кнопку ниже 👇"
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
#         markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

#     elif call.data == 'drink_milk':
#         text = "🥛 <b>Молоко на выбор</b>\n\n• миндальное • кокосовое • классическое\n\nЧтобы заказать молоко нажмите кнопку ниже 👇"
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
#         markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

#     elif call.data == 'drink_syrup':
#         text = "🍯 <b>Сиропы</b>\n\n• ванильный • карамельный • миндальный • кокосовый\n\nЧтобы заказать сироп нажмите кнопку ниже 👇"
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
#         markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

#     elif call.data == 'drink_add':
#         text = "🍋 <b>Дополнения</b>\n\n• корица • лимон\n\nЧтобы заказать дополнения нажмите кнопку ниже 👇"
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
#         markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

#     elif call.data == 'drink_water':
#         text = "🥤 <b>Вода</b>\n\n• Без газа / с лимоном\n\nЧтобы заказать воду нажмите кнопку ниже 👇"
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
#         markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

#     elif call.data == 'drink_mood':
#         text = "🥂 <b>Для настроения</b>\n\n• Игристое сухое / вино белое\n\nЧтобы заказать напиток для настроения нажмите кнопку ниже 👇"
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
#         markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
#         bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

#     elif call.data == 'back_to_drinks':
#         bot.edit_message_text("🎁 <b>Угощение для наших любимых гостей</b>\n\nВыберите, что хотите попробовать 👇", call.message.chat.id, call.message.message_id, reply_markup=drinks_menu_markup())

# # ====================== ЗАПУСК ======================
# if __name__ == '__main__':
#     print("🚀 Бот Бьютилаб запущен...")
#     bot.infinity_polling()
import os
import json
from dotenv import load_dotenv
import telebot
from telebot import types
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    print("❌ Добавь BOT_TOKEN в .env файл!")
    exit()
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ====================== ХРАНИЛИЩЕ ПОЛЬЗОВАТЕЛЕЙ ======================
USERS_FILE = "users.json"
try:
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = set(json.load(f))
except:
    users = set()

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(users), f)

# ====================== КЛАВИАТУРЫ ======================
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('👋 О нас')
    btn2 = types.KeyboardButton('💅 Услуги')
    btn3 = types.KeyboardButton('☕🍹 Угощение')
    btn4 = types.KeyboardButton('📅 Записаться')
    btn5 = types.KeyboardButton('📞 Контакты')
    btn6 = types.KeyboardButton('❓ Помощь')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    return markup

def services_categories():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('💅 Маникюр и педикюр', callback_data='cat_nails'),
        types.InlineKeyboardButton('🌟 Брови и ресницы', callback_data='cat_brows'),
        types.InlineKeyboardButton('💇‍♀️ Волосы', callback_data='cat_hair'),
        types.InlineKeyboardButton('💄 Макияж', callback_data='cat_makeup')
    )
    markup.row(types.InlineKeyboardButton('« Назад в меню', callback_data='back_to_main'))
    return markup

def back_to_services_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('📅 Записаться', url='https://n757778.yclients.com/company/712716/personal/menu?o='),
        types.InlineKeyboardButton('« Назад к категориям', callback_data='back_to_categories')
    )
    return markup

def drinks_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('🍵 Чай', callback_data='drink_tea'),
        types.InlineKeyboardButton('☕ Кофе', callback_data='drink_coffee'),
        types.InlineKeyboardButton('🥛 Молоко на выбор', callback_data='drink_milk'),
        types.InlineKeyboardButton('🍯 Сиропы', callback_data='drink_syrup'),
        types.InlineKeyboardButton('🍋 Дополнения', callback_data='drink_add'),
        types.InlineKeyboardButton('🥤 Вода', callback_data='drink_water'),
        types.InlineKeyboardButton('🥂 Для настроения', callback_data='drink_mood')
    )
    markup.add(types.InlineKeyboardButton('« Назад в меню', callback_data='back_to_main'))
    return markup

# ====================== ОБРАБОТЧИКИ ======================
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)
    save_users()
    welcome = (
        "👋 <b>Добро пожаловать в студию красоты Бьютилаб!</b>\n\n"
        "📍 Москва, ул. Щепкина 28, м. Проспект Мира\n"
        "📞 <a href='tel:+79774498581'>+7 (977) 449-85-81</a>\n"
        "🕒 Ежедневно 10:00–22:00\n\n"
        "💅 Запишитесь на услугу за 30 секунд — без очередей и лотереи с мастером ✨"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=main_keyboard())

@bot.message_handler(commands=['update'])
def broadcast_update(message):
    if message.from_user.id !=  YOUR_ID:   # ←←← ЗАМЕНИ НА СВОЙ TELEGRAM ID !!!
        return
    sent = 0
    for uid in list(users):
        try:
            bot.send_message(uid, "🔄 <b>Бот обновлён!</b>\n\nПожалуйста нажмите <b>/start</b> чтобы увидеть новое меню ❤️\n\nСпасибо, что вы с нами ✨")
            sent += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ Сообщение отправлено {sent} пользователям!")

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ['привет', 'здравствуй', 'добрый день', 'доброе утро', 'добрый вечер', 'хай', 'hello', 'hi', 'здрасьте'])
def hello(message):
    users.add(message.chat.id)
    save_users()
    start(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    users.add(message.chat.id)
    save_users()
    text = message.text
    if text == '👋 О нас':
        about = "✨ <b>Бьютилаб</b> — студия красоты у метро Проспект Мира.\n\n📍 Адрес: Москва, ул. Щепкина, 28\n\nМы создаём пространство, где каждая девушка чувствует заботу, комфорт и результат.\nСтерильность, современные материалы, опытные мастера и никакого стресса."
        bot.send_message(message.chat.id, about, reply_markup=main_keyboard())
        bot.send_location(message.chat.id, 55.77393, 37.63198)
    elif text == '💅 Услуги':
        bot.send_message(message.chat.id, "🛍️ <b>Выберите категорию услуг:</b>", reply_markup=services_categories())
    elif text == '☕🍹 Угощение':
        bot.send_message(message.chat.id, "🎁 <b>Угощение для наших любимых гостей</b>\n\nВыберите, что хотите попробовать 👇", reply_markup=drinks_menu_markup())
    elif text == '📅 Записаться':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('🚀 Записаться онлайн', url='https://n757778.yclients.com/company/712716/personal/menu?o='))
        bot.send_message(message.chat.id, "💫 Переходи в онлайн-запись — выбери мастера, услугу и удобное время за 30 секунд!", reply_markup=markup)
    elif text == '📞 Контакты':
        contacts = "📍 <b>Бьютилаб</b>\nул. Щепкина 28, Москва\nм. Проспект Мира\n\n📞 <a href='tel:+79774498581'>+7 (977) 449-85-81</a>\n🕒 Ежедневно 10:00–22:00\n\nНапиши нам в любой момент — ответим максимально быстро ❤️"
        bot.send_message(message.chat.id, contacts, reply_markup=main_keyboard())
    elif text == '❓ Помощь':
        help_text = "❓ <b>Нужна помощь?</b>\n\nЕсли бот глючит, не открывается запись, не приходят сообщения или есть любые вопросы/пожелания — пиши напрямую администратору:\n\n👉 @ScreamLulzz\n\nМы ответим максимально быстро ❤️\nТакже можешь позвонить: +7 (933) 205-88-10"
        bot.send_message(message.chat.id, help_text, reply_markup=main_keyboard())

# ====================== CALLBACK ======================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'back_to_main':
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        bot.send_message(call.message.chat.id, "Главное меню:", reply_markup=main_keyboard())

    elif call.data == 'back_to_categories':
        bot.edit_message_text("🛍️ <b>Выберите категорию услуг:</b>", call.message.chat.id, call.message.message_id, reply_markup=services_categories())

    elif call.data.startswith('cat_'):
        if call.data == 'cat_nails':
            text = "<b>💅 Маникюр и педикюр</b>\n\n• Комплексный маникюр — 3100 ₽\n• Маникюр без покрытия — 1700 ₽\n• Наращивание ногтей — от 3990 ₽\n• Педикюр с покрытием Luxio — от 2550 ₽\n• Smart педикюр — 2300 ₽\n• Мужской/детский маникюр — от 800 ₽\n\nВсе цены актуальны на март 2026."
        elif call.data == 'cat_brows':
            text = "<b>🌟 Брови и ресницы</b>\n\n• Архитектура бровей — 1990 ₽\n• Окрашивание бровей — 1300 ₽\n• Ламинирование бровей — 3000 ₽\n• Наращивание ресниц 1D — 2490 ₽\n• Наращивание ресниц 2D–4D — от 3790 ₽"
        elif call.data == 'cat_hair':
            text = "<b>💇‍♀️ Волосы</b>\n\n• Стрижка + укладка — 2490 ₽\n• Комплексный уход — 3490 ₽\n• Прикорневое окрашивание — от 4490 ₽\n• Сложное окрашивание Airtouch — 29900 ₽"
        elif call.data == 'cat_makeup':
            text = "<b>💄 Макияж</b>\n\n• Дневной макияж — 3500 ₽\n• Вечерний макияж — 5000 ₽"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_to_services_markup())

    # ==================== УГОЩЕНИЕ ====================
    elif call.data == 'drink_tea':
        text = "🍵 <b>Чай</b>\n\nЧтобы заказать чай нажмите кнопку ниже 👇\n• Зелёный: классический / с мелиссой\n• Чёрный: с бергамотом / классический\n• Травяной: гибискус с малиной"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
        markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'drink_coffee':
        text = "☕ <b>Кофе</b>\n\nЧтобы заказать кофе нажмите кнопку ниже 👇\n• Эспрессо / Американо / Капучино / Латте"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
        markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'drink_milk':
        text = "🥛 <b>Молоко на выбор</b>\n\nЧтобы заказать молоко нажмите кнопку ниже 👇\n• миндальное • кокосовое • классическое"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
        markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'drink_syrup':
        text = "🍯 <b>Сиропы</b>\n\nЧтобы заказать сироп нажмите кнопку ниже 👇\n• ванильный • карамельный • миндальный • кокосовый"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
        markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'drink_add':
        text = "🍋 <b>Дополнения</b>\n\nЧтобы заказать дополнения нажмите кнопку ниже 👇\n• корица • лимон"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
        markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'drink_water':
        text = "🥤 <b>Вода</b>\n\nЧтобы заказать воду нажмите кнопку ниже 👇\n• Без газа / с лимоном"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
        markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'drink_mood':
        text = "🥂 <b>Для настроения</b>\n\nЧтобы заказать напиток для настроения нажмите кнопку ниже 👇\n• Игристое сухое / вино белое"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url='https://t.me/Wish_Lab'))
        markup.add(types.InlineKeyboardButton('« Назад к угощению', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'back_to_drinks':
        bot.edit_message_text("🎁 <b>Угощение для наших любимых гостей</b>\n\nВыберите, что хотите попробовать 👇", call.message.chat.id, call.message.message_id, reply_markup=drinks_menu_markup())

# ====================== ЗАПУСК ======================
if __name__ == '__main__':
    print("🚀 Бот Бьютилаб запущен...")
    bot.infinity_polling()
