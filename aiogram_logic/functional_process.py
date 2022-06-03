import datetime
import logging
import os

import aiogram

from config_tg.config import admin_id
from music.music_script_download import download
from data_base.sqlite_db import sql_start, sql_insert

import csv
# ======================== Проверка работоспособности (проверка токена) =========================================


async def send_to_myself(dp):
    sql_start()
    await dp.bot.send_message(chat_id=admin_id, text='Бот запущен')

    # создаем csv файл (записываем названия столбцов)
    with open("data.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["users_id", "music_name", "download_date"])

    print('Бот вышел в чат')


# Определяем функцию, которая ищет(по ID)/скачивает композицию и возвращает нам имя скаченного/найденного файла.
async def get_filename_song(query):

    # создаем список, если id песни есть в папке (downloads_music) или пустой список - если такого id нет
    filename_find = [i for i in os.listdir('downloads_music') if query.data in i]
    if not filename_find:
        await query.answer('Прошу немного подождать, идёт загрузка трека')
        # функция, при помощи которой мы скачиваем видео из YouTube и переводим в Mp3 формат
        download(query.data.strip())

        filename_find = [i for i in os.listdir('downloads_music') if query.data in i]
    await query.answer('Скоро пришлем трек')
    filename = filename_find[0]
    return filename


#  функция, которая берет имя пользователя, ID песни и дату когда пользователь запросил песню, и записывает в БД
def insert_music_data_in_db(query):
    users_id = query.from_user.id
    music_name = query.data
    download_date = datetime.datetime.today()

    sql_insert(users_id, music_name, download_date)

    # создаем csv файл (записываем данные)
    with open("data.csv", mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow([f"{users_id}, {music_name}, {download_date}"])


#  получаем путь к запрошенной аудиозаписи перед отправкой пользователю
async def get_audio_file_by_query(query):
    filename = await get_filename_song(query)  # определяем переменную filename
    insert_music_data_in_db(query)

    # открытие файла типа open(), и InputFile запихивает указатель на этот файл (указываем путь к файлу)
    audio_file = aiogram.types.input_file.InputFile(f'./downloads_music/{filename}')

    logging.info(f'SEND_AUDIO {query.from_user.id}, {audio_file}', exc_info=1)
    return audio_file
