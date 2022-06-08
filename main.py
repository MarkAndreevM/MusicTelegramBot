from aiogram.utils import executor
from create_bot import dp

# import logging
# logging.basicConfig(filename='log.log',
#     encoding='utf-8',
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(name)s\t| %(message)s',
#     datefmt='%Y-%m-%d %I:%M:%S %p'
# )


# ========================================= Запуск Бота ===========================================

if __name__ == "__main__":
    from aiogram_logic.functional_process import send_to_myself
    executor.start_polling(dp, on_startup=send_to_myself)
