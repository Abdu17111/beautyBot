import telebot
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, SALON_NAME
from database import init_db, add_booking, get_user_bookings, cancel_booking, is_slot_free
from keyboards import main_menu, masters_keyboard, duration_keyboard, date_keyboard, time_keyboard
from utils import is_greeting
from datetime import datetime
import time
import sqlite3

bot = telebot.TeleBot(BOT_TOKEN)

user_state = {}
user_data = {}

# ─── СПЕЦИАЛЬНЫЕ ХЕНДЛЕРЫ (имя → телефон) ────────────────────────────────────────
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "entering_name")
def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["name"] = message.text.strip()
    user_state[chat_id] = "entering_phone"
    bot.send_message(chat_id, "Введите ваш номер телефона (например +7 999 123-45-67):")


@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "entering_phone")
def get_phone(message):
    chat_id = message.chat.id
    data = user_data[chat_id]
    phone = message.text.strip()

    add_booking(
        chat_id, data["master"], data["date"], data["time"],
        data["duration"], data["name"], phone
    )

    admin_text = (
        "💅 НОВАЯ ЗАПИСЬ\n\n"
        f"Мастер: {data['master']}\n"
        f"Дата и время: {data['date']} {data['time']}\n"
        f"Длительность: {data['duration']} мин\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {phone}\n"
        f"Клиент: @{message.from_user.username or 'нет'}"
    )

    try:
        bot.send_message(ADMIN_ID, admin_text)
        print(f"Уведомление админу отправлено")
    except Exception as e:
        print(f"Ошибка уведомления админу: {e}")

    bot.send_message(
        chat_id,
        f"✅ Запись подтверждена!\n\n"
        f"🗓 {data['date']} в {data['time']}\n"
        f"👩‍🎨 {data['master']}\n"
        f"⏱ {data['duration']} мин\n\n"
        f"Ждём вас! 💅",
        reply_markup=main_menu()
    )

    user_state.pop(chat_id, None)
    user_data.pop(chat_id, None)


# ─── КОМАНДЫ ДЛЯ ТЕСТА И СБРОСА ─────────────────────────────────────────────────
@bot.message_handler(commands=['test_admin'])
def test_admin(message):
    try:
        bot.send_message(ADMIN_ID, "🧪 ТЕСТ УВЕДОМЛЕНИЯ\nЕсли видишь — всё работает!")
        bot.send_message(message.chat.id, "Тест отправлен в группу/личку")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка теста: {str(e)}")


@bot.message_handler(commands=['cancel'])
def cancel_state(message):
    chat_id = message.chat.id
    user_state.pop(chat_id, None)
    user_data.pop(chat_id, None)
    bot.send_message(chat_id, "Состояние сброшено. Нажми /start", reply_markup=main_menu())


# ─── ОБЩИЙ ОБРАБОТЧИК СООБЩЕНИЙ ──────────────────────────────────────────────────
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    chat_id = message.chat.id
    if not message.text:
        return

    text = message.text.strip()
    text_lower = text.lower()

    print(f"[DEBUG] Получено сообщение: '{text}' (от {chat_id})")  # ← для отладки

    if user_state.get(chat_id):
        return

    if is_greeting(text):
        bot.send_message(chat_id,
                         "Привет! Хотите записаться? Нажмите кнопку ниже 👇",
                         reply_markup=main_menu())
        return

    # Записаться на маникюр
    if "записаться" in text_lower or "маникюр" in text_lower:
        user_state[chat_id] = "choosing_master"
        bot.send_message(chat_id, "Выберите мастера:", reply_markup=masters_keyboard())
        return

    # Мои записи
    if "мои записи" in text_lower or "записи" in text_lower:
        bookings = get_user_bookings(chat_id)
        if not bookings:
            bot.send_message(chat_id, "У вас нет активных записей 😊")
            return

        text_reply = "📋 Ваши записи:\n\n"
        markup = types.InlineKeyboardMarkup(row_width=1)
        has_active = False

        for b in bookings:
            booking_id, master, date, time_str, duration = b
            try:
                booking_dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
                if booking_dt <= datetime.now():
                    text_reply += f"🗓 {date} {time_str} — {master} ({duration} мин) [прошла]\n"
                    continue
            except:
                pass

            text_reply += f"🗓 {date} {time_str} — {master} ({duration} мин)\n"
            markup.add(types.InlineKeyboardButton(
                f"❌ Отменить {date} {time_str}",
                callback_data=f"cancel_confirm_{booking_id}"
            ))
            has_active = True

        if not has_active:
            text_reply += "\nВсе записи уже прошли или отменены."

        bot.send_message(chat_id, text_reply, reply_markup=markup)
        return

    # Помощь
    if "помощь" in text_lower or "?" in text or "помоги" in text_lower:
        bot.send_message(chat_id, "По всем вопросам пишите @ваш_логин\nИли просто нажмите «Записаться на маникюр» 💅")
        return

    # Если ничего не подошло
    bot.send_message(chat_id, "Не понял команду 😅\nПопробуйте кнопки ниже:", reply_markup=main_menu())


# ─── CALLBACKS ───────────────────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id

    if call.data.startswith("master_"):
        master = call.data.split("_", 1)[1]
        user_data[user_id] = {"master": master}
        user_state[user_id] = "choosing_duration"
        bot.edit_message_text("Выберите длительность:", user_id, call.message.message_id,
                              reply_markup=duration_keyboard())

    elif call.data.startswith("dur_"):
        duration = int(call.data.split("_")[1])
        user_data[user_id]["duration"] = duration
        user_state[user_id] = "choosing_date"
        bot.edit_message_text("Выберите дату:", user_id, call.message.message_id,
                              reply_markup=date_keyboard())

    elif call.data.startswith("date_"):
        date = call.data.split("_")[1]
        user_data[user_id]["date"] = date
        user_state[user_id] = "choosing_time"
        master = user_data[user_id]["master"]
        duration = user_data[user_id]["duration"]
        bot.edit_message_text(
            f"Свободные слоты на {date} для {master} ({duration} мин):",
            user_id,
            call.message.message_id,
            reply_markup=time_keyboard(date, master, duration)
        )

    elif call.data.startswith("time_"):
        time_slot = call.data.split("_")[1]
        user_data[user_id]["time"] = time_slot
        user_state[user_id] = "entering_name"
        bot.edit_message_text("Введите ваше имя:", user_id, call.message.message_id)

    elif call.data.startswith("cancel_confirm_"):
        booking_id = int(call.data.split("_")[2])

        conn = sqlite3.connect('bookings.db')
        c = conn.cursor()
        c.execute("SELECT user_id, master, date, time, duration, name, phone FROM bookings WHERE id=?", (booking_id,))
        row = c.fetchone()
        conn.close()

        if row:
            user_id_db, master, date, time_str, duration, name, phone = row
            cancel_text = (
                "❌ ОТМЕНА ЗАПИСИ\n\n"
                f"Мастер: {master}\n"
                f"Дата и время: {date} {time_str}\n"
                f"Длительность: {duration} мин\n"
                f"Имя: {name}\n"
                f"Телефон: {phone}\n"
                f"Клиент: @{call.from_user.username or 'нет'} (ID: {user_id_db})"
            )
            try:
                bot.send_message(ADMIN_ID, cancel_text)
                print(f"Уведомление об отмене отправлено")
            except Exception as e:
                print(f"Ошибка уведомления об отмене: {e}")

        cancel_booking(booking_id)
        bot.answer_callback_query(call.id, "Запись отменена ✅")

        bot.edit_message_text(
            "✅ Запись успешно отменена!\nМожете записаться заново.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )


# ─── START ───────────────────────────────────────────────────────────────────────
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"👋 Добро пожаловать в **{SALON_NAME}**!\n\n"
        "💅 Запишитесь на маникюр за 30 секунд\n"
        "Работаем ежедневно 10:00 — 22:00",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


# ─── ЗАПУСК С ДИАГНОСТИКОЙ ───────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("🤖 Бот запущен")
    print(f"Админ (группа): {ADMIN_ID}")
    print(f"Токен (первые 10 символов): {BOT_TOKEN[:10]}...")

    while True:
        try:
            print("→ Запуск polling... (ожидаю сообщений)")
            bot.infinity_polling(
                none_stop=True,
                interval=0,
                timeout=10,
                long_polling_timeout=15,
                skip_pending=False,
                allowed_updates=["message", "callback_query", "edited_message"]
            )
            print("Polling завершился без исключения (странно)")
        except Exception as e:
            print(f"!!! ОШИБКА POLLING: {type(e).__name__} — {str(e)}")
            print("Перезапуск через 5 сек...")
            time.sleep(5)