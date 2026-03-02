import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

SALON_NAME = "Nail Harmony Studio Москва"

MASTERS = [
    "Анна Смирнова",
    "Мария Иванова",
    "Екатерина Петрова",
    "Ольга Сидорова",
    "Дарья Козлова",
    "София Морозова"
]

# Слоты каждые 30 минут с 10:00 до 21:30
POSSIBLE_TIMES = [f"{h:02d}:{m:02d}" for h in range(10, 22) for m in (0, 30) if not (h == 21 and m == 30)]