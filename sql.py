import sqlite3 as sl
from datetime import datetime

DATABASE_PATH = 'db/database.db'
date = datetime.now()


def create_track(track_number: str, user_id: int, row_count: int, description: str):
    """ Создает запись о номере трека и пользователе в таблице TRACKS """

    con = sl.connect(DATABASE_PATH)
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO TRACKS(track_num, user_id, row_count, description, date) VALUES(?, ?, ?, ?, ?);",
                       (track_number, user_id, row_count, description, date))
    except sl.DatabaseError as err:
        print("Error: ", err)
    else:
        con.commit()
    finally:
        cursor.close()
        con.close()


def read_track_num(track_number: str, user_id: int) -> str:
    """ Читает номер трека из таблицы TRACKS """

    track_num = ''
    con = sl.connect(DATABASE_PATH)
    cursor = con.cursor()
    try:
        cursor.execute("SELECT track_num FROM TRACKS WHERE track_num = :track_number AND user_id = :user_id;",
                       {"track_number": track_number, "user_id": user_id})
    except sl.DatabaseError as err:
        print("Error: ", err)
    else:
        con.commit()
        record = cursor.fetchall()
        for row in record:
            track_num = row[0]
    finally:
        cursor.close()
        con.close()
    return track_num


def read_track_id(track_number: str, user_id: int) -> int:
    """ Читает id трека из таблицы TRACKS """

    track_id = 0
    con = sl.connect(DATABASE_PATH)
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT id FROM TRACKS WHERE track_num = :track_number AND user_id = :user_id;""",
                       {"track_number": track_number, "user_id": user_id})
    except sl.DatabaseError as err:
        print("Error: ", err)
    else:
        con.commit()
        record = cursor.fetchall()
        for row in record:
            track_id = row[0]
    finally:
        cursor.close()
        con.close()
    return track_id


def read_track_row_count(track_number: str, user_id: int) -> int:
    """ Читает id трека из таблицы TRACKS """

    track_id = 0
    con = sl.connect(DATABASE_PATH)
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT row_count FROM TRACKS WHERE track_num = :track_number AND user_id = :user_id;""",
                       {"track_number": track_number, "user_id": user_id})
    except sl.DatabaseError as err:
        print("Error: ", err)
    else:
        con.commit()
        record = cursor.fetchall()
        for row in record:
            track_id = row[0]
    finally:
        cursor.close()
        con.close()
    return track_id


def read_all_user_tracks(user_id: int) -> list:
    """ Читает все треки пользователя """

    tracks = ''
    con = sl.connect(DATABASE_PATH)
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT track_num, description, date FROM TRACKS WHERE user_id = :userId;""",
                       {"userId": user_id})
    except sl.DatabaseError as err:
        print("Error: ", err)
    else:
        con.commit()
        records = cursor.fetchall()
        for row in records:
            tracks += row[0] + '\n'
    finally:
        cursor.close()
        con.close()
    return records


def delete_track(track_number, user_id):
    """ Удаляет трек пользователя """

    con = sl.connect(DATABASE_PATH)
    cursor = con.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("""DELETE FROM TRACKS WHERE track_num = :trackNumber AND user_id = :user_id;""",
                       {"trackNumber": track_number, "user_id": user_id})
    except sl.DatabaseError as err:
        print("Error: ", err)
    else:
        con.commit()
    finally:
        cursor.close()
        con.close()
