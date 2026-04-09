import os
import json
import time
from collections import deque
from urllib.parse import quote
from dotenv import load_dotenv
import telebot
from telebot import types

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    print("❌ Добавь BOT_TOKEN в .env файл!")
    exit()

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

ADMIN_ID = 6177817315  # ←←← ТВОЙ ID

# ====================== ХРАНИЛИЩЕ ======================
USERS_FILE = "users.json"
BANNED_FILE = "banned.json"

try:
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = set(json.load(f))
except:
    users = set()

try:
    with open(BANNED_FILE, "r", encoding="utf-8") as f:
        banned_users = set(json.load(f))
except:
    banned_users = set()

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(users), f)

def save_banned():
    with open(BANNED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(banned_users), f)

# ====================== ПРОДВИНУТАЯ АНТИСПАМ (обновлено по твоей просьбе) ======================
SPAM_SETTINGS = {
    'max_messages_60s': 12,
    'flood_threshold': 7,
    'flood_window': 10,
    'temp_ban_time': 900,        # ← 15 минут (как ты просил)
}

user_messages = {}
temp_bans = {}

def is_banned(chat_id):
    if chat_id in banned_users:
        return True
    if chat_id in temp_bans and time.time() < temp_bans[chat_id]:
        return True
    return False

def check_spam(chat_id):
    if chat_id == ADMIN_ID:          # Админ имеет полный иммунитет
        return False
    if is_banned(chat_id):
        return True

    now = time.time()

    if chat_id not in user_messages:
        user_messages[chat_id] = deque(maxlen=50)

    while user_messages[chat_id] and user_messages[chat_id][0] < now - 60:
        user_messages[chat_id].popleft()

    user_messages[chat_id].append(now)

    ban_message = (
        "🚫 <b>Временный бан за спам!</b>\n\n"
        "Здравствуйте! Вы отправили слишком много сообщений подряд.\n"
        "Бот заблокировал вас на <b>15 минут</b> для защиты от спама.\n\n"
        "Через 15 минут можете писать снова. Спасибо за понимание ❤️"
    )

    # Rate-limit
    if len(user_messages[chat_id]) > SPAM_SETTINGS['max_messages_60s']:
        temp_bans[chat_id] = now + SPAM_SETTINGS['temp_ban_time']
        print(f"🚫 RATE-LIMIT: Пользователь {chat_id} получил бан на 15 минут")
        try:
            bot.send_message(chat_id, ban_message)
        except:
            pass
        return True

    # Flood
    recent = [t for t in user_messages[chat_id] if t > now - SPAM_SETTINGS['flood_window']]
    if len(recent) > SPAM_SETTINGS['flood_threshold']:
        temp_bans[chat_id] = now + SPAM_SETTINGS['temp_ban_time']
        print(f"🚫 FLOOD: Пользователь {chat_id} получил бан на 15 минут")
        try:
            bot.send_message(chat_id, ban_message)
        except:
            pass
        return True

    return False

# ====================== КЛАВИАТУРЫ ======================
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('👋 О нас')
    btn2 = types.KeyboardButton('💅 Услуги')
    btn3 = types.KeyboardButton('☕🍹 Угощения')
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
    if check_spam(message.chat.id):
        return
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
    if message.from_user.id != ADMIN_ID:
        return
    sent = 0
    for uid in list(users):
        try:
            bot.send_message(uid, "🔄 Бот обновлён!\n\nМы добавили новые удобства и улучшения ❤️\nЧтобы увидеть все свежие изменения — пожалуйста, просто отправьте боту команду\n\n/start\n\nЭто займёт 2 секунды, и дальше всё будет обновляться автоматически ✨\nСпасибо, что вы с нами!")
            sent += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ Сообщение отправлено {sent} пользователям!")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        user_to_ban = int(message.text.split()[1])
        banned_users.add(user_to_ban)
        save_banned()
        if user_to_ban in temp_bans:
            del temp_bans[user_to_ban]
        bot.reply_to(message, f"✅ Пользователь {user_to_ban} добавлен в перманентный чёрный список")
    except:
        bot.reply_to(message, "Использование: /ban <chat_id>")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        user_to_unban = int(message.text.split()[1])
        banned_users.discard(user_to_unban)
        if user_to_unban in temp_bans:
            del temp_bans[user_to_unban]
        save_banned()
        bot.reply_to(message, f"✅ Пользователь {user_to_unban} полностью разбанен")
    except:
        bot.reply_to(message, "Использование: /unban <chat_id>")

@bot.message_handler(commands=['myid'])
def my_id(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.reply_to(message, f"🔑 <b>Твой chat_id:</b> <code>{message.chat.id}</code>")

@bot.message_handler(commands=['banlist'])
def ban_list(message):
    if message.from_user.id != ADMIN_ID:
        return
    now = time.time()
    for uid in list(temp_bans.keys()):
        if temp_bans[uid] <= now:
            del temp_bans[uid]

    perm = sorted(list(banned_users))
    temp_list = []
    for uid, until in sorted(temp_bans.items()):
        remaining = max(0, int(until - now))
        temp_list.append(f"{uid} — {remaining} сек")

    text = "📋 <b>Бан-лист</b>\n\n"
    text += f"🛑 <b>Перманентные баны</b> ({len(perm)}):\n" + ("\n".join(map(str, perm)) if perm else "— пусто\n")
    text += f"\n\n⏳ <b>Временные баны</b> ({len(temp_list)}):\n" + ("\n".join(temp_list) if temp_list else "— пусто")
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ['привет', 'здравствуй', 'добрый день', 'доброе утро', 'добрый вечер', 'хай', 'hello', 'hi', 'здрасьте'])
def hello(message):
    if check_spam(message.chat.id):
        return
    users.add(message.chat.id)
    save_users()
    start(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if check_spam(message.chat.id):
        return
    users.add(message.chat.id)
    save_users()
    text = message.text

    if text == '👋 О нас':
        about = "✨ <b>Бьютилаб</b> — студия красоты у метро Проспект Мира.\n\n📍 Адрес: Москва, ул. Щепкина, 28\n\nМы создаём пространство, где каждая девушка чувствует заботу, комфорт и результат.\nСтерильность, современные материалы, опытные мастера и никакого стресса."
        bot.send_message(message.chat.id, about, reply_markup=main_keyboard())
        bot.send_location(message.chat.id, 55.77393, 37.63198)
    elif text == '💅 Услуги':
        bot.send_message(message.chat.id, "🛍️ <b>Выберите категорию услуг:</b>", reply_markup=services_categories())
    elif text == '☕🍹 Угощения':
        bot.send_message(message.chat.id, " <b>🍹Угощения для наших любимых гостей</b>\n\nВыберите, что хотите попробовать 👇", reply_markup=drinks_menu_markup())
    elif text == '📅 Записаться':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('🚀 Записаться онлайн', url='https://n757778.yclients.com/company/712716/personal/menu?o='))
        bot.send_message(message.chat.id, "💫 Переходи в онлайн-запись — выбери мастера, услугу и удобное время за 30 секунд!", reply_markup=markup)
    elif text == '📞 Контакты':
        contacts = "📍 <b>Бьютилаб</b>\nул. Щепкина 28, Москва\nм. Проспект Мира\n\n📞 <a href='tel:+79774498581'>+7 (977) 449-85-81</a>\n🕒 Ежедневно 10:00–22:00\n\n📱 <a href='https://t.me/Wish_Lab'> Администратор салона @Wish_Lab</a>\n\nНапиши нам в любой момент — ответим максимально быстро ❤️"
        bot.send_message(message.chat.id, contacts, reply_markup=main_keyboard())
    elif text == '❓ Помощь':
        help_text = "❓ <b>Нужна помощь?</b>\n\nЕсли бот глючит, не открывается запись, не приходят сообщения или есть любые вопросы/пожелания — пиши напрямую тех разработчику:\n\n👉 @ScreamLulzz\n\nМы ответим максимально быстро ❤️\nТакже можешь позвонить: +7 (933) 205-88-10"
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

    # ==================== УГОЩЕНИЯ С АВТОЗАПОЛНЕНИЕМ ====================
    elif call.data in ['drink_tea', 'drink_coffee', 'drink_milk', 'drink_syrup', 'drink_add', 'drink_water', 'drink_mood']:
        texts = {
            'drink_tea': ("🍵 <b>Чай</b>\n\n• Зелёный: классический / с мелиссой\n• Чёрный: с бергамотом / классический\n• Травяной: гибискус с малиной", "Здравствуйте! Хочу заказать чай 🍵"),
            'drink_coffee': ("☕ <b>Кофе</b>\n\n• Эспрессо / Американо / Капучино / Латте", "Здравствуйте! Хочу заказать кофе ☕"),
            'drink_milk': ("🥛 <b>Молоко на выбор</b>\n\n• миндальное • кокосовое • классическое", "Здравствуйте! Хочу выбрать молоко для напитка 🥛"),
            'drink_syrup': ("🍯 <b>Сиропы</b>\n\n• ванильный • карамельный • миндальный • кокосовый", "Здравствуйте! Хочу добавить сиропы 🍯"),
            'drink_add': ("🍋 <b>Дополнения</b>\n\n• корица • лимон", "Здравствуйте! Хочу добавить корицу и/или лимон 🍋"),
            'drink_water': ("🥤 <b>Вода</b>\n\n• Без газа / с лимоном", "Здравствуйте! Хочу заказать воду 🥤"),
            'drink_mood': ("🥂 <b>Для настроения</b>\n\n• Игристое сухое / вино белое", "Здравствуйте! Хочу напиток для настроения 🥂")
        }
        text, pre = texts[call.data]
        markup = types.InlineKeyboardMarkup()
        pre_text = quote(pre)
        markup.add(types.InlineKeyboardButton('✍️ Написать @Wish_Lab', url=f'https://t.me/Wish_Lab?text={pre_text}'))
        markup.add(types.InlineKeyboardButton('« Назад в меню↩️', callback_data='back_to_drinks'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'back_to_drinks':
        bot.edit_message_text("🍹 <b>Угощения для наших любимых гостей</b>\n\nВыберите, что хотите попробовать 👇", call.message.chat.id, call.message.message_id, reply_markup=drinks_menu_markup())

# ====================== ЗАПУСК ======================
if __name__ == '__main__':
    print("🚀 Бот Бьютилаб запущен! Временный бан теперь 15 минут + сообщение пользователю")
    bot.infinity_polling()
