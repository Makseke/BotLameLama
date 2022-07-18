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

def add_user( userid, time_on_server, server_name, user_name):
    try:
        con =psycopg2.connect(
            database=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host']
        )
        with con.cursor() as cur:
            cur.execute(f"SELECT * from users_list where userid = '{userid}'")
            user_id = cur.fetchall()
            print(user_id)
            if len(user_id) == 1:
                pass
            elif len(user_id) > 1:
                pass
            else:
                cur.execute(f"SELECT MAX (id) from users_list")
                max_ = cur.fetchall()
                new_id = max_[0][0] + 1
                user_info = f""" INSERT INTO users_list (id, userid, timeonserver, servername, messages) VALUES ({new_id}, {userid}, {time_on_server}, {server_name}, 1)"""
                cur.execute(user_info)
                con.commit()
                print(f"NEW USER IN DATA BASE {user_name}")
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