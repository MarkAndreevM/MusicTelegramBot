import yt_dlp  # скорость скачивания быстрее чем у youtube_dl
from youtubesearchpython import VideosSearch, VideoDurationFilter, CustomSearch


fpath = f"downloads/%(title)s   %(id)s.%(ext)s"
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
        x = ydl.extract_info(song, download=True)


download('https://www.youtube.com/watch?v=JRXJ1aT8Q4A')



