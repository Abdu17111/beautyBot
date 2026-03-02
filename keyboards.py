from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import MASTERS, POSSIBLE_TIMES
from database import is_slot_free
from datetime import datetime, timedelta

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📅 Записаться на маникюр")
    markup.add("📋 Мои записи", "❓ Помощь")
    return markup

def masters_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    for master in MASTERS:
        markup.add(InlineKeyboardButton(master, callback_data=f"master_{master}"))
    return markup

def duration_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("60 минут", callback_data="dur_60"))
    markup.add(InlineKeyboardButton("90 минут", callback_data="dur_90"))
    return markup

def date_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)
    today = datetime.now()
    for i in range(14):
        d = today + timedelta(days=i)
        date_str = d.strftime("%d.%m (%a)")
        callback = f"date_{d.strftime('%Y-%m-%d')}"
        markup.add(InlineKeyboardButton(date_str, callback_data=callback))
    return markup

def time_keyboard(date, master, duration):
    markup = InlineKeyboardMarkup(row_width=3)
    free_slots = 0
    for t in POSSIBLE_TIMES:
        if is_slot_free(master, date, t, duration):
            text = f"{t} ✅"
            markup.add(InlineKeyboardButton(text, callback_data=f"time_{t}"))
            free_slots += 1
    if free_slots == 0:
        markup.add(InlineKeyboardButton("😔 Нет свободных слотов", callback_data="no_slots"))
    return markup