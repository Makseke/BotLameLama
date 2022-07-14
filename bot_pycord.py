from config import config

import discord
from discord.commands import Option

from random import randint

import datetime

def time_now():
    dt = datetime.datetime.now()
    dt_string = dt.strftime("Date: %d/%m/%Y  Time: %H:%M:%S")
    return dt_string

print('--------------------------------------------------')
print('SERVER ONLINE')
print(time_now())
print('--------------------------------------------------')


intents = discord.Intents.default()

bot = discord.Bot(
    intents=intents,
    # debug_guilds=[995982160928444486]
)

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

@bot.slash_command(description="Выводит информацию о пользователе", name="info")
async def info(message, member: discord.User):
    print(f'GET INFO ABOUT {member.name} / {message.guild} BY {message.author} AT {time_now()}')
    dt_member = str(member.created_at).split('.')[0]
    user_info = f'Имя пользователя: {member.name}\n' \
                f'Отображаемое имя: {member.display_name}\n' \
                f'ID пользователя: {member.id}\n' \
                f'Дата регистрации аккаунта: {dt_member}\n'
    if member.name == 'makseke':
        user_info += 'Мой повелитель... и ваш...\n'
    await message.send(user_info)

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

bot.run(config['token'])