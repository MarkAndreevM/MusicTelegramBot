from aiogram import types
from aiogram_logic.functional_process import get_audio_file_by_query
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from youtubesearchpython import VideosSearch
from music.music_script_download import long_time

from create_bot import bot, dp

from math import ceil

import json
# ======================== Отлавливаем команду(сообщение = start) --> отвечаем приветствием =====================


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет, я музыкальный бот!\n"
                         "Чтобы найти аудиозапись, отправь мне название песни и исполнителя!")


# =========== Обрабатываем запрос (сообщение пользователя) НАЗВАНИЕ ПЕСНИ / ИСПОЛНИТЕЛЯ ========================

# Создаём глобальную переменную (словарь, где ключ - ID пользователя, а значение - список песен по запросу)
global_dict_list_music_on_request = {}


@dp.message_handler()
#  Функция, возвращающая список найденных песен по запросу
async def user_song_request(message: types.Message):
    global global_dict_list_music_on_request

    song_title = '+'.join(message.text.split())  # если название песни состоит из 2 и более слов
    # метод VideosSearch достаёт всю информацию о limit=количестве видео (по запросу-названию)
    search_result = VideosSearch(song_title, limit=150)
    # вытаскиваем время песни, название, и ID, чтобы собрать клавиатуру (limit = ?)
    songs = [(f"{i['duration']} | {i['title']} ", f" {i['id']}") for i in search_result.resultComponents if i['duration']]

    # ============================= ИНЛАЙНКЛАВИАТУРА ДЛЯ ТРЕКОВ В ТЕЛЕГРАМ ========================================
    new_songs_list = []
    # пересоздаем список с допустимой продолжительностью треков
    for i in songs:
        if long_time(i[0]) <= 1200:
            new_songs_list.append(i)

    if len(new_songs_list) == 0:
        await message.answer('По данному запросу ничего не нашлось. Попробуйте ещё раз!')
    else:
        # Записываю в словарь новый ключ и значение
        global_dict_list_music_on_request[message.from_user.id] = new_songs_list

        # компонуем клавиатуру используя цикл for, где i[0] это duration и title, i[1] - ID выбранной песни
        count = 0
        keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        number_songs_page = ceil(len(new_songs_list) / 5)  # количество страниц в клавиатуре (в одной странице до 5 песен)

        for i in new_songs_list[count*5:(count+1)*5]:
            keyboard.row(InlineKeyboardButton(i[0], callback_data=i[1]))
        keyboard.add(InlineKeyboardButton('<', callback_data=f'<,{count},{message.text}'))
        keyboard.insert(InlineKeyboardButton(f'1/{number_songs_page}', callback_data='='))
        keyboard.insert(InlineKeyboardButton('>', callback_data=f'>,{count + 1},{message.text}'))

        await message.answer(f'{message.text}', reply_markup=keyboard)


@dp.callback_query_handler()
# Функция отвечает пользователю на запрос --> отправляет выбранную композицию (в аргументе - значение callback_data)
async def send_audio_by_query(query):

    global global_dict_list_music_on_request

    new_songs_list = global_dict_list_music_on_request[query.from_user.id]

    if '>' in query.data:  # Запрос со стрелочкой > содержит номер страницы. Пример '>,3'
        count_next = int(query.data.split(',')[1])
        if count_next == ceil(len(new_songs_list) / 5):
            pass
        else:
            await query.message.edit_text(f"{query.data.split(',')[2]}", reply_markup=next_keyboard(new_songs_list=new_songs_list, count=count_next, query=query))

    elif '<' in query.data:
        count_back = int(query.data.split(',')[1])
        if count_back == -1:
            pass
        else:
            await query.message.edit_text(f"{query.data.split(',')[2]}", reply_markup=back_keyboard(new_songs_list=new_songs_list, count=count_back, query=query))

    elif '=' in query.data:
        pass

    else:
        audio_file = await get_audio_file_by_query(query)
        await query.bot.send_audio(query.from_user.id, audio_file)


# Отлавливаем нажатие на кнопку '>'
@dp.callback_query_handler()
# Пересобираю клавиатуру после нажатия на '>'
def next_keyboard(new_songs_list, count, query):

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    number_songs_page = ceil(len(new_songs_list) / 5)  # количество страниц в клавиатуре (в одной странице до 5 песен)

    for i in new_songs_list[int(count) * 5:(int(count) + 1) * 5]:
        keyboard.row(InlineKeyboardButton(i[0], callback_data=i[1]))
    keyboard.add(InlineKeyboardButton('<', callback_data=f"<,{count - 1},{query.data.split(',')[2]}"))
    keyboard.insert(InlineKeyboardButton(f'{int(count)+1}/{number_songs_page}', callback_data='='))
    keyboard.insert(InlineKeyboardButton('>', callback_data=f">,{count + 1},{query.data.split(',')[2]}"))

    return keyboard


# Отлавливаем нажатие на кнопку '<'
@dp.callback_query_handler()
# Пересобираю клавиатуру после нажатия на '<'
def back_keyboard(new_songs_list, count, query):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    number_songs_page = ceil(len(new_songs_list) / 5)  # количество страниц в клавиатуре (в одной странице до 5 песен)

    for i in new_songs_list[int(count) * 5:(int(count) + 1) * 5]:
        keyboard.row(InlineKeyboardButton(i[0], callback_data=i[1]))
    keyboard.add(InlineKeyboardButton('<', callback_data=f"<,{count - 1},{query.data.split(',')[2]}"))
    keyboard.insert(InlineKeyboardButton(f'{int(count) + 1}/{number_songs_page}', callback_data='='))
    keyboard.insert(InlineKeyboardButton('>', callback_data=f">,{count + 1},{query.data.split(',')[2]}"))

    return keyboard
