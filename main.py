from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db


# ================================== ПРОВЕРКА ВЫХОДА БОТА В РЕЖИМ ON ===============================

    # sqlite_db.sql_start()



# ========================================= Запуск Бота ===========================================

if __name__ == "__main__":
    from handlers.client import send_to_myself
    executor.start_polling(dp, on_startup=send_to_myself)
