import os

import discord

from dotenv import load_dotenv

import powers

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

power = powers.Power()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    hero_server = message.guild.name
    hero_name = message.author.name
    hero_request = message.content
    result = power.power("{}.{}".format(hero_server, hero_name), hero_request)
    if result:
        await message.channel.send(result)

token = os.environ['TOKEN']
client.run(token)
