import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import response, info
from discord_buttons_plugin import  *
import plotly.graph_objects as go
import pandas_datareader as pdr
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="$", help_command=None)
button = ButtonsClient(bot)
bot.token = ""

def sendDesc(tickerName):
    coinDesc = info.getCoinDesc(tickerName)
    embed = discord.Embed(title=coinDesc[1], description=coinDesc[0], color=0xFFFFFF).set_thumbnail(url=coinDesc[2])
    return coinDesc, embed

#To fetch the data for specified ticker and plot it on the graph
def plotGraph(tickerName, chartFile):
    now = datetime.now()
    start = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    end = now.strftime("%Y-%m-%d")
    data = pdr.get_data_yahoo(f"{tickerName}-{'USD'}", start, end)
    
    fig = go.Figure(
        data=[
            go.Candlestick(
                x = data.index,
                open=data.Open,
                high=data.High,
                low=data.Low,
                close=data.Close
            )
        ]
    )
    fig.update_layout(
        title=f"Statistics of {tickerName} over past 1 year",
        xaxis_title="Date",
        yaxis_title=f"Value of {tickerName}",
        xaxis_rangeslider_visible=False,
        title_x=0.5
    )
    fig.update_yaxes(tickprefix='$')
    fig.write_image(chartFile)


@bot.event
async def on_ready():
    print("We have logged in as {}".format(bot.user))

@bot.command()
async def ping(ctx):
    await ctx.send("Pong")

@bot.command()
async def hello(ctx):
    embed = discord.Embed(description="Hey {}".format(ctx.message.author.mention))
    await ctx.reply(embed=embed)
    

@bot.command()
async def price(ctx, tikcerName):
    responseName, respondPrice = response.getTicketPrice(tikcerName.lower())
    bot.token = tikcerName
    embed = discord.Embed(title="Current value of {}".format(responseName), description="${}".format(respondPrice), color=0x66acba)
    await ctx.reply(embed=embed)

@bot.command()
async def whatis(ctx, tickerName):
    coinDesc, embed = sendDesc(tickerName)
    await button.send(
        embed=embed,
        channel=ctx.channel.id,
        components=[
            ActionRow([
                Button(
                    label="{} Webpage".format(coinDesc[1]),
                    style=ButtonType().Link,
                    url=coinDesc[3]
                )
            ])
        ]
    )

@bot.command()
async def stat(ctx, tickerName):
    chartFile = "chart.jpg"
    plotGraph(tickerName.upper(), chartFile)
    embed = discord.Embed(title=f"Graph for {tickerName}")
    file = discord.File(chartFile, filename=chartFile)
    embed.set_image(url=f"attachment://{chartFile}")
    await ctx.reply(file=file, embed=embed)
    os.remove(chartFile) 

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")