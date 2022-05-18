from youtubesearchpython import *
import yt_dlp

# a = CustomSearch('Крек+нежность', VideoSortOrder.viewCount, limit=5)
# print(a.result())

# get_time_1 = '3:51| KREC - Нежность-5.4K'
# get_time_1 = '3:51| KREC - Нежность-5.4M'
#


# get_time = '3:49:58| #KREC - Лучшеe-50.7M'
#
#
# def len_time(get_time: str):
#     index_music = get_time.rfind('-')
#     for i in get_time[index_music+1:]:
#         if 'M' in get_time[index_music+1:]:
#             new_get_time = int(get_time[index_music+1:-1])
#             if new_get_time > 50:
#                 return False
#             else:
#                 return True
#         elif 'K' in get_time[index_music+1:]:
#             return True
#         else:
#             return False
#
#
# len_time(get_time)


# def len_time(string_numeric: str):
#     index_music = string_numeric.find('|')
#     count_num = ''
#     for i in string_numeric[:index_music]:
#         if i.isnumeric():
#             count_num += i
#     return len(count_num)
#






# music_options = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '310',
#
#     }],
# }
#
#
# def download(song: str):
#     """
#     Функция для скачивания и преобразования в Mp3 формат
#     :param song: ссылка на видео в Youtube
#     :return: ничего не возвращает (None)
#     """
#     with yt_dlp.YoutubeDL(music_options) as ydl:
#         ydl.add_default_info_extractors()
#         finished_hook_called = set()
#
#         def _hook(status):
#             if status['status'] == 'finished':
#                 finished_hook_called.add(status['filename'])
#
#         ydl.add_progress_hook(_hook)
#
#         ydl.download(song)
#
# download('https://www.youtube.com/watch?v=WywSogtPfFc')
#
#
