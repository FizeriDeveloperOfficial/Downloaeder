# main.py
from downloader import process_and_send_playlist
from bot import send_track_to_channel

def main():
    print("=== YouTube/SoundCloud to Telegram Music Bot ===")
    playlist_url = input("Введите ссылку на плейлист или видео: ").strip()
    
    if not playlist_url:
        print("Ссылка не может быть пустой.")
        return
        
    print("\nНачинаем обработку...")
    
    # Мы передаем функцию send_track_to_channel как коллбек.
    # Как только трек скачается, downloader вызовет эту функцию.
    process_and_send_playlist(
        playlist_url=playlist_url,
        on_download_finished=send_track_to_channel
    )
    
    print("\n🎉 Все треки из плейлиста скачаны и отправлены в канал!")

if __name__ == "__main__":
    main()