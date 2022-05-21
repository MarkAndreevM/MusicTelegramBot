from create_bot import bot, dp
from aiogram import types, Dispatcher
from youtubesearchpython import VideosSearch, VideoDurationFilter, CustomSearch
from aiogram_logic.client import the_path_to_the_song
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from music.music_script_download import len_time  # говнофункция (временная), чтобы треки были длинной до 10 минут


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
    videosSearch_on_song_title = VideosSearch(song_title, limit=10)

    # вытаскиваем время песни, название, и ID, чтобы собрать клавиатуру (limit = ?)
    songs = list(map(lambda x: [x['duration'] + '|' + ' ' + x['title'], x['id']],
                     videosSearch_on_song_title.resultComponents))

    # ============================= ИНОЛАЙНКЛАВИАТУРА ДЛЯ ТРЕКОВ В ТЕЛЕГРАМ ========================================

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    #  компонуем клавиатуру используя цикл for, где i[0] это duration и title, i[1] - ID выбранной песни
    for i in songs:
        if len_time(i[0]) > 3:
            pass
        else:
            keyboard.row(InlineKeyboardButton(i[0], callback_data=i[1]))
    await message.answer('Выберите название трека', reply_markup=keyboard)


#  отлавливаем нажатие пользователя на инлайнкнопку --> возвращается ID трека
@dp.callback_query_handler()
async def callback_func(query):
    file_audio_send = await the_path_to_the_song(query)
    await bot.send_audio(query.from_user.id, file_audio_send)
