import sqlite3

# =========================================== Создаем БД ===============================================

database_path = 'users_who_have_downloaded_music.db'


def sql_start():
    connection = sqlite3.connect(database_path)

    if connection:
        print('Data connection connected OK!')
    else:
        raise Exception('Ошибка подключения к базе данных')

    cur = connection.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users_download_music (users_name TEXT, music_name TEXT, download_date TEXT)")
    connection.commit()
    connection.close()


def sql_insert(users_name, music_name, download_date):
    connection = sqlite3.connect(database_path)

    if connection:
        print('Data connection connected OK!')
    else:
        raise Exception('Ошибка подключения к базе данных')

    cur = connection.cursor()

    cur.execute("INSERT INTO users_download_music VALUES (?,?,?)", (users_name, str(music_name), str(download_date)))
    connection.commit()
    connection.close()


