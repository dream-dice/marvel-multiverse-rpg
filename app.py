import os

import cherrypy
import discord

from dotenv import load_dotenv

import powers
import multiverse


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

power = powers.Power()
token = os.environ['TOKEN']
salt = bytes(os.environ['SALT'], 'utf8')
port = os.environ['PORT']
base_route = os.environ['BASE_ROUTE']
discord_client_id = os.environ['DISCORD_CLIENT_ID']
discord_client_secret = os.environ['DISCORD_CLIENT_SECRET']


def start_cherrypy():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'engine.autoreload.on': True,
        'tools.sessions.on': True,
        "tools.sessions.storage_class": cherrypy.lib.sessions.FileSession,
        "tools.sessions.storage_path": "sessions",
        'tools.sessions.timeout': 60,
        'tools.sessions.secure': True,
        'tools.sessions.httponly': True,
        'server.socket_port': int(port)
    })
    cherrypy.quickstart(
        multiverse.Multiverse(
            discord_client_id,
            discord_client_secret
        )
    )


if __name__ == '__main__':
    start_cherrypy()
