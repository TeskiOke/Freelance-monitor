import feedparser
import time
import requestspython test_tg.py

# --- НАСТРОЙКИ ---
# Вставь сюда токен от @BotFather
TELEGRAM_TOKEN = "ВАШ_ТОКЕН_ТУТ"
# Вставь сюда свой ID (можно узнать у @userinfobot)
CHAT_ID = "ВАШ_CHAT_ID_ТУТ"

# Ссылка на RSS Freelancehunt (Программирование)
RSS_URL = "https://freelancehunt.com/projects.rss?category=1"

# Ключевые слова для фильтрации
KEYWORDS = ["python", "android", "kotlin", "парсинг", "автоматизация", "скрипт"]

def send_telegram(message):
    if TELEGRAM_TOKEN == "ВАШ_ТОКЕН_ТУТ":
        print(f"[ТЕЛЕГРАМ - НЕ НАСТРОЕНО]: {message[:100]}...")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})
    except Exception as e:
        print(f"Ошибка отправки в TG: {e}")

def monitor():
    print("Запуск мониторинга Freelancehunt...")
    seen_ids = set()
    
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            for entry in feed.entries:
                if entry.id not in seen_ids:
                    title = entry.title.lower()
                    description = entry.description.lower()
                    
                    # Проверяем наличие ключевых слов
                    if any(word in title or word in description for word in KEYWORDS):
                        msg = f"<b>Новый заказ!</b>\n\n<b>{entry.title}</b>\n\n{entry.link}"
                        send_telegram(msg)
                        print(f"Найдено: {entry.title}")
                    
                    seen_ids.add(entry.id)
            
            # Ограничиваем размер сета, чтобы не забивать память
            if len(seen_ids) > 100:
                seen_ids.clear()
                
        except Exception as e:
            print(f"Ошибка при парсинге: {e}")
            
        time.sleep(60) # Проверка каждую минуту

if __name__ == "__main__":
    monitor()
