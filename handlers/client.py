import aiogram
from create_bot import bot, dp
from aiogram import types, Dispatcher
from config_tg.config import admin_id
# модуль для парсинга (вытягивания отдельных ссылок с запросов на Youtube)
from youtubesearchpython import VideosSearch, VideoDurationFilter, CustomSearch
# todo: youtubesearchpython.__future__
import os, sys

# Импортируем модуль datetime (определяем переменные для записи в БД)
import datetime
from data_base.sqlite_db import sql_start, sql_insert

# import logging
# logging.basicConfig(
#     handlers=[
#         logging.FileHandler("debug.log"),
#         logging.StreamHandler(sys.stdout)
#     ],
#     encoding='utf-8',
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(name)s\t| %(message)sm',
#     datefmt='%Y-%m-%d %I:%M:%S %p'
# )

# ======================== Проверка работоспособности (проверка токена) =========================================

from music.music_script_download import download  # импортируем функцию download, для скачивания музыки


async def send_to_myself(dp):
    sql_start()
    await bot.send_message(chat_id=admin_id, text='Бот запущен')
    print('Бот вышел в чат')


# ======================== Отлавливаем команду(сообщение = start) --> отвечаем приветствием =====================

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет, я музыкальный бот!\n"
                         "Чтобы найти аудиозапись, отправь мне название песни и исполнителя!")


# =========== Обрабатываем запрос (сообщение пользователя) НАЗВАНИЕ ПЕСНИ / ИСПОЛНИТЕЛЯ ========================

@dp.message_handler()
async def start_command(message: types.Message):
    song_title = message.text  # определяем переменную и записываем в неё название песни, которую прислал пользователь
    song_title = '+'.join(song_title.split())  # если название песни состоит из 2 и более слов
    # метод VideosSearch достаёт всю информацию о limit=количестве видео (по запросу-названию)
    videosSearch_on_song_title = VideosSearch(song_title, limit=10)

    # достаем всю информацию по 7 видео (по фильтру - с коротким времени воспроизведения)
    # videosSearch_on_song_title = CustomSearch(song_title, VideoDurationFilter.short, limit=7)

    songs = list(map(lambda x: [x['duration'] + '|' + ' ' + x['title'], x['id']], videosSearch_on_song_title.resultComponents))  # вытаскиваем время песни, название, размер и ID, чтобы собрать клавиатуру (limit = ?)
    # ============================= ИНОЛАЙНКЛАВИАТУРА ДЛЯ ТРЕКОВ В ТЕЛЕГРАМ ========================================

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from music.music_script_download import len_time  # говнофункция (временная), чтобы треки были длинной до 10 минут

    # ======================================= КНОПКИ КЛАВИАТУРЫ ===================================================

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    #  компонуем клавиатуру используя цикл for
    for i in songs:
        if len_time(i[0]) > 3:
            pass
        else:
            keyboard.row(InlineKeyboardButton(i[0], callback_data=i[1]))
    await message.answer('Выберите название трека', reply_markup=keyboard)


# Определяем функцию, которая возвращает нам имя скаченного файла
async def get_filename(query, song):
    """
    Определяем функцию, которая возвращает нам имя скаченного файла
    :param query:
    :param song:
    :return:
    """
    # создаем список, если id песни есть в директории или пустой список - если такого id нет
    filename_find = [i for i in os.listdir('downloads_music') if song['id'] in i]
    if not filename_find:
        await query.answer('Прошу немного подождать, идёт загрузка трека')
        # функция, при помощи которой мы скачиваем видео из YouTube и переводим в Mp3 формат
        download(song['id'], query)

        filename_find = [i for i in os.listdir('downloads_music') if song['id'] in i]
    await query.answer('Скоро пришлем трек')
    filename = filename_find[0]
    return filename


#  функция, которая берет имя пользователя, название песни и сегодняшнюю дату и записывает в БД
def insert_music_data_in_db(query, song):
    users_name = query.from_user.first_name
    music_name = song['title']
    download_date = datetime.datetime.today()

    sql_insert(users_name, music_name, download_date)


#  функция возвращает данные песни (имя, время, ссылку и тд...), которую выбрал пользователь
def get_song(query):
    data = query.data
    # метод достаёт всю информацию о 1-ом видео (по ID (data) )
    videosSearch_on_id = VideosSearch(data, limit=1)
    song = videosSearch_on_id.resultComponents[0]
    return song


#  получаем путь к запрошенной аудиозаписи
async def get_file_audio(query):
    song = get_song(query)
    filename = await get_filename(query, song)  # определяем переменную filename
    insert_music_data_in_db(query, song)

    # try:
    # открытие файла типа open(), и InputFile запихивает указатель на этот файл (указываем путь к файлу)
    file_audio_send = aiogram.types.input_file.InputFile(rf'C:\Users\Admin\PycharmProjects\MusicTelegramBot\downloads_music\{filename}')
    # except:
    #     await query.answer('Произошла ошибка при загрузке трека')
    return file_audio_send


#  отлавливаем нажатие пользователя на инлайнкнопку --> возвращается ID трека
@dp.callback_query_handler()
async def callback_func(query):
    file_audio_send = await get_file_audio(query)
    await bot.send_audio(query.from_user.id, file_audio_send)

    # logging.info(f'SEND_AUDIO {query.from_user.id}, {file_audio_send}', exc_info=1)



