import os

import discord

from dotenv import load_dotenv

# from run_command import run_command

load_dotenv()

# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)


# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     response = run_command(message.author.name, message.content)
#     if response:
#         await message.channel.send(response)

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.slash_command(name="first_slash")
async def first_slash(ctx):
    await ctx.respond("You executed the slash command!")

token = os.environ['TOKEN']
# client.run(token)
bot.run(token)
