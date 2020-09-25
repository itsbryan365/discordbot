import discord
from discord.ext import commands
import random
import os
import string
import requests
import sqlite3
import time
t=time

default_prefixes = ['b.']

async def determine_prefix(bot, message):
    guild=message.guild
    if guild:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild.id,))
        data = c.fetchone()
        if data:
            return [data[1]] + ['bbot plz ']
    return default_prefixes + ['bbot plz ']

client = commands.Bot(command_prefix = determine_prefix)

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

@client.event
async def on_ready():
    print("bot is ready ")

@client.command()
@commands.guild_only()
async def setprefix(ctx, *, prefix):
    ' '.join(prefix)
    if prefix[0] == '"' and prefix[-1] == '"' or prefix[0] == "'" and prefix[-1] == "'":
        prefix = prefix[1:-1]
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    data = c.fetchone()
    if not data:
        c.execute("INSERT INTO guilds VALUES (?,?)", (ctx.guild.id, prefix))
    else:
        c.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id))
    conn.commit()
    await ctx.send(f"Prefix set to {prefix}")

@client.command()
@commands.guild_only()
async def resetprefix(ctx):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    data = c.fetchone()
    if not data :
        await ctx.send("This server does not have a custom prefix")
        return
    c.execute("DELETE FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    conn.commit()
    default = ''
    for i in default_prefixes:
        default += f"{i} "
    await ctx.send(f"prefixes were reset to default prefixes {default}")


@client.command()
@commands.guild_only()
async def prefix(ctx):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    data = c.fetchone()
    if not data :
        default = ''
        for i in default_prefixes:
            default += f"{i} "
        await ctx.send(f"NO custom prefixes are set. Default prfixes are {default}")
        return
    await ctx.send(f"current prefix is '{data[1]}'")

@client.command(aliases = ['close', 'stop'])
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Bot shutting down...")
    await client.close()
   
    

#math
@client.command()
async def square(ctx,num):
    await ctx.send((int(num))**2)

@client.command()
async def add(ctx,num1,num2):
    await ctx.send(int(num1)+int(num2))
# @client.command()
# async def embedism(ctx):
#     embed = discord.Embed(
#     title = "meme",
#     url = f"https://www.youtube.com/channel/UCCWp4CCmI2JmIaoAuv0ocEA",
#     color = ctx.author.color
#     )
#     await ctx.send(embed=embed)

@client.command()
async def memevideos(ctx):
    await ctx.send(f"memevideos: https://www.youtube.com/channel/UCCWp4CCmI2JmIaoAuv0ocEA")
@client.command()
async def brawlstars(ctx):
    await ctx.send(f"brawlstars: https://www.youtube.com/results?search_query=brawl+stars")
  
    

@client.command()
async def server(ctx):
    await ctx.send(f"this is {ctx.guild.name}")

@client.command()
async def say(ctx,something):
    await ctx.send(something)

@client.command()
async def spam(ctx, what, times):
    t.sleep(10)
    for i in range(1, int(times)+1):
        await ctx.send(what)
        t.sleep(0.2)


@client.command()
async def timer(ctx, seconds):
    await ctx.send("timer activated")
    t.sleep(int(seconds))
    await ctx.send("timers up")    


#numbergamer

@client.command()
async def ng(ctx, range1, range2):
    range1=int(range1)
    range2=int(range2)
    number=random.randint(range1, range2)
    await ctx.send("im thinking of a number between %s and %s, you can start guessing" %(range1,range2))
    def check(m):
        return m.channel == ctx.channel
    try:
        msg = await self.client.wait_for('message', timeout = 300.0, check = check)
    except asyncio.TimeoutError:
        await ctx.send('game timed out.')
@client.command()
async def shoot(ctx, name):
    ctx.send("(⌐▀͡ ̯ʖ▀)︻̷┻̿═━一-  %s ",(name)) 




# @commands.command()
# async def weather(self, ctx, *, city_name: str):
#     url = f'http://api.openweathermap.org/data/2.5/weather?q=%7Bcity_name%7D&appid=5600d029daa66557cbb0b2c66c52a0e4'
#     response = requests.get(url)
#     result = response.json()
#     emoji = ":sunny:"
#     embed = discord.Embed(
#         title=f"Weather in {city_name}",
#         description=f" {emoji} {result['weather'][0]['description']}",
#     )
#     embed.add_field(name="Weather", value =f"\n :thermometer: {(int)((result['main']['temp'] - 273.15) * 9/5 +32)} °F \n :high_brightness: Feels like {(int)((result['main']['feels_like'] - 273.15) * 9/5 +32)} °F \n :small_red_triangle: Max: {(int)((result['main']['temp_max'] - 273.15) * 9/5 +32)} °F \n :small_red_triangle_down: Min: {(int)((result['main']['temp_min'] - 273.15) * 9/5 +32)} °F", inline = True)
#     embed.add_field(name="Winds", value = f"\n :cloud: Wind Speed: {result['wind']['speed']} MPH \n :compass: Bearing: {result['wind']['deg']} degrees \n \n :cloud_tornado: Air Pressure: {result['main']['pressure']}")
#     await ctx.send(embed=embed)
# client.run('NzMxOTY3MzE1NjQ1Njk0MDUz.Xwtvrw.EfiHk59pnfKlCmV4-Ta0z-BpecM')