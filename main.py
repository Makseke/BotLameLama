import discord
from discord.ext import commands

config = {
    'prefix': '$',
}

bot = commands.Bot(command_prefix = config['prefix'])

@bot.event
async def test(m):
    if m.author != bot.user:
        await m.reply(m.content)

@bot.command()
async def testworking(m):
    await m.reply('Working')

bot.run(config['token'])