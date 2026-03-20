# import os
# from dotenv import load_dotenv
# import telebot
# from telebot import types

# load_dotenv()
# TOKEN = os.getenv('BOT_TOKEN')
# if not TOKEN:
#     print("❌ Добавь BOT_TOKEN в .env файл!")
#     exit()

# bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# # ====================== КЛАВИАТУРЫ ======================
# def main_keyboard():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     btn1 = types.KeyboardButton('👋 О нас')
#     btn2 = types.KeyboardButton('💅 Услуги')
#     btn3 = types.KeyboardButton('👩‍🎨 Наши мастера')
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
#     markup.row(
#         types.InlineKeyboardButton('« Назад в меню', callback_data='back_to_main')
#     )
#     return markup

# def back_to_services_markup():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     markup.add(
#         types.InlineKeyboardButton('📅 Записаться', url='https://n757778.yclients.com/company/712716/personal/menu?o='),
#         types.InlineKeyboardButton('« Назад к категориям', callback_data='back_to_categories')
#     )
#     return markup

# # ====================== СПИСОК МАСТЕРОВ ======================
# MASTERS = [
#     {
#         "name": "Айсулуу",
#         "spec": "Топ мастер маникюра и педикюра",
#         "rating": "★★★★★ 1135 отзыв",
#         "info": "Один из самых опытных и популярных мастеров студии. Высокий рейтинг и тысячи довольных гостей."
#     },
#     {
#         "name": "Чынара",
#         "spec": "Топ мастер маникюра и педикюра",
#         "rating": "★★★★★ 1148 отзывов",
#         "info": "Профессионал с огромным количеством положительных отзывов. Работает быстро и качественно."
#     },
#     {
#         "name": "Айжан",
#         "spec": "Топ мастер маникюра и педикюра",
#         "rating": "★★★★★ 502 отзыва",
#         "info": "Любимый мастер многих гостей за аккуратность и внимание к деталям."
#     },
#     {
#         "name": "Айгуль",
#         "spec": "Топ мастер маникюра и педикюра",
#         "rating": "★★★★★ 1716 отзывов",
#         "info": "Рекордсмен по отзывам — очень опытный специалист с безупречной репутацией."
#     },
#     {
#         "name": "Диля",
#         "spec": "Мастер маникюра и педикюра. Парикмахер",
#         "rating": "★★★★★ 55 отзывов",
#         "info": "Универсальный мастер — делает и маникюр/педикюр, и стрижки. Аккуратная и внимательная."
#     },
#     {
#         "name": "Эля",
#         "spec": "Мастер маникюра и педикюра",
#         "rating": "★★★★★ 29 отзывов",
#         "info": "Молодой, но уже любимый многими мастер. Делает красиво и с душой."
#     },
#     {
#         "name": "Нестан",
#         "spec": "Мастер маникюра и педикюра",
#         "rating": "★★★★★ 5 отзыва",
#         "info": "Начинающий специалист с хорошим потенциалом. Аккуратная работа."
#     },
#     {
#         "name": "Мэри",
#         "spec": "Мастер маникюра и педикюра",
#         "rating": "★★★★★ 2 отзыва",
#         "info": "Внимательный подход к каждому клиенту. Хорошее качество по доступной цене."
#     },
#     {
#         "name": "Бермет",
#         "spec": "Мастер маникюра и педикюра",
#         "rating": "",
#         "info": "Специалист по ногтевому сервису. Доброжелательная и аккуратная."
#     },
# ]

# def masters_list_markup():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     for master in MASTERS:
#         markup.add(types.InlineKeyboardButton(master["name"], callback_data=f'master_{master["name"]}'))
#     markup.row(
#         types.InlineKeyboardButton('« Назад в меню', callback_data='back_to_main')
#     )
#     return markup

# # ====================== ОБРАБОТЧИКИ ======================
# @bot.message_handler(commands=['start'])
# def start(message):
#     welcome = (
#         "👋 <b>Добро пожаловать в студию красоты Бьютилаб!</b>\n\n"
#         "📍 Москва, ул. Щепкина 28, м. Проспект Мира\n"
#         "📞 <a href='tel:+79774498581'>+7 (977) 449-85-81</a>\n"
#         "🕒 Ежедневно 10:00–22:00\n\n"
#         "💅 Запишитесь на услугу за 30 секунд — без очередей и лотереи с мастером ✨"
#     )
#     bot.send_message(message.chat.id, welcome, reply_markup=main_keyboard())

# @bot.message_handler(func=lambda m: m.text and m.text.lower() in [
#     'привет', 'здравствуй', 'добрый день', 'доброе утро', 'добрый вечер',
#     'хай', 'hello', 'hi', 'здрасьте'
# ])
# def hello(message):
#     start(message)

# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     text = message.text
#     if text == '👋 О нас':
#         about = (
#             "✨ <b>Бьютилаб</b> — студия красоты у метро Проспект Мира.\n\n"
#             "📍 Адрес: Москва, ул. Щепкина, 28\n\n"
#             "Мы создаём пространство, где каждая девушка чувствует заботу, комфорт и результат.\n"
#             "Стерильность, современные материалы, опытные мастера и никакого стресса."
#         )
#         bot.send_message(message.chat.id, about, reply_markup=main_keyboard())
#         # Отправка геолокации
#         bot.send_location(message.chat.id, 55.77393, 37.63198)
#     elif text == '💅 Услуги':
#         bot.send_message(message.chat.id,
#                          "🛍️ <b>Выберите категорию услуг:</b>",
#                          reply_markup=services_categories())
#     elif text == '👩‍🎨 Наши мастера':
#         text_msg = "👩‍🎨 <b>Наши мастера</b>\n\nВыберите мастера, чтобы узнать подробнее:"
#         bot.send_message(message.chat.id, text_msg, reply_markup=masters_list_markup())
#     elif text == '📅 Записаться':
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton(
#             '🚀 Записаться онлайн',
#             url='https://n757778.yclients.com/company/712716/personal/menu?o='
#         ))
#         bot.send_message(
#             message.chat.id,
#             "💫 Переходи в онлайн-запись — выбери мастера, услугу и удобное время за 30 секунд!",
#             reply_markup=markup
#         )
#     elif text == '📞 Контакты':
#         contacts = (
#             "📍 <b>Бьютилаб</b>\n"
#             "ул. Щепкина 28, Москва\n"
#             "м. Проспект Мира\n\n"
#             "📞 <a href='tel:+79774498581'>+7 (977) 449-85-81</a>\n"
#             "🕒 Ежедневно 10:00–22:00\n\n"
#             "Напиши нам в любой момент — ответим максимально быстро ❤️"
#         )
#         bot.send_message(message.chat.id, contacts, reply_markup=main_keyboard())
#     elif text == '❓ Помощь':
#         help_text = (
#             "❓ <b>Нужна помощь?</b>\n\n"
#             "Если бот глючит, не открывается запись, не приходят сообщения или есть любые вопросы/пожелания — "
#             "пиши напрямую администратору:\n\n"
#             "👉 @ScreamLulzz\n\n"
#             "Мы ответим максимально быстро ❤️\n"
#             "Также можешь позвонить: +7 (933) 205-88-10"
#         )
#         bot.send_message(message.chat.id, help_text, reply_markup=main_keyboard())

# # ====================== CALLBACK ======================
# @bot.callback_query_handler(func=lambda call: True)
# def callback_handler(call):
#     if call.data == 'back_to_main':
#         try:
#             bot.delete_message(call.message.chat.id, call.message.message_id)
#         except:
#             pass
#         bot.send_message(call.message.chat.id, "Главное меню:", reply_markup=main_keyboard())
#     elif call.data == 'back_to_categories':
#         bot.edit_message_text(
#             "🛍️ <b>Выберите категорию услуг:</b>",
#             call.message.chat.id,
#             call.message.message_id,
#             reply_markup=services_categories()
#         )
#     elif call.data == 'back_to_masters':
#         bot.edit_message_text(
#             "👩‍🎨 <b>Наши мастера</b>\n\nВыберите мастера, чтобы узнать подробнее:",
#             call.message.chat.id,
#             call.message.message_id,
#             reply_markup=masters_list_markup()
#         )
#     elif call.data.startswith('cat_'):
#         category = call.data
#         if category == 'cat_nails':
#             text = (
#                 "<b>💅 Маникюр и педикюр</b>\n\n"
#                 "• Комплексный маникюр — 3100 ₽\n"
#                 "• Маникюр без покрытия — 1700 ₽\n"
#                 "• Наращивание ногтей — от 3990 ₽\n"
#                 "• Педикюр с покрытием Luxio — от 2550 ₽\n"
#                 "• Smart педикюр — 2300 ₽\n"
#                 "• Мужской/детский маникюр — от 800 ₽\n\n"
#                 "Все цены актуальны на март 2026. Точная стоимость зависит от выбранного покрытия."
#             )
#         elif category == 'cat_brows':
#             text = (
#                 "<b>🌟 Брови и ресницы</b>\n\n"
#                 "• Архитектура бровей — 1990 ₽\n"
#                 "• Окрашивание бровей — 1300 ₽\n"
#                 "• Ламинирование бровей — 3000 ₽\n"
#                 "• Наращивание ресниц 1D — 2490 ₽\n"
#                 "• Наращивание ресниц 2D–4D — от 3790 ₽"
#             )
#         elif category == 'cat_hair':
#             text = (
#                 "<b>💇‍♀️ Волосы</b>\n\n"
#                 "• Стрижка + укладка — 2490 ₽\n"
#                 "• Комплексный уход — 3490 ₽\n"
#                 "• Прикорневое окрашивание — от 4490 ₽\n"
#                 "• Сложное окрашивание Airtouch — 29900 ₽"
#             )
#         elif category == 'cat_makeup':
#             text = (
#                 "<b>💄 Макияж</b>\n\n"
#                 "• Дневной макияж — 3500 ₽\n"
#                 "• Вечерний макияж — 5000 ₽"
#             )
#         bot.edit_message_text(
#             text,
#             call.message.chat.id,
#             call.message.message_id,
#             reply_markup=back_to_services_markup()
#         )
#     elif call.data.startswith('master_'):
#         name = call.data.split('_', 1)[1]
#         master = next((m for m in MASTERS if m["name"] == name), None)
#         if master:
#             text = (
#                 f"<b>{master['name']}</b>\n\n"
#                 f"{master['spec']}\n"
#                 f"{master['rating']}\n\n"
#                 f"{master['info']}\n\n"
#                 "Хотите записаться именно к этому мастеру?"
#             )
#             markup = types.InlineKeyboardMarkup(row_width=2)
#             markup.add(
#                 types.InlineKeyboardButton('📅 Записаться', url='https://n757778.yclients.com/company/712716/personal/menu?o='),
#                 types.InlineKeyboardButton('« Назад к мастерам', callback_data='back_to_masters')
#             )
#             bot.edit_message_text(
#                 text,
#                 call.message.chat.id,
#                 call.message.message_id,
#                 reply_markup=markup
#             )

# # ====================== ЗАПУСК ======================
# if __name__ == '__main__':
#     print("🚀 Бот Бьютилаб запущен...")
#     bot.infinity_polling()

import telebot
from telebot import types

# ====================== НАСТРОЙКИ ======================
bot = telebot.TeleBot("ТОКЕН_СЮДА")  # ←←← СЮДА СВОЙ ТОКЕН

# Список мастеров (добавляй своих)
MASTERS = [
    {"name": "Анна", "spec": "💅 Мастер маникюра и педикюра", "rating": "⭐ 4.98 (127 отзывов)", "info": "Опыт 8 лет • Luxio • Smart педикюр"},
    {"name": "Мария", "spec": "🌟 Брови и ресницы", "rating": "⭐ 4.95 (89 отзывов)", "info": "Ламинирование • Архитектура • Наращивание 1D-4D"},
    {"name": "Елена", "spec": "💇‍♀️ Парикмахер-колорист", "rating": "⭐ 4.97 (64 отзыва)", "info": "Airtouch • Сложное окрашивание • Уход"},
    # Добавляй сюда сколько угодно мастеров
]

# ====================== КЛАВИАТУРЫ ======================
def main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('🛍 Услуги', callback_data='back_to_categories'),
        types.InlineKeyboardButton('👩‍🎨 Мастера', callback_data='back_to_masters')
    )
    markup.add(types.InlineKeyboardButton('☕🍹 Бесплатные напитки', callback_data='cat_drinks'))
    markup.add(types.InlineKeyboardButton('📍 Адрес • Контакты', url='https://yandex.ru/maps/...'))
    return markup

def services_categories():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('💅 Маникюр и педикюр', callback_data='cat_nails'),
        types.InlineKeyboardButton('🌟 Брови и ресницы', callback_data='cat_brows'),
        types.InlineKeyboardButton('💇‍♀️ Волосы', callback_data='cat_hair'),
        types.InlineKeyboardButton('💄 Макияж', callback_data='cat_makeup'),
        types.InlineKeyboardButton('☕🍹 Бесплатные напитки', callback_data='cat_drinks')
    )
    markup.add(types.InlineKeyboardButton('« Назад в главное меню', callback_data='back_to_main'))
    return markup

def back_to_services_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('« Назад к категориям услуг', callback_data='back_to_categories'))
    return markup

def masters_list_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for m in MASTERS:
        markup.add(types.InlineKeyboardButton(f"👤 {m['name']}", callback_data=f'master_{m["name"]}'))
    markup.add(types.InlineKeyboardButton('« Назад в главное меню', callback_data='back_to_main'))
    return markup

# ====================== СТАРТ ======================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в <b>Бьютилаб!</b>\n\n"
        "Мы рады видеть тебя ❤️\n"
        "Выбери, что тебе нужно:",
        reply_markup=main_keyboard(),
        parse_mode='HTML'
    )

# ====================== CALLBACK ======================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'back_to_main':
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, "Главное меню:", reply_markup=main_keyboard())

    elif call.data == 'back_to_categories':
        bot.edit_message_text(
            "🛍 <b>Выберите категорию услуг:</b>",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=services_categories(),
            parse_mode='HTML'
        )

    elif call.data == 'back_to_masters':
        bot.edit_message_text(
            "👩‍🎨 <b>Наши мастера</b>\n\nВыберите мастера, чтобы узнать подробнее:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=masters_list_markup(),
            parse_mode='HTML'
        )

    elif call.data.startswith('cat_'):
        category = call.data
        if category == 'cat_nails':
            text = (
                "<b>💅 Маникюр и педикюр</b>\n\n"
                "• Комплексный маникюр — 3100 ₽\n"
                "• Маникюр без покрытия — 1700 ₽\n"
                "• Наращивание ногтей — от 3990 ₽\n"
                "• Педикюр с покрытием Luxio — от 2550 ₽\n"
                "• Smart педикюр — 2300 ₽\n"
                "• Мужской/детский маникюр — от 800 ₽\n\n"
                "Все цены актуальны на март 2026. Точная стоимость зависит от выбранного покрытия."
            )
        elif category == 'cat_brows':
            text = (
                "<b>🌟 Брови и ресницы</b>\n\n"
                "• Архитектура бровей — 1990 ₽\n"
                "• Окрашивание бровей — 1300 ₽\n"
                "• Ламинирование бровей — 3000 ₽\n"
                "• Наращивание ресниц 1D — 2490 ₽\n"
                "• Наращивание ресниц 2D–4D — от 3790 ₽"
            )
        elif category == 'cat_hair':
            text = (
                "<b>💇‍♀️ Волосы</b>\n\n"
                "• Стрижка + укладка — 2490 ₽\n"
                "• Комплексный уход — 3490 ₽\n"
                "• Прикорневое окрашивание — от 4490 ₽\n"
                "• Сложное окрашивание Airtouch — 29900 ₽"
            )
        elif category == 'cat_makeup':
            text = (
                "<b>💄 Макияж</b>\n\n"
                "• Дневной макияж — 3500 ₽\n"
                "• Вечерний макияж — 5000 ₽"
            )
        elif category == 'cat_drinks':
            text = (
                "<b>☕🍹 Меню напитков</b>\n\n"
                "🎁 <i>Бесплатно для всех клиентов Бьютилаб!</i>\n\n"
                "<b>🍵 Чай</b>\n"
                "• Зелёный: классический / с мелиссой\n"
                "• Чёрный: с бергамотом / классический\n"
                "• Травяной: гибискус с малиной\n\n"
                "<b>☕ Кофе</b>\n"
                "• Эспрессо / Американо / Капучино / Латте\n\n"
                "🥛 <b>Выберите молоко:</b> миндальное • кокосовое • классическое\n\n"
                "🍯 <b>Сиропы:</b> ванильный • карамельный • миндальный • кокосовый\n\n"
                "🍋 <b>Дополнения:</b> корица • лимон\n\n"
                "<b>🥤 Вода</b>\n"
                "• Без газа / с лимоном\n\n"
                "<b>🥂 Для настроения</b>\n"
                "• Игристое сухое / вино белое\n\n"
                "✨ <i>Наслаждайтесь, приятного отдыха в Бьютилаб! 💖</i>"
            )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=back_to_services_markup(),
            parse_mode='HTML'
        )

    elif call.data.startswith('master_'):
        name = call.data.split('_', 1)[1]
        master = next((m for m in MASTERS if m["name"] == name), None)
        if master:
            text = (
                f"<b>{master['name']}</b>\n\n"
                f"{master['spec']}\n"
                f"{master['rating']}\n\n"
                f"{master['info']}\n\n"
                "Хотите записаться именно к этому мастеру?"
            )
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton('📅 Записаться онлайн', url='https://n757778.yclients.com/company/712716/personal/menu?o='),
                types.InlineKeyboardButton('« Назад к мастерам', callback_data='back_to_masters')
            )
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup,
                parse_mode='HTML'
            )

# ====================== ЗАПУСК ======================
if __name__ == '__main__':
    print("🚀 Бот Бьютилаб успешно запущен...")
    bot.infinity_polling()

