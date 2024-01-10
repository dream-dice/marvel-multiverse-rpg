import os

import discord

from dotenv import load_dotenv

import robot

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = message.author.name
    if message.content.startswith('!cap d616'):
        robot.d616(username)
        await message.channel.send(robot.display(username))

token = os.environ['TOKEN']
client.run(token)
