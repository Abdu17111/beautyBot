import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    master TEXT,
                    date TEXT,
                    time TEXT,
                    duration INTEGER,
                    name TEXT,
                    phone TEXT,
                    created_at TEXT,
                    status TEXT DEFAULT 'active')''')
    conn.commit()
    conn.close()

def add_booking(user_id, master, date, time, duration, name, phone):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""INSERT INTO bookings 
                 (user_id, master, date, time, duration, name, phone, created_at, status) 
                 VALUES (?,?,?,?,?,?,?,?,?)""",
              (user_id, master, date, time, duration, name, phone, now, 'active'))
    conn.commit()
    conn.close()

def get_master_bookings_on_date(master, date):
    """Возвращает все активные записи мастера на указанную дату"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT time, duration FROM bookings WHERE master=? AND date=? AND status='active'",
              (master, date))
    rows = c.fetchall()
    conn.close()
    return rows

def is_slot_free(master, date, start_time_str, duration_min):
    """Проверяет, свободен ли слот с учётом длительности и пересечений"""
    bookings = get_master_bookings_on_date(master, date)
    if not bookings:
        return True

    # Преобразуем start_time в минуты с начала дня
    def time_to_minutes(t_str):
        h, m = map(int, t_str.split(':'))
        return h * 60 + m

    proposed_start = time_to_minutes(start_time_str)
    proposed_end = proposed_start + duration_min

    for booked_time_str, booked_dur in bookings:
        booked_start = time_to_minutes(booked_time_str)
        booked_end = booked_start + booked_dur

        # Пересечение: не (proposed_end <= booked_start или proposed_start >= booked_end)
        if not (proposed_end <= booked_start or proposed_start >= booked_end):
            return False

    return True

def get_user_bookings(user_id):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT id, master, date, time, duration FROM bookings WHERE user_id=? AND status='active'", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def cancel_booking(booking_id):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()