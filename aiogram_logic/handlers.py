from aiogram import types
from aiogram_logic.functional_process import get_audio_file_by_query
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from youtubesearchpython import VideosSearch
from music.music_script_download import long_time

from create_bot import bot, dp


# ======================== Отлавливаем команду(сообщение = start) --> отвечаем приветствием =====================

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет, я музыкальный бот!\n"
                         "Чтобы найти аудиозапись, отправь мне название песни и исполнителя!")


# =========== Обрабатываем запрос (сообщение пользователя) НАЗВАНИЕ ПЕСНИ / ИСПОЛНИТЕЛЯ ========================

@dp.message_handler()
async def user_song_request(message: types.Message):
    song_title = message.text  # определяем переменную и записываем в неё название песни, которую прислал пользователь
    song_title = '+'.join(song_title.split())  # если название песни состоит из 2 и более слов
    # метод VideosSearch достаёт всю информацию о limit=количестве видео (по запросу-названию)
    search_result = VideosSearch(song_title, limit=10)

    # вытаскиваем время песни, название, и ID, чтобы собрать клавиатуру (limit = ?)
    songs = (f"{i['duration']} | {i['title']} ~ {i['id']}" for i in search_result.resultComponents if i['duration'])

    # ============================= ИНОЛАЙНКЛАВИАТУРА ДЛЯ ТРЕКОВ В ТЕЛЕГРАМ ========================================

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # компонуем клавиатуру используя цикл for, где i[0] это duration и title, i[1] - ID выбранной песни
    for i in songs:
        i = i.split('~')
        if long_time(i[0]) <= 420:
            keyboard.row(InlineKeyboardButton(i[0], callback_data=i[1]))
    await message.answer('Выберите название трека', reply_markup=keyboard)


@dp.callback_query_handler()
async def send_audio_by_query(query):
    # Функция отвечает пользователю на запрос --> отправляет выбранную композицию (в аргументе - значение callback_data)
    audio_file = await get_audio_file_by_query(query)
    await query.bot.send_audio(query.from_user.id, audio_file)

