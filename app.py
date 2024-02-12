import os

import bcrypt
import discord
import cherrypy

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
    hero = str(bcrypt.hashpw("{}.{}".format(hero_server, hero_name).encode(), salt))

    hero_request = message.content
    result = power.power(hero, hero_name, hero_request)
    if result:
        await message.channel.send(result)



class HelloWorld:
    @cherrypy.expose
    def index(self):
        return "Hello, world!"


token = os.environ['TOKEN']
salt = bytes(os.environ['SALT'], 'utf8')
cherrypy.quickstart(HelloWorld())
client.run(token)