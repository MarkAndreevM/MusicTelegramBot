# import youtube_dl  # модуль для скачивания файлов с Youtube
import yt_dlp  # скорость скачивания быстрее чем у youtube_dl

# даём имя папке в которую будем загружать треки и компонуем название трека
fpath = f"downloads_music/%(title)s   %(id)s.%(ext)s"

# Параметры, которые передаем в init при создании экземпляра класса
music_options = {
    'format': 'bestaudio/best',
    "outtmpl": fpath,
}


# Функция для скачивания и преобразования в Mp3 формат (song: ссылка на видео в Youtube)
def download(song: str):

    with yt_dlp.YoutubeDL(music_options) as ydl:
        ydl.download(song)


# string_numeric = '3:51| KREC - Нежность'
# Функция подсчитывает количество секунд в треке (string_numeric: строка с продолжительностью трека)
def long_time(string_numeric):
    index_music = string_numeric.find('|')
    string_time = string_numeric[:index_music]

    if string_time.count(':') <= 1:
        ftr = [60, 1]
        return sum([a * b for a, b in zip(ftr, map(int, string_time.split(':')))])
    else:
        ftr = [3600, 60, 1]
        return sum([a * b for a, b in zip(ftr, map(int, string_time.split(':')))])


# # OLD Функция подсчитывает кол-во цифр в продолжительности трека (string_numeric: строка с продолжительностью трека)
# def len_time(string_numeric: str) -> int:
#
#     index_music = string_numeric.find('|')
#     len_num = 0
#     for i in string_numeric[:index_music]:
#         if i.isnumeric():
#             len_num += 1
#     return len_num






