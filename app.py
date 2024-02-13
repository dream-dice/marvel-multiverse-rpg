import os
import random
import string


import bcrypt
import cherrypy
import discord

from dotenv import load_dotenv

import powers
import routes


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
power = powers.Power()
token = os.environ['TOKEN']
salt = bytes(os.environ['SALT'], 'utf8')

@client.event
async def on_ready():
    start_cherrypy(client)
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    hero_server = message.guild.name
    hero_name = message.author.name
    hero = str(
        bcrypt.hashpw('{}.{}'.format(
            hero_server, hero_name).encode(), salt
        )
    )

    hero_request = message.content
    result = power.power(hero, hero_name, hero_request)
    if result:
        await message.channel.send(result)


def start_cherrypy(client):
    cherrypy.config.update({
        'engine.autoreload.on': False,
        'server.socket_port': 8099
    })
    cherrypy.tree.mount(routes.D616(client), '/d616')
    cherrypy.engine.start()


def start_discord():
    client.run(token)


if __name__ == '__main__':
    start_discord()
