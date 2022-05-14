import aiogram
from create_bot import bot, dp
from aiogram import types, Dispatcher
from config_tg.config import admin_id
from youtubesearchpython import VideosSearch  # модуль для парсинга (вытягивания отдельных ссылок с запросов на Youtube)
import os

# ======================== Проверка работоспособности (проверка токена) =========================================

from music.music_script_download import download  # импортируем функцию download, для скачивания музыки

async def send_to_myself(dp):
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
    videosSearch = VideosSearch(song_title, limit=5)  # метод достаёт всю информацию о 1-ом видео (по запросу-названию)
    songs = list(map(lambda x: [x['duration'] + '|' + ' ' + x['title'],  x['id']], videosSearch.resultComponents))  # вытаскиваем ссылку на видео (limit = ?)

    # ============================= КЛАВИАТУРА ДЛЯ ТРЕКОВ ========================================

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    # КНОПКИ ДЛЯ КАЛЬКУЛЯТОРА

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for i in songs:
        keyboard.row(InlineKeyboardButton(i[0], callback_data=i[1]))
    await message.answer('Выберите название трека', reply_markup=keyboard)
    # name_song = list(map(lambda x: x['title'] + ' ' + x['duration'] + '\n', videosSearch.resultComponents))   # соберет все названия limit = ?
    # name_song = ''.join(name_song)
    # await message.answer(name_song)


    @dp.callback_query_handler()
    async def callback_func(query):

        query = videosSearch.resultComponents[0]
        filename = f"{query['title']} [{query['id']}].mp3"  # компонуем название композиции, чтобы оно совпадало со скаченным названием композиции
        filename = filename.replace('/', "_")  # Это говно нужно добавить из-за ошибки youtube_DL. Он заменяет любые кавычки на одинарные ('')

        try:
            if filename not in os.listdir():
                await message.answer('Прошу немного подождать, идёт загрузка трека')
                download(songs)  # функция, при помощи которой мы скачиваем музыку из YouTube и переводим в Mp3 формат

            file_audio_send = aiogram.types.input_file.InputFile(filename)  # открытие файла типа open(), и InputFile запихивает указатель на этот файл ?
            await message.answer('Скоро пришлём трек!')
            await bot.send_audio(message.from_user.id, file_audio_send)  # отправляем композицию пользователю, в ответ на его запрос

        except:
            await message.answer('Произошла непредвиденная ошибка, попробуйте ввести другое название')





