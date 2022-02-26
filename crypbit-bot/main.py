from json import load
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import response
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
    price = response.getTicketPrice(tikcerName)
    await ctx.send(price)

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
