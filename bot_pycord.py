from config import config

import discord
from discord.commands import Option

from random import randint

import datetime

dt = datetime.datetime.now()
dt_string = dt.strftime("Date: %d/%m/%Y  Time: %H:%M:%S")

print('--------------------------------------------------')
print('SERVER ONLINE')
print(dt_string)
print('--------------------------------------------------')


intents = discord.Intents.default()

bot = discord.Bot(
    intents=intents,
    debug_guilds=[995982160928444486]
)


@bot.slash_command(description="Выдает случайное число в переданном диапазоне", name="random")
async def makseke(message, min: Option(int), max: Option(int)):
    print(f'RANDOM BY {message.author} / {message.guild} AT {dt_string} ')
    await message.respond(randint(min, max))

@bot.slash_command(description="Выводит информацию о пользователе", name="info")
async def info(message, member: discord.User):
    print(f'GET INFO ABOUT {member.name} / {message.guild} BY {message.author} AT {dt_string}')
    user_info = f'Имя пользователя: {member.name}\n' \
                f'Отображаемое имя: {member.display_name}\n' \
                f'ID пользователя: {member.id}\n' \
                f'Дата регистрации аккаунта: {member.created_at}\n'
    await message.send(user_info)

bot.run(config['token'])