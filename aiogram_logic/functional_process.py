import datetime
import logging
import os

import aiogram
from youtubesearchpython import VideosSearch

from config_tg.config import admin_id
from music.music_script_download import download
from data_base.sqlite_db import sql_start, sql_insert

import csv
# ======================== Проверка работоспособности (проверка токена) =========================================


async def send_to_myself(dp):
    sql_start()
    await dp.bot.send_message(chat_id=admin_id, text='Бот запущен')

    # создаем csv файл (записываем названия столбцов) --> для дальнейшей работы в pandas
    with open("data.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["users_id", "music_name", "download_date"])

    print('Бот вышел в чат')


# Определяем функцию, которая ищет/скачивает композицию и возвращает нам имя скаченного/найденного файла.
async def get_filename_song(query, song):

    # создаем список, если id песни есть в папке (downloads_music) или пустой список - если такого id нет
    filename_find = [i for i in os.listdir('downloads_music') if song['id'] in i]
    if not filename_find:
        await query.answer('Прошу немного подождать, идёт загрузка трека')
        # функция, при помощи которой мы скачиваем видео из YouTube и переводим в Mp3 формат
        download(song['id'])

        filename_find = [i for i in os.listdir('downloads_music') if song['id'] in i]
    await query.answer('Скоро пришлем трек')
    filename = filename_find[0]
    return filename


#  функция, которая берет имя пользователя, название песни и дату когда пользователь запросил песню, и записывает в БД
def insert_music_data_in_db(query, song):
    users_id = query.from_user.id
    music_name = song['title']
    download_date = datetime.datetime.today()

    sql_insert(users_id, music_name, download_date)

    # создаем csv файл (записываем данные для столбцов) --> для дальнейшей работы в pandas
    with open("data.csv", mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow([f"{users_id}, {music_name}, {download_date}"])


#  функция возвращает данные песни которую выбрал пользователь на клавиатуре (имя, время, ссылку и тд...)
def get_data_song_by_query(query):
    data = query.data
    # метод достаёт всю информацию о 1-ом видео с YouTube (по ID песни)
    videosSearch_on_id = VideosSearch(data, limit=1)
    song = videosSearch_on_id.resultComponents[0]
    return song


#  получаем путь к запрошенной аудиозаписи перед отправкой пользователю
async def get_audio_file_by_query(query):
    song = get_data_song_by_query(query)
    filename = await get_filename_song(query, song)  # определяем переменную filename
    insert_music_data_in_db(query, song)

    # открытие файла типа open(), и InputFile запихивает указатель на этот файл (указываем путь к файлу)
    audio_file = aiogram.types.input_file.InputFile(
        rf'C:\Users\Admin\PycharmProjects\MusicTelegramBot\downloads_music\{filename}'
    )

    logging.info(f'SEND_AUDIO {query.from_user.id}, {audio_file}', exc_info=1)
    return audio_file
