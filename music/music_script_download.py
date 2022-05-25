# import youtube_dl  # модуль для скачивания файлов с Youtube
import yt_dlp  # скорость скачивания быстрее чем у youtube_dl

# даём имя папке в которую будем загружать треки и компонуем название трека
fpath = f"downloads_music/%(title)s   %(id)s.%(ext)s"

# Параметры, которые передаем в init при создании экземпляра класса
music_options = {

    'format': 'bestaudio/best',
    "outtmpl": fpath,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '310',

    }],
}

# Функция для скачивания и преобразования в Mp3 формат (song: ссылка на видео в Youtube)
def download(song: str):

    with yt_dlp.YoutubeDL(music_options) as ydl:
        ydl.download(song)


# string_numeric = '3:51| KREC - Нежность'

# todo: написать функцию, которая подсчитывает секунды в трек
# Функция подсчитывает количество цифр в продолжительности трека (string_numeric: строка с продолжительностью трека)
def len_time(string_numeric: str) -> int:

    index_music = string_numeric.find('|')
    len_num = 0
    for i in string_numeric[:index_music]:
        if i.isnumeric():
            len_num += 1
    return len_num


