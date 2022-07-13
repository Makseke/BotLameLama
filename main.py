from config import config

import discord, os, datetime, json
import random

from discord.ext import commands
import discord.user

from random import randint

import requests
from bs4 import BeautifulSoup

dt = datetime.datetime.now()
dt_string = dt.strftime("Date: %d/%m/%Y  Time: %H:%M:%S")

bot = commands.Bot(command_prefix = config['prefix'])
client = discord.Client
chanal = discord.TextChannel
guild = discord.Guild

print('--------------------------------------------------')
print('SERVER ONLINE')
print(dt_string)
print('--------------------------------------------------')

@bot.command()
async def testworking(message):
    await message.reply('Working')

#Выводит число в переданном диапазоне из 2 цифр, или 1 случайный элемент из переданных в команду
@bot.command()
async def random(message, *arg):
    print(f'RANDOM BY {message.author} / {message.guild} AT {dt_string} ')
    if len(arg) == 2 and str(arg[0]).isdigit() == True and str(arg[1]).isdigit() == True:
        min = int(arg[0])
        max = int(arg[1])
        if min > max:
            _ = min
            min = max
            max = _
        await message.reply(randint(min, max))
    else:
        await message.reply(arg[randint(0, len(arg))])
    await message.message.delete()

#Выводит онформацию о пользователе
@bot.command()
@commands.has_role('♣Босс♣')
async def info(message, user: discord.User):
    print(f'GET INFO ABOUT {user.name} / {message.guild} BY {message.author} AT {dt_string}')
    user_info = f'Имя пользователя: {user.name}\n' \
                f'Отображаемое имя: {user.display_name}\n' \
                f'ID пользователя: {user.id}\n' \
                f'Дата регистрации аккаунта: {user.created_at}\n'
    await message.send(user_info)

bot.run(config['token'])