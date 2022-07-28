import psycopg2
from psycopg2 import Error

from config import config

# Выводит инфомрацию о работе базы данных
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
            with open('LOG.txt', 'a', encoding="utf-8") as file:
                file.write(f'--------------------------------------------------\nDATA BASE ONLINE\nSERVER VERSION: {cur.fetchone()}\n')
    except (Exception, Error) as error:
        print("ERROR IN POSTGRESQL", error)
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'ERROR IN POSTGRESQL {error}\n')
    finally:
        if con:
            cur.close()
            con.close()

# Добавляет пользователя в базу данных
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
                    with open('LOG.txt', 'a', encoding="utf-8") as file:
                        file.write(f"ADD USER IN DATA BASE {user_name}\n")
            else:
                cur.execute(f"SELECT MAX (id) from users_list")
                max_ = cur.fetchall()
                new_id = max_[0][0] + 1
                user_info = f""" INSERT INTO users_list (id, userid, timeonserver, servername, messages) VALUES ({new_id}, {userid}, {time_on_server}, {server_name}, 1)"""
                cur.execute(user_info)
                con.commit()
                print(f"NEW USER IN DATA BASE {user_name}")
                with open('LOG.txt', 'a', encoding="utf-8") as file:
                    file.write(f"NEW USER IN DATA BASE {user_name}\n")
    except (Exception, Error) as error:
        print("ERROR IN POSTGRESQL", error)
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f"ERROR IN POSTGRESQL {error}\n")
        error_finder = 1
        return error_finder
    finally:
        error_finder = 0
        if con:
            cur.close()
            con.close()
        return error_finder

# Добавляет единицу к количеству сообщений пользователя
def add_message_to_user(userid, guildid):
    try:
        messages = 0
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
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f"ERROR ID ADDING MESSAGE TO USERS_LIST: {error}\n")
    finally:
        if con:
            cur.close()
            con.close()
        return messages

# Добавляет время проведенное в голосовых каналах пользователю
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
        print("ERROR ID ADDING TIME TO USERS_LIST: ", error)
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f"ERROR ID ADDING TIME TO USERS_LIST: {error}\n")
    finally:
        if con:
            cur.close()
            con.close()
            return addtime

def get_info(userid, guildid):
    try:
        con = psycopg2.connect(
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
                    main_info = i
    except (Exception, Error) as error:
        print("ERROR ID GET_INFO_USER IN USERS_LIST: ", error)
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f"ERROR ID GET_INFO_USER IN USERS_LIST: {error}\n")
    finally:
        if con:
            cur.close()
            con.close()
            return main_info