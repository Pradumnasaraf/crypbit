from json import load
import os
from turtle import color, title
from discord.ext import commands
import discord
from dotenv import load_dotenv
import response, info
load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="?")


@bot.event
async def on_ready():
    print("We have logged in as {}".format(bot.user))

@bot.command()
async def ping(ctx):
    await ctx.send("Pong")

@bot.command()
async def hello(ctx):
    await ctx.send("Hey {}".format(ctx.message.author.mention))

@bot.command()
async def price(ctx, tikcerName):
    respondPrice = response.getTicketPrice(tikcerName)
    embed = discord.Embed(title="Current value of {}".format(tikcerName), description="${}".format(respondPrice), color=0x66acba)
    await ctx.send(embed=embed)

@bot.command()
async def whatis(ctx, tickerName):
    coinDesc = info.getCoinDesc(tickerName)
    embed = discord.Embed(title=coinDesc[1], description=coinDesc[0], color=0xFFFFFF).set_thumbnail(url=coinDesc[2])
    await ctx.send(embed=embed)
try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
