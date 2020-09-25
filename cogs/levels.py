import discord
from discord.ext import commands
import sqlite3
import math
import typing

conn=sqlite3.connect('database.db')
c=conn.cursor()

class levels(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def find_level(self, xp):
        return int((math.floor(math.sqrt(25 * xp+25)-5)/10))

    def find_xp(self, level):
        return 5*level *level + (5*level)
     
    # level_badges = {
    #     1: ":small_blue_diamond:"
    #     5: ":large_blue_diamond:"
    #     10: ":diamond_shape_with_a_dot_inside:"
    #     20: ":beginner:"
    #     30: ":reminder_ribbon:"
    #     40: ":military_metak:"
    # }



    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        c.execute("SELECT * FROM users WHERE id =?", (msg.author.id,))
        data= c.fetchone()
        if not data:
            c.execute("INSERT INTO users VALUES (?,?,?)", (msg.author.id, msg.author.name, 1))
            conn.commit()
            return
        level = self.find_level(data[2])
        new_level= self.find_level(data[2]+1)
        if level != new_level:
            await msg.channel.send(f"congratulation {msg.author.display_name}, your iq is {new_level} ")
        c.execute("UPDATE users SET xp = ?, name = ? WHERE id = ?", (data[2]+1, msg.author.name, msg.author.id))
        conn.commit()


    @commands.command()
    async def get_level(self, ctx, xp):
        await ctx.send(self.find_level(int(xp)))    



def setup(client):
    client.add_cog(levels(client))