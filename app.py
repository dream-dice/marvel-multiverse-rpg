import os

import discord

from dotenv import load_dotenv

from run_command import run_command

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

    response = run_command(message.author.name, message.content)
    if response:
        await message.channel.send(response)

token = os.environ['TOKEN']
client.run(token)
