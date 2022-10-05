import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import requests
import response
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
import graph
import time
from pymongo import MongoClient
load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')
mongo_connect = os.environ.get('MONGO_CONNECT')

bot = commands.Bot(command_prefix="/", help_command=None)
slash = SlashCommand(bot,sync_commands=True)

client = MongoClient(mongo_connect)
database = client['crypbit_test']
slugCollection = database['slug']
watchlistCollection = database['watchlist']

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@slash.slash(name ="test",description="check whether bot is alive or not.")
async def test(ctx):
    if(watchlistCollection.find_one({"_id":"Crypbit"})):
        print("Present")
    else:print("Not present")

@slash.slash(name ="whatis",description="get description of any ticker.")
async def whatis(ctx, tickername):
    coinDesc = response.getCoinDesc(tickername.upper())
    button = [
        create_button(style=ButtonStyle.URL, label=f"{tickername} webpage", url=coinDesc[3])
    ]
    action_row = create_actionrow(*button)
    embed = discord.Embed(title=coinDesc[1], description=coinDesc[0], color=0xFFFFFF).set_thumbnail(url=coinDesc[2])
    await ctx.send(embed=embed, components=[action_row])

@slash.slash(name="chart", description="Chart for specified ticker")
async def chart(ctx, tickername):
    start = time.time()
    try:
        chart_file = "chart.jpg"
        check = graph.plotGraph(tickername.upper(), chart_file)
        print(check)
        file = discord.File(chart_file, filename=chart_file)
        embed = discord.Embed(title=f"Graph for {tickername}")
        embed.set_image(url=f"attachment://{chart_file}")
        await ctx.send(file=file, embed=embed)
        os.remove(chart_file)
    except:
        print("Error occured here...")
    print(time.time() - start)

@slash.slash(name="stats", description="get price of any ticker")
async def stats(ctx, ticker):
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    entire_data = response.json()
    ticker = slugCollection.find_one({'symbol':ticker.upper()})['market']
    try:
        embed = discord.Embed(title=f"Stats for {ticker} :bar_chart:")
        for data in entire_data:
            if data['market'] == ticker:
                change_24_h = float(data['change_24_hour'])
                embed.add_field(name="Price", value=f"{format(float(data['last_price']), '.3f')} \N{Fire}")
                embed.add_field(name="Volume", value=format(float(data['volume']), ".3f"))
                if(change_24_h < 0):embed.set_field_at(index=1, name="Percent change in 24h", value=f"{format(change_24_h, '.2f')}% :chart_with_downwards_trend:")
                elif(change_24_h > 0):embed.set_field_at(index=1, name="Percent change in 24h", value=f"{format(change_24_h, '.2f')}% :chart_with_upwards_trend:")
                break

        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="Oops! ticker not found", description="Try using command with ticker(with its market) eg. btcusdt")
        await ctx.send(embed=embed)

@slash.slash(name="watchlist", description="to add tokens to the watchlist")
async def watchlist(ctx, slugs):
    guildDoc = watchlistCollection.find_one({"_id":ctx.guild.id})
    slugs = slugs.strip().split(" ")
    if(guildDoc):
        guildDoc['tickers'] += slugs
        embed = discord.Embed(title="Watchlist successfully updated")
    else:
        watchlistCollection.insert_one({"_id":ctx.guild.id, "tickers":slugs})
        embed = discord.Embed(title="Watchlist successfully added")
    await ctx.send(embed=embed)

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
    