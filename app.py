import os
import random
import string


import bcrypt
import cherrypy
import discord

from dotenv import load_dotenv

import cassandra_session
import powers
import multiverse


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
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
        'server.socket_host': '0.0.0.0',
        'engine.autoreload.on': False,
        'tools.sessions.on': True,
        "tools.sessions.storage_class": cassandra_session.CassandraSession,
        'tools.sessions.timeout': 60,
        'tools.sessions.secure': True,
        'tools.sessions.httponly': True,
        'server.socket_port': int(port)
    })
    cherrypy.tree.mount(
        multiverse.Multiverse(
            client,
            discord_client_id,
            discord_client_secret
        ),
        base_route
    )
    cherrypy.engine.start()


def start_discord():
    client.run(token)


if __name__ == '__main__':
    start_discord()
