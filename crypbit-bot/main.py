import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import response
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
import graph
load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="/", help_command=None)
slash = SlashCommand(bot,sync_commands=True)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@slash.slash(name ="crypbit",description="check whether bot is alive or not.")
async def crypbit(ctx):
    embed = discord.Embed(description=f"Hey {ctx.author.mention}")
    await ctx.send(embed=embed)
  
@slash.slash(name ="price",description="get the latest ticker price")
async def price(ctx, tikcername):
    responseName, respondPrice = response.getTicketPrice(tikcername.lower())
    embed = discord.Embed(title=f"Current value of {responseName}:", description=f"${respondPrice}",color=0x66acba)
    await ctx.send(embed=embed)

@slash.slash(name ="whatis",description="get description of any ticker.")
async def whatis(ctx, tickername):
    coinDesc, embed = response.sendDesc(tickername)
    button = [
        create_button(style=ButtonStyle.URL, label=f"{tickername} webpage", url=coinDesc[3])
    ]
    action_row = create_actionrow(*button)
    await ctx.send(embed=embed, components=[action_row])

@bot.command()
async def chart(ctx, tickername):
    chart_file = "chart.jpg"
    graph.plotGraph(tickername.upper(), chart_file)
    file = discord.File(chart_file, filename=chart_file)
    embed = discord.Embed(title=f"Graph for {tickername}")
    embed.set_image(url=f"attachment://{chart_file}")
    await ctx.send(file=file, embed=embed)
    os.remove(chart_file) 

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
    