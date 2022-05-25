import sqlite3 as sq

# =========================================== БД ===============================================

database_path = 'database.db'


def sql_start():

    with sq.connect(database_path) as connection:
        cur = connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users_download_music ("
                    "users_id INT, "
                    "music_name TEXT, "
                    "download_date TEXT "
                    ")")


def sql_insert(users_id, music_name, download_date):

    with sq.connect(database_path) as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO users_download_music VALUES (?,?,?)", (users_id, str(music_name), str(download_date)))
