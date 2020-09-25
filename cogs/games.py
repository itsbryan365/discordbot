import discord
import requests
from discord.ext import commands
import os
import random
import html
import asyncio

class games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def t(self, ctx):
        data = requests.get("https://opentdb.com/api.php?amount=1&type=multiple").json()
        results = data['results'][0]
        embed = discord.Embed(
            title = ":question: Trivia",
            description = f"Category: {results['category']} | Difficulty: {results['difficulty'].capitalize()}",
            color = ctx.author.color
        )

        pos = random.randint(0, 3)
        if pos == 3:
            answers = results['incorrect_answers'] + [results['correct_answer']]
        else:
            answers = results['incorrect_answers'][0:pos] + [results['correct_answer']] + results['incorrect_answers'][pos:]
        value = ''
        letters=['a','b','c','d']
        for i in range(len(answers)):
            value += f"{letters[i].capitalize()}) {answers[i]}\n"
        embed.add_field(name = html.unescape(results['question']), value = value)
        embed2 =embed
        question = await ctx.send(embed = embed)
        available_commands = letters + [a.lower() for a in answers]
        def check(m):
            return m.channel == ctx.channel and m.content.lower() in available_commands
        try:
            msg = await self.client.wait_for('message', timeout = 30.0, check = check)
        except asyncio.TimeoutError:
            return
        answer_string = f"The answer was {letters[pos].upper()}) {results['correct_answer']}"
        if msg.content.lower() == letters[pos] or msg.content.lower() == results['correct_answer'].lower():
            name = ":white_check_mark:  Correct"
        else:
            name = ":x:  Incorrect"
        embed2.clear_fields()
        embed2.add_field(name = name, value = answer_string)
        await question.edit(embed = embed2)
        
        
def setup(client):
    client.add_cog(games(client))