import discord, os
import random
from discord.ext import commands
import discord.user
from random import randint

import requests
from bs4 import BeautifulSoup

url = 'https://ru.citaty.net/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('p')

print(quotes[0].text)
print(quotes[1].text)

# for quote in quotes:
#     print(quote.text)

config = {
    'prefix': '!',
}

bot = commands.Bot(command_prefix = config['prefix'])
client = discord.Client
chanal = discord.TextChannel

@bot.command()
async def testworking(message):
    await message.reply('Working')

#Выводит число в переданном диапазоне из 2 цифр, или 1 случайный элемент из переданных в команду
@bot.command()
async def random(message, *arg):
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

#Выводит онформацию о пользователе
@bot.command()
@commands.has_role('♣Босс♣')
async def info(message, user: discord.User):
    user_info = f'Имя пользователя: {user.name}\n' \
                f'Отображаемое имя: {user.display_name}\n' \
                f'ID пользователя: {user.id}\n' \
                f'Дата регистрации аккаунта: {user.created_at}\n'
    await message.send(user_info)

@bot.command()
async def sent(message):
    random_key = randint(1, len(quotes))
    if random_key % 2 == 0:
        random_key += 1
    text = str(quotes[random_key].text)
    author = str(quotes[random_key + 1].text)
    message_ = text + author
    await message.send(message_)

bot.run(config['token'])