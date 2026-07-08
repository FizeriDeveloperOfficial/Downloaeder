# bot.py
import telebot
from config import BOT_TOKEN, CHANNEL_ID

# Инициализируем бота
bot = telebot.TeleBot(BOT_TOKEN)

def send_track_to_channel(file_path: str, title: str, author: str):
    """
    Отправляет аудиофайл в Telegram-канал с нужной подписью.
    """
    # Формируем подпись: Название - Автор
    caption_text = f"{title} - {author}"
    
    print(f"Отправка в Telegram: {caption_text}...")
    
    try:
        with open(file_path, 'rb') as audio_file:
            bot.send_audio(
                chat_id=CHANNEL_ID,
                audio=audio_file,
                caption=caption_text,
                title=title,
                performer=author
            )
        print(f"✅ Успешно отправлено: {title}")
    except Exception as e:
        print(f"❌ Ошибка при отправке {title} в Telegram: {e}")
