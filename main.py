from aiogram.utils import executor
from create_bot import dp


# ========================================= Запуск Бота ===========================================

if __name__ == "__main__":
    from aiogram_logic.client import send_to_myself
    executor.start_polling(dp, on_startup=send_to_myself)
