import sqlite3
from sqlite3 import Error
from initialize_db import read_params, CWD

config = read_params()
DB = CWD + config["DB"]["sqlite3"]


def get_all():
    conn = None
    result_pass = None
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        query = f"SELECT unit_id, status FROM product"
        cur.execute(query)
        result = cur.fetchall()
        return result
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    print(result_pass)


def get_good():
    conn = None
    result_pass = None
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        query = f"SELECT unit_id, status FROM product WHERE status = 'Good'"
        cur.execute(query)
        result = cur.fetchall()
        return result
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    print(result_pass)


def get_bad():
    conn = None
    result_pass = None
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        query = f"SELECT unit_id, status FROM product WHERE status = 'Bad'"
        cur.execute(query)
        result = cur.fetchall()
        return result
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    print(result_pass)


def fetch_last():
    conn = None
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        query = f"SELECT MAX(unit_id) FROM product"
        cur.execute(query)
        result = cur.fetchone()
        return result[0]
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def update_status(status):
    conn = None
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        query = f'INSERT INTO product(status) VALUES ("{status}")'
        cur.execute(query)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print(fetch_last())
    print(get_all())
