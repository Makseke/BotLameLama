from config import config
import bot_data_base

import discord
from discord.commands import Option
from discord.ext import commands

from random import randint

import datetime

import time

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(
    intents=intents
)

# Выводит время в формате часы:минуты:секунды
def time_now():
    dt = datetime.datetime.now()
    dt_string = dt.strftime("DATE: %d/%m/%Y  TIME: %H:%M:%S")
    return dt_string

# Переводит секунду в  формат часы:минуты:секунды
def sec_to_time(sec):
    sec = int(sec)
    hour = 0
    min = 0
    while sec >= 60:
        sec -= 60
        min += 1
        if min >= 60:
            min -= 60
            hour += 1
    if min == 0 and hour == 0:
        final_sec_to_time = f'{sec} SEC'
        return final_sec_to_time
    elif min != 0 and hour == 0:
        if sec < 10:
            sec = '0' + str(sec)
        final_sec_to_time = f'{min}:{sec} MIN'
        return final_sec_to_time
    else:
        if min < 10:
            min = '0' + str(min)
        if sec < 10:
            sec = '0' + str(sec)
        final_sec_to_time = f'{hour}:{min}:{sec} HOUR'
        return final_sec_to_time

def role_time(time_for_role, member):
    if time_for_role >= 2400:
        for i in member.guild.roles:
            if i.name == 'Любимчик администрации':
                role = i
        return role
    elif time_for_role >= 1800:
        for i in member.guild.roles:
            if i.name == 'Любимчик бармена':
                role = i
        return role
    elif time_for_role >= 1200:
        for i in member.guild.roles:
            if i.name == 'Завсегдатай':
                role = i
        return role
    elif time_for_role >= 600:
        for i in member.guild.roles:
            if i.name == 'Посетитель':
                role = i
        return role
    elif time_for_role >= 1:
        for i in member.guild.roles:
            if i.name == 'Проходимец':
                role = i
        return role
    else:
        return 0

print(f'--------------------------------------------------\nSERVER ONLINE\n{time_now()}')
with open('LOG.txt', 'a', encoding="utf-8") as file:
    file.write(f'\n\n\n--------------------------------------------------\nSERVER ONLINE\n{time_now()}\n')
bot_data_base.server_srart()

global tdict
global tdict_user_disconnect
tdict = {}
tdict_user_disconnect = {}
global time_start
time_start = time.time()

# Выводит список серверов использующих бота
@bot.event
async def on_ready():
    print(f'--------------------------------------------------\nINFO AT {time_now()}')
    for guilds in bot.guilds:
        print(f'{guilds} SERVER WITH {guilds.member_count} USERS USING LAMELAMA')
    print('--------------------------------------------------')
    print(f"BOT ONLINE\n{len(bot.guilds)} SERVERS USING LAMELAMA")
    print('--------------------------------------------------')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'--------------------------------------------------\nINFO AT {time_now()}\n--------------------------------------------------\n')
        for guilds in bot.guilds:
            file.write(f'{guilds} SERVER WITH {guilds.member_count} USERS USING LAMELAMA\n')
        file.write(f'--------------------------------------------------\nBOT ONLINE\n{len(bot.guilds)} SERVERS USING LAMELAMA\n--------------------------------------------------\n')

# Добавлеят основные роли при добавлении на сервер
@bot.event
async def on_guild_join(guild):
    print(f'ADD_BOT_ROLES TO {guild.name}')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'ADD_BOT_ROLES TO {guild.name}\n')
    new_role_5 = await guild.create_role(name='Любимчик администрации', color=0xfcf7b5)
    new_role_4 = await guild.create_role(name='Любимчик бармена', color=0xfcffaf)
    new_role_3 = await guild.create_role(name='Завсегдатай', color=0xfcff82)
    new_role_2 = await guild.create_role(name='Посетитель', color=0xf4ec7f)
    new_role_1 = await guild.create_role(name='Проходимец', color=0xf2da71)

# Получает время проведенное пользователем в голосовых каналах
@bot.event
async def on_voice_state_update(member, before, after):
    if after.self_mute == True and after.channel.id != 835231201634680873:
        print(f'{member} MUTED AT {str(time_now()).split()[3]}')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'{member} MUTED AT {str(time_now()).split()[3]}\n')
    elif before.self_mute == True and after.self_mute == False:
        print(f'{member} UNMUTED AT {str(time_now()).split()[3]}')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'{member} UNMUTED AT {str(time_now()).split()[3]}\n')
    author = member.id
    if (before.channel is None and after.channel is not None) or (before.channel.id == 835231201634680873 and after.channel is not None):
        print(f'{member.name} JOIN TO {after.channel.name} AT {time_now()}')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'{member.name} JOIN TO {after.channel.name} AT {time_now()}\n')
        tdict[author] = time.time()
        tdict_user_disconnect[author] = None
    elif before.channel is not None and after.channel is None and author in tdict:
        print(sec_to_time(str(time.time()-tdict[author]).split('.')[0]), f'BY {member.name} AT {member.guild}')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            time_ = sec_to_time(str(time.time()-tdict[author]).split('.')[0])
            file.write(f'{time_} BY {member.name} AT {member.guild}\n')
        actual_time = int(int(str(time.time()-tdict[author]).split('.')[0])/60)
        time_user = bot_data_base.add_time_to_user(member.id, member.guild.id, actual_time)
        _ = role_time(time_user, member)
        tdict_user_disconnect[author] = time.time()
        if _ != 0:
            if _ in member.roles:
                pass
            else:
                print(f'LVL UP TO {_.name} BY {member.name}')
                with open('LOG.txt', 'a', encoding="utf-8") as file:
                    file.write(f'LVL UP TO {_.name} BY {member.name}\n')
            await member.add_roles(_)
    elif before.channel is not None and after.channel is None and author not in tdict:
        print(sec_to_time(str(time.time() - time_start).split('.')[0]), f'BY {member.name} AT {member.guild} AFTER SERVER RESTART')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            time_ = sec_to_time(str(time.time()-time_start).split('.')[0])
            file.write(f'{time_} BY {member.name} AT {member.guild} AFTER SERVER RESTART\n')
        actual_time = int(int(str(time.time() - time_start).split('.')[0]) / 60)
        time_user = bot_data_base.add_time_to_user(member.id, member.guild.id, actual_time)
        _ = role_time(time_user, member)
        tdict_user_disconnect[author] = time.time()
        if _ != 0:
            if _ in member.roles:
                pass
            else:
                print(f'LVL UP TO {_.name} BY {member.name}')
                with open('LOG.txt', 'a', encoding="utf-8") as file:
                    file.write(f'LVL UP TO {_.name} BY {member.name}\n')
            await member.add_roles(_)
    elif before.channel != after.channel and after.channel.id !=835231201634680873:
        print(f'{member.name} JOIN TO {after.channel.name} AT {time_now()}')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'{member.name} JOIN TO {after.channel.name} AT {time_now()}\n')
    if before.channel is not None and after.channel.id == 835231201634680873:
        print(f'{member.name} MOVED TO {after.channel.name} AT {time_now()} - REASON - AFK MORE THAN 5 MINUTES')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'{member.name} MOVED TO {after.channel.name} AT {time_now()} - REASON - AFK MORE THAN 5 MINUTES\n')
        if before.channel is not None and author in tdict:
            print(sec_to_time(str(time.time() - tdict[author]).split('.')[0]), f'BY {member.name} AT {member.guild}')
            with open('LOG.txt', 'a', encoding="utf-8") as file:
                time_ = sec_to_time(str(time.time() - tdict[author]).split('.')[0])
                file.write(f'{time_} BY {member.name} AT {member.guild}\n')
            actual_time = int(int(str(time.time() - tdict[author]).split('.')[0]) / 60)
            time_user = bot_data_base.add_time_to_user(member.id, member.guild.id, actual_time)
            _ = role_time(time_user, member)
            tdict_user_disconnect[author] = time.time()
            if _ != 0:
                if _ in member.roles:
                    pass
                else:
                    print(f'LVL UP TO {_.name} BY {member.name}')
                    with open('LOG.txt', 'a', encoding="utf-8") as file:
                        file.write(f'LVL UP TO {_.name} BY {member.name}\n')
                await member.add_roles(_)
        elif before.channel is not None and author not in tdict:
            print(sec_to_time(str(time.time() - time_start).split('.')[0]),f'BY {member.name} AT {member.guild} AFTER SERVER RESTART')
            with open('LOG.txt', 'a', encoding="utf-8") as file:
                time_ = sec_to_time(str(time.time() - time_start).split('.')[0])
                file.write(f'{time_} BY {member.name} AT {member.guild} AFTER SERVER RESTART\n')
            actual_time = int(int(str(time.time() - time_start).split('.')[0]) / 60)
            time_user = bot_data_base.add_time_to_user(member.id, member.guild.id, actual_time)
            _ = role_time(time_user, member)
            tdict_user_disconnect[author] = time.time()
            if _ != 0:
                if _ in member.roles:
                    pass
                else:
                    print(f'LVL UP TO {_.name} BY {member.name}')
                    with open('LOG.txt', 'a', encoding="utf-8") as file:
                        file.write(f'LVL UP TO {_.name} BY {member.name}\n')
                await member.add_roles(_)

# Добавляет пользователя в базу данных и выдает роль при подключении к серверу
@bot.event
async def on_member_join(member):
    print(f'ADD_TO_DATA_BASE WHEN MEMBER JOIN SERVER {member.name} / {member.guild} AT {time_now()}')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'ADD_TO_DATA_BASE WHEN MEMBER JOIN SERVER {member.name} / {member.guild} AT {time_now()}\n')
    error_finder = bot_data_base.add_user(member.id, 1, member.guild.id, member.name)
    role = ''
    for i in member.guild.roles:
        if i.name == 'Проходимец':
            role = i
    await member.add_roles(role)
    if error_finder == 0:
        print(f'USER {member.name} ADD TO DATABASE')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'USER {member.name} ADD TO DATABASE\n')
    else:
        print(f'ERROR IN ADDING {member.name} TO DATABASE')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'ERROR IN ADDING {member.name} TO DATABASE\n')

# Добавляет единицу к количетсву сообщений пользователя
@bot.event
async def on_message(message):
    if message.author.name != 'BotLameLama':
        bot_data_base.add_message_to_user(message.author.id, message.author.guild.id)

# Возвращает случайное число в введеном диапазоне
@bot.slash_command(description="Выдает случайное число в переданном диапазоне", name="random")
async def random(message, min: Option(int), max: Option(int)):
    print(f'RANDOM BY {message.author} / {message.guild} AT {time_now()}')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'RANDOM BY {message.author} / {message.guild} AT {time_now()}\n')
    if min > max:
        _ = min
        min = max
        max = _
    await message.respond(randint(min, max))

# Возвращает одно случайное слово из введеной строки
@bot.slash_command(description="Выдает случайное слово из введенной строки", name="random_word")
async def random_word(message, string: Option(str)):
    print(f'RANDOM_WORD BY {message.author} / {message.guild} AT {time_now()} ')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'RANDOM_WORD BY {message.author} / {message.guild} AT {time_now()}\n')
    string_list = string.split()
    if len(string_list) == 1:
        await message.respond(string_list[0])
    else:
        await message.respond(string_list[randint(0, len(string_list))])

# Выводит информацию о пользователе в виде карточки
@bot.slash_command(description='Выводит информацию о пользователе в виде карточки', name='info')
async def info(message, member: discord.User):
    if member.bot == False:
        print(f'GET INFO ABOUT {member.name} / {message.guild} BY {message.author} AT {time_now()}')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'GET INFO ABOUT {member.name} / {message.guild} BY {message.author} AT {time_now()}\n')
        dt_member = str(member.created_at).split('.')[0]
        embed = discord.Embed(
            title=f'Информация о пользователе {member.name}',
            description=f'Сервер {message.guild}',
            color=0xf2da71
        )
        embed.set_author(name=f'{message.author.display_name}', icon_url=f'{message.author.avatar}')
        embed.set_thumbnail(url=f'{member.avatar}')
        embed.add_field(name='Отображаемое имя', value=member.display_name, inline=True)
        embed.add_field(name='ID пользователя', value=member.id, inline=True)
        embed.add_field(name='Дата регистрации аккаунта', value=str(dt_member).split()[0], inline=False)
        addtime = 0
        try:
            if tdict[member.id] != None and tdict_user_disconnect[member.id] == None:
                addtime = int(str(time.time() - tdict[member.id]).split('.')[0])
        except:
            pass
        embed.add_field(name='Время в голосовых каналах', value=str(sec_to_time(int(bot_data_base.get_info(member.id, member.guild.id)[2]) * 60 + addtime)).split()[0], inline=True)
        embed.add_field(name='Отправлено сообщений', value=bot_data_base.get_info(member.id, member.guild.id)[4], inline=True)
        embed.set_footer(text=f'Информация актульна на {str(time_now()).split()[1]} {str(time_now()).split()[3]}')
        await message.respond(embed=embed)
    else:
        print(f'TRY GET INFO ABOUT {member.name} / {message.guild} BY {message.author} AT {time_now()}')
        with open('LOG.txt', 'a', encoding="utf-8") as file:
            file.write(f'TRY GET INFO ABOUT {member.name} / {message.guild} BY {message.author} AT {time_now()}\n')
        await message.respond('Нельзя вывести информацию о боте')

# Выдает роль пользователю
@bot.slash_command(description='Выдает роль', name='set_role', pass_context=True)
@commands.has_role("♣Босс♣")
async def set_role(message, member : discord.User, role : discord.Role):
    print(f'SET_ROLE {role.name} FOR {member.name} / {message.guild} BY {message.author} AT {time_now()}')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'SET_ROLE {role.name} FOR {member.name} / {message.guild} BY {message.author} AT {time_now()}\n')
    await member.add_roles(role)
    await message.respond(f'Пользователю {member.name} выдана роль {role}')

# Добавляет пользователя в базу данных в случае если он не был зарегистрирован при подключении к серверу
@bot.slash_command(description='Добавляет пользователя в базу данных вручную', name='add_to_data_base', pass_context=True)
async def add_to_data_base(message, member : discord.User):
    print(f'ADD_TO_DATA_BASE {member.name} / {message.guild} BY {message.author} AT {time_now()}')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'ADD_TO_DATA_BASE {member.name} / {message.guild} BY {message.author} AT {time_now()}\n')
    error_finder = bot_data_base.add_user(member.id, 1, message.guild.id, member.name)
    if error_finder == 0:
        await message.respond(f'Пользователь {member.name} добавлен в базу данных')
    else:
        await message.respond(f'Возникла ошибка при добавлении {member.name} в базу данных')

# Добавляет набор из 5 основных ролей для работы сервера
@bot.slash_command(description='Добавляет на сервер набор из 5 ролей', name='add_bot_roles', pass_context=True)
async def add_bot_roles(message):
    print(f'ADD_BOT_ROLES TO {message.guild.name}')
    with open('LOG.txt', 'a', encoding="utf-8") as file:
        file.write(f'ADD_BOT_ROLES TO {message.guild.name}\n')
    new_role_5 = await message.guild.create_role(name='Любимчик администрации', color=0xfcf7b5)
    new_role_4 = await message.guild.create_role(name='Любимчик бармена', color=0xfcffaf)
    new_role_3 = await message.guild.create_role(name='Завсегдатай', color=0xfcff82)
    new_role_2 = await message.guild.create_role(name='Посетитель', color=0xf4ec7f)
    new_role_1 = await message.guild.create_role(name='Проходимец', color=0xf2da71)
    await message.respond(f'Роли бота добавлены на сервер')

bot.run(config['token'])