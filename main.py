import discord, os
import random
from discord.ext import commands
import discord.user
from random import randint

config = {
    'prefix': '!',
}

bot = commands.Bot(command_prefix = config['prefix'])
client = discord.Client
chanal = discord.TextChannel

@bot.command()
async def testworking(message):
    await message.reply('Working')

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

@bot.command()
async def info(message, user: discord.User):
    print(user.name)
    print(user.id)
    print(user.created_at)

bot.run(config['token'])