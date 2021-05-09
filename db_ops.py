import configparser
import datetime
import sqlite3

db = 'CalangoHC'

def select(table, col, arg):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''SELECT * FROM {} WHERE
       {} ="{}"''').format(table, col, arg)
    cursor.execute(aux)
    data = cursor.fetchone()
    conn.close()
    return data

def selectall(table, col, arg, order=''):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''SELECT * FROM {} WHERE
       {} ="{}" {}''').format(table, col, arg, order)
    cursor.execute(aux)
    data = cursor.fetchall()
    conn.close()
    return data

def selectbigger(table, col, arg, order=''):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''SELECT * FROM {} WHERE
       {} >"{}" {}''').format(table, col, arg, order)
    cursor.execute(aux)
    data = cursor.fetchall()
    conn.close()
    return data

def add(table, photo, post):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''INSERT INTO {} (post, photo, desc, days, newp)
        VALUES ('{}', '{}', '{}', '{}', '{}')''').format(table, post, photo, None, 7, 0)
    cursor.execute(aux)
    conn.commit()
    conn.close()

def delete(table, arg, arg_value):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''DELETE FROM {}
        WHERE {} = "{}"''').format(table, arg, str(arg_value))
    cursor.execute(aux)
    conn.commit()
    conn.close()

def update(table, arg, arg_value, arg_select, arg_select_value):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''UPDATE {} SET {} = "{}"
            WHERE {} = "{}"''').format(table, arg, str(arg_value), arg_select, str(arg_select_value))
    cursor.execute(aux)
    conn.commit()
    conn.close()
