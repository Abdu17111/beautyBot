def is_greeting(text):
    greetings = ["привет", "здравствуй", "добрый", "hello", "hi", "доброе", "день", "вечер", "утро", "хай", "салам", "здарова"]
    return any(g in text.lower() for g in greetings)