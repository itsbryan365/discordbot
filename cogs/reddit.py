import discord 
import requests 
from discord.ext import commands
import aiohttp
import asyncio
import string
import praw
from prawcore import NotFound
import random
from random import randint

reddit = praw.Reddit(client_id="3GEx77dC-L8aDg",
                    client_secret="HzEr05QapqNh75CztenWBsCGfNU",
                    user_agent="itsbryan365")

def setup(client):
    client.add_cog(Reddit(client))


class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases = ['Meme'])
    async def meme(self, ctx):
        submissions = []
        for submission in reddit.subreddit("dankmemes").hot(limit = 100):
            if submission.score > 300:
                submissions.append(submission)
        submission = submissions[random.randint(0, len(submissions)-1)]
        embed = discord.Embed(
            title = submission.title,
            url = f"https://reddit.com{submission.permalink}",
            color = ctx.author.color
        )
        if submission.url.startswith('https://i.redd.it/'):
            embed.set_image(url = submission.url)
            await ctx.send(embed = embed)
        elif submission.url.startswith('https://v.redd.it/'):
            await ctx.send(submission.url)
        else:
            await ctx.send(embed = embed)
            await ctx.send(submission.url)
