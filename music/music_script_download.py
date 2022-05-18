import youtube_dl  # модуль для скачивания файлов с Youtube
import yt_dlp  # скорость скачивания быстрее чем у youtube_dl

# даём имя папке в которую будем загружать треки и компонуем название трека
fpath = f"downloads_music/%(title)s   %(id)s.%(ext)s"
#  Конструкция преобразования файла из любого формата в Mp3
music_options = {

    'format': 'bestaudio/best',
    "outtmpl": fpath,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '310',

    }],
}


#  Функция для скачивания видео с YouTube и преобразования в Mp3 формат

def download(song: str, query=None):

    """
    Функция для скачивания и преобразования в Mp3 формат
    :param song: ссылка на видео в Youtube
    :return: ничего не возвращает (None)
    """

    with yt_dlp.YoutubeDL(music_options) as ydl:
        ydl.download(song)


# string_numeric = '3:51| KREC - Нежность'

# todo: написать функцию, которая подсчитывает секунды в треке
# функция подсчитывает количество цифр в продолжительности трека
def len_time(string_numeric: str):
    """
    Функция подсчитывает количество цифр в продолжительности трека
    :param string_numeric: строка с продолжительностью трека в формате: '3:51| KREC - Нежность'
    :return: количество цифр в строке
    """
    index_music = string_numeric.find('|')
    len_num = 0
    for i in string_numeric[:index_music]:
        if i.isnumeric():
            len_num += 1
    return len_num


