import aiogram
from create_bot import bot, dp
from config_tg.config import admin_id
from music.music_script_download import download  # импортируем функцию download, для скачивания музыки
# модуль для парсинга (вытягивания отдельных ссылок с запросов на Youtube)
from youtubesearchpython import VideosSearch, VideoDurationFilter, CustomSearch
import os, sys
import datetime
from data_base.sqlite_db import sql_start, sql_insert

# import logging
# logging.basicConfig(
#     aiogram_logic=[
#         logging.FileHandler("debug.log"),
#         logging.StreamHandler(sys.stdout)
#     ],
#     encoding='utf-8',
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(name)s\t| %(message)sm',
#     datefmt='%Y-%m-%d %I:%M:%S %p'
# )


# ======================== Проверка работоспособности (проверка токена) =========================================

async def send_to_myself(dp):
    sql_start()
    await bot.send_message(chat_id=admin_id, text='Бот запущен')
    print('Бот вышел в чат')


# Определяем функцию, которая ищет/скачивает композицию и возвращает нам имя скаченного/найденного файла
async def get_filename_song(query, song):
    """
    Определяем функцию, которая возвращает нам имя скаченного файла
    :param query:
    :param song:
    :return:
    """
    # создаем список, если id песни есть в папке (downloads_music) или пустой список - если такого id нет
    filename_find = [i for i in os.listdir('downloads_music') if song['id'] in i]
    if not filename_find:
        await query.answer('Прошу немного подождать, идёт загрузка трека')
        # функция, при помощи которой мы скачиваем видео из YouTube и переводим в Mp3 формат
        download(song['id'], query)

        filename_find = [i for i in os.listdir('downloads_music') if song['id'] in i]
    await query.answer('Скоро пришлем трек')
    filename = filename_find[0]
    return filename


#  функция, которая берет имя пользователя, название песни и дату когда пользователь запросил песню, и записывает в БД
def insert_music_data_in_db(query, song):
    users_name = query.from_user.first_name
    music_name = song['title']
    download_date = datetime.datetime.today()

    sql_insert(users_name, music_name, download_date)


#  функция возвращает данные песни которую выбрал пользователь на клавиатуре (имя, время, ссылку и тд...)
def get_data_song(query):
    data = query.data
    # метод достаёт всю информацию о 1-ом видео с YouTube (по ID песни)
    videosSearch_on_id = VideosSearch(data, limit=1)
    song = videosSearch_on_id.resultComponents[0]
    return song


#  получаем путь к запрошенной аудиозаписи перед отправкой пользователю
async def the_path_to_the_song(query):
    song = get_data_song(query)
    filename = await get_filename_song(query, song)  # определяем переменную filename
    insert_music_data_in_db(query, song)

    # try:
    # открытие файла типа open(), и InputFile запихивает указатель на этот файл (указываем путь к файлу)
    file_audio_send = aiogram.types.input_file.InputFile(rf'C:\Users\Admin\PycharmProjects\MusicTelegramBot\downloads_music\{filename}')
    # except:
    #     await query.answer('Произошла ошибка при загрузке трека')
    return file_audio_send

    # logging.info(f'SEND_AUDIO {query.from_user.id}, {file_audio_send}', exc_info=1)



