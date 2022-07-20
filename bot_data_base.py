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

def add_user(userid, time_on_server, server_name, user_name):
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
            if len(user_id) >= 1:
                user_guild_list = []
                for i in user_id:
                    user_guild_list.append(str(i[3]))
                if str(server_name) not in user_guild_list:
                    cur.execute(f"SELECT MAX (id) from users_list")
                    max_ = cur.fetchall()
                    new_id = max_[0][0] + 1
                    user_info = f""" INSERT INTO users_list (id, userid, timeonserver, servername, messages) VALUES ({new_id}, {userid}, {time_on_server}, {server_name}, 1)"""
                    cur.execute(user_info)
                    con.commit()
                    print(f"ADD USER IN DATA BASE {user_name}")
            else:
                cur.execute(f"SELECT MAX (id) from users_list")
                max_ = cur.fetchall()
                new_id = max_[0][0] + 1
                user_info = f""" INSERT INTO users_list (id, userid, timeonserver, servername, messages) VALUES ({new_id}, {userid}, {time_on_server}, {server_name}, 1)"""
                cur.execute(user_info)
                con.commit()
                print(f"NEW USER IN DATA BASE {user_name}")
    except (Exception, Error) as error:
        print("ERROR IN POSTGRESQL", error)
        error_finder = 1
        return error_finder
    finally:
        error_finder = 0
        if con:
            cur.close()
            con.close()
        return error_finder

def add_message_to_user(userid, guildid):
    try:
        con =psycopg2.connect(
            database=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host']
        )
        with con.cursor() as cur:
            cur.execute(f"SELECT * from users_list where userid = '{userid}'")
            users = cur.fetchall()
            for i in users:
                if str(i[3]) == str(guildid):
                    id = i[0]
                    messages = i[4] + 1
            update_message_count = f"""Update users_list set messages = {messages} where id = {id}"""
            cur.execute(update_message_count)
            con.commit()
    except (Exception, Error) as error:
        print("ERROR ID ADDING MESSAGE TO USERS_LIST: ", error)
        error_finder = 1
        return error_finder
    finally:
        error_finder = 0
        if con:
            cur.close()
            con.close()
        return error_finder

def add_time_to_user(userid, guildid, timeinvoise_minutes):
    try:
        con =psycopg2.connect(
            database=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host']
        )
        with con.cursor() as cur:
            cur.execute(f"SELECT * from users_list where userid = '{userid}'")
            users = cur.fetchall()
            for i in users:
                if str(i[3]) == str(guildid):
                    id = i[0]
                    addtime = int(i[2]) + timeinvoise_minutes
            update_message_count = f"""Update users_list set timeonserver = {addtime} where id = {id}"""
            cur.execute(update_message_count)
            con.commit()
    except (Exception, Error) as error:
        print("ERROR ID ADDING MESSAGE TO USERS_LIST: ", error)
        error_finder = 1
        return error_finder
    finally:
        error_finder = 0
        if con:
            cur.close()
            con.close()
        return error_finder