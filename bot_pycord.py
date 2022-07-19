from config import config
import bot_data_base

import discord
from discord.commands import Option
from discord.ext import commands
from discord.utils import get

from random import randint

import datetime

import time

import psycopg2
from psycopg2 import Error

bot_data_base.server_srart()

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(
    intents=intents,
    # debug_guilds=[995982160928444486]
)

def time_now():
    dt = datetime.datetime.now()
    dt_string = dt.strftime("DATE: %d/%m/%Y  TIME: %H:%M:%S")
    return dt_string

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

print('--------------------------------------------------')
print('SERVER ONLINE')
print(time_now())

@bot.event
async def on_ready():
    print('--------------------------------------------------')
    print(f'INFO AT {time_now()}')
    for guilds in bot.guilds:
        print(f'{guilds} SERVER WITH {guilds.member_count} USERS USING LAMELAMA')
    print('--------------------------------------------------')
    print(f"{len(bot.guilds)} SERVERS USING LAMELAMA")
    print('--------------------------------------------------')
    global tdict
    tdict = {}
    global time_start
    time_start = time.time()

@bot.event
async def on_voice_state_update(member, before, after):
    author = member.id
    if before.channel is None and after.channel is not None:
        tdict[author] = time.time()
    elif before.channel is not None and after.channel is None and author in tdict:
        print(sec_to_time(str(time.time()-tdict[author]).split('.')[0]), f'BY {member.name} AT {member.guild}')
    elif before.channel is not None and after.channel is None and author not in tdict:
        print(sec_to_time(str(time.time() - time_start).split('.')[0]), f'BY {member.name} AT {member.guild} AFTER SERVER RESTART')

@bot.event
async def on_member_join(member):
    print(f'ADD_TO_DATA_BASE WHEN MEMBER JOIN SERVER {member.name} / {member.guild} AT {time_now()}')
    error_finder = bot_data_base.add_user(member.id, 1, member.guild.id, member.name)
    if error_finder == 0:
        print(f'Пользователь {member.name} добавлен в базу данных')
    else:
        print(f'Возникла ошибка при добавлении {member.name} в базу данных')

@bot.event
async def on_message(message):
    if message.author.name != 'BotLameLama':
        bot_data_base.add_message_to_user(message.author.id, message.author.guild.id)


@bot.slash_command(description="Выдает случайное число в переданном диапазоне", name="random")
async def makseke(message, min: Option(int), max: Option(int)):
    print(f'RANDOM BY {message.author} / {message.guild} AT {time_now()} ')
    if min > max:
        _ = min
        min = max
        max = _
    await message.respond(randint(min, max))

@bot.slash_command(description="Выдает случайное слово из введенной строки", name="random_word")
async def makseke(message, string: Option(str)):
    print(f'RANDOM_WORD BY {message.author} / {message.guild} AT {time_now()} ')
    string_list = string.split()
    if len(string_list) == 1:
        await message.respond(string_list[0])
    else:
        await message.respond(string_list[randint(0, len(string_list))])

@bot.slash_command(description='Выводит информацию о пользователе в виде карточки', name='info_card')
async def info_card(message, member: discord.User):
    print(f'GET INFO_CARD ABOUT {member.name} / {message.guild} BY {message.author} AT {time_now()}')
    dt_member = str(member.created_at).split('.')[0]
    embed = discord.Embed(
        title=f'Информация о пользователе {member.name}',
        description=f'Отображаемое имя: {member.display_name}\n' \
                    f'ID пользователя: {member.id}\n' \
                    f'Дата регистрации аккаунта: {dt_member}\n',
        color=0x2EE8CA
    )
    await message.respond(embed=embed)

@bot.slash_command(description='Выдает роль', name='set_role', pass_context=True)
@commands.has_role("♣Босс♣")
async def set_role(message, member : discord.User, role : discord.Role):
    print(f'SET_ROLE {role.name} FOR {member.name} / {message.guild} BY {message.author} AT {time_now()}')
    await member.add_roles(role)
    await message.respond(f'Пользователю {member.name} выдана роль {role}')

@bot.slash_command(description='Добавляет пользователя в базу данных вручную', name='add_to_data_base', pass_context=True)
async def set_role(message, member : discord.User):
    print(f'ADD_TO_DATA_BASE {member.name} / {message.guild} BY {message.author} AT {time_now()}')
    error_finder = bot_data_base.add_user(member.id, 1, message.guild.id, member.name)
    if error_finder == 0:
        await message.respond(f'Пользователь {member.name} добавлен в базу данных')
    else:
        await message.respond(f'Возникла ошибка при добавлении {member.name} в базу данных')

bot.run(config['token'])