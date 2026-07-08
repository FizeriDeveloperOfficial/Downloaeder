# downloader.py
import yt_dlp
import os
from config import DOWNLOAD_FOLDER

def get_ydl_opts():
    return {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "writethumbnail": True,
        "embedthumbnail": True,
        "addmetadata": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
        "quiet": False, # Можно поставить True, чтобы скрыть логи скачивания
    }

def process_and_send_playlist(playlist_url: str, on_download_finished: callable):
    """
    Извлекает плейлист, скачивает треки по одному и вызывает коллбек для отправки.
    """
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    
    with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
        print("Получение информации о плейлисте (это может занять время)...")
        # Извлекаем инфу, но пока не качаем весь плейлист разом
        info_dict = ydl.extract_info(playlist_url, download=False)
        
        # Проверяем, плейлист это или одиночное видео
        entries = info_dict.get('entries', [info_dict])
        
        for entry in entries:
            if not entry:
                continue
                
            video_url = entry.get('original_url') or entry.get('webpage_url')
            if not video_url:
                continue
                
            print(f"\n--- Скачивание трека: {entry.get('title')} ---")
            
            # Скачиваем конкретный трек
            track_info = ydl.extract_info(video_url, download=True)
            
            # Достаем метаданные
            title = track_info.get('title', 'Неизвестное название')
            # Пытаемся взять исполнителя (artist), если нет - берем автора канала (uploader)
            author = track_info.get('artist') or track_info.get('uploader') or 'Неизвестный автор'
            
            # Определяем финальное имя файла после конвертации в mp3
            filename = ydl.prepare_filename(track_info)
            final_filename = os.path.splitext(filename)[0] + ".mp3"
            
            if os.path.exists(final_filename):
                # Передаем файл и данные в Telegram-бота
                on_download_finished(final_filename, title, author)
            else:
                print(f"Файл {final_filename} не найден после скачивания.")