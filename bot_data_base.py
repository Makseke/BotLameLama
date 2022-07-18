import psycopg2
from psycopg2 import Error

from config import config

def server_srart():
    global error_finder
    error_finder = 0
    try:
        con =psycopg2.connect(
            database=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host']
        )
        with con.cursor() as cur:
            cur.execute(
                'SELECT version();'
            )
            print('--------------------------------------------------')
            print('DATA BASE ONLINE')
            print(f'SERVER VERSION: {cur.fetchone()}')
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if con:
            cur.close()
            con.close()

def add_user( userid, time_on_server, server_name):
    try:
        con =psycopg2.connect(
            database=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host']
        )
        with con.cursor() as cur:
            cur.execute("SELECT userid from users_list")
            user_id = cur.fetchall()
            print(user_id)
            for i in user_id:
                if str(i[0]) == str(userid):
                    print('FIND')
                else:
                    print('ERROR')
            user_info = f""" INSERT INTO users_list (id, userid, timeonserver, servername) VALUES ({id}, {userid}, {time_on_server}, {server_name})"""
            cur.execute(user_info)
            con.commit()
            print("1 запись успешно вставлена")
            cur.execute("SELECT * from users_list")
            record = cur.fetchall()
            print("Результат", record)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        error_finder = 1
        return error_finder
    finally:
        error_finder = 0
        return error_finder
        if con:
            cur.close()
            con.close()