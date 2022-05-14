import youtube_dl  # модуль для скачивания файлов с Youtube
import yt_dlp  # скорость скачивания быстрее чем у youtube_dl

#  Конструкция преобразования файла из любого формата в Mp3

music_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '310',
    }],
}

# Функция для скачивания и преобразования в Mp3 формат песню

def download(songs):
    with yt_dlp.YoutubeDL(music_options) as ydl:
        ydl.download(songs)
