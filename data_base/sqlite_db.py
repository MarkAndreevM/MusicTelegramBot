import sqlite3

# =========================================== Создаем БД ===============================================


def sql_start(users_name, music_name, download_date):
    base = sqlite3.connect('users_who_have_downloaded_music.db')

    if base:
        print('Data base connected OK!')
    else:
        raise Exception('Ошибка подключения к базе данных')

    cur = base.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users_download_music (users_name TEXT, music_name TEXT, download_date TEXT)")
    cur.execute("INSERT INTO users_download_music VALUES (?,?,?)", (users_name, str(music_name), str(download_date)))
    base.commit()
    base.close()


