from aiogram.utils import executor
from create_bot import dp

import os

# import logging
# logging.basicConfig(filename='log.log',
#     encoding='utf-8',
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(name)s\t| %(message)s',
#     datefmt='%Y-%m-%d %I:%M:%S %p'
# )

name_path_music_downloads = 'downloads_music'


# Функция создает папку, куда будет скачиваться вся музыка
def music_download_makedir():
    if not os.path.isdir(name_path_music_downloads):
        os.mkdir(name_path_music_downloads)


# ========================================= Запуск Бота ===========================================


if __name__ == "__main__":
    from aiogram_logic.functional_process import send_to_myself
    music_download_makedir()
    executor.start_polling(dp, on_startup=send_to_myself)
