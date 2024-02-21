import os

import bcrypt
import discord
from dotenv import load_dotenv

import powers


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

power = powers.Power()
token = os.environ['TOKEN']
salt = bytes(os.environ['SALT'], 'utf8')
port = os.environ['PORT']
base_route = os.environ['BASE_ROUTE']
discord_client_id = os.environ['DISCORD_CLIENT_ID']
discord_client_secret = os.environ['DISCORD_CLIENT_SECRET']


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    hero_server = message.guild.id
    hero_name = message.author.id
    hero = str(
        bcrypt.hashpw('{}.{}'.format(
            hero_server, hero_name).encode(), salt
        )
    )

    hero_request = message.content
    result = power.power(hero, hero_name, hero_request)
    if result:
        await message.channel.send(result)


if __name__ == '__main__':
    client.run(token)
