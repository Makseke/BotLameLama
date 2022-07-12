import interactions
from random import randint
import datetime
import discord.user
from discord.ext import commands

bot = interactions.Client('OTk1MzA5NzExMzUwMDM4NTc4.GTS_QM.VtqDhxzeyfshVDWSjYXwHw5tI1_9JCJ6ym6G7o')
user = interactions.User
guild = interactions.Guild

dt = datetime.datetime.now()
dt_string = dt.strftime("Date: %d/%m/%Y  Time: %H:%M:%S")

print('--------------------------------------------------')
print('SERVER ONLINE')
print(dt_string)
print('--------------------------------------------------')

@bot.command(
    name='test',
    description='desc...',
)
async def test(message):
    await message.send('YES YES YES')

#Выводит число в переданном диапазоне из 2 цифр, или 1 случайный элемент из переданных в команду
@bot.command(
    name='random',
    description='Выводит случайное число из переданного диапазона, или лдно случайное слово',
    options=[interactions.Option(
        name='arg',
        description='Выводит случйное число из переданного диапазона, или лдно случайное слово',
        type=interactions.OptionType.STRING,
        required=True
    )]

)
async def random(message, arg):
    print(f'RANDOM BY {message.author} / {message.guild} AT {dt_string} ')
    val = arg.split()
    min = int(val[0])
    max = int(val[1])
    await message.send(randint[min, max])

#Выводит онформацию о пользователе
# @bot.command()
# @commands.has_role('♣Босс♣')
# async def info(message, user: discord.User):
#     print(f'GET INFO ABOUT {user.name} / {message.guild} BY {message.author} AT {dt_string}')
#     user_info = f'Имя пользователя: {user.name}\n' \
#                 f'Отображаемое имя: {user.display_name}\n' \
#                 f'ID пользователя: {user.id}\n' \
#                 f'Дата регистрации аккаунта: {user.created_at}\n'
#     await message.send(user_info)


bot.start()