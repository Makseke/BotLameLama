import discord
import random
from discord.ext import commands

config = {
    'prefix': '$',
}

bot = commands.Bot(command_prefix = config['prefix'])

@bot.command()
async def testworking(message):
    await message.reply('Working')

@bot.command()
async def random_number(message, *arg):
    min = int(arg[0])
    max = int(arg[1])
    await message.reply(random.randint(min, max))

@bot.command()
async def random_word(message, *arg):
    await message.reply(arg[random.randint(0, len(arg))])

bot.run(config['token'])