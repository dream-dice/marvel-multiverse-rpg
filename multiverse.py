import asyncio
import os
import requests
import urllib.parse

from dotenv import load_dotenv
from discord import SyncWebhook
import cherrypy

from marvel import Marvel

API_ENDPOINT = 'https://discord.com/api/v10'

load_dotenv()
token = os.environ['TOKEN']


def get_user(access_token):
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    r = requests.get('%s/users/@me' % API_ENDPOINT, headers=headers)
    r.raise_for_status()
    return r.json()


def get_guilds(access_token):
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    r = requests.get('%s/users/@me/guilds' % API_ENDPOINT, headers=headers)
    r.raise_for_status()
    return r.json()


def get_channels(guild_id):
    headers = {
        'Authorization': 'Bot %s' % token
    }
    r = requests.get('%s/guilds/%s/channels' %
                     (API_ENDPOINT, guild_id), headers=headers)
    r.raise_for_status()
    return r.json()


def exchange_code(client_id, client_secret, code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "https://local.trailapp.com/robot/callback"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data,
                      headers=headers, auth=(client_id, client_secret))
    r.raise_for_status()
    return r.json()


def refresh_token(refresh_token, client_id, client_secret):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data,
                      headers=headers, auth=(client_id, client_secret))
    r.raise_for_status()
    return r.json()


def revoke_access_token(access_token, client_id, client_secret):
    data = {
        'token': access_token,
        'token_type_hint': 'access_token'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    requests.post('%s/oauth2/token/revoke' % API_ENDPOINT, data=data,
                  headers=headers, auth=(client_id, client_secret))


async def send_message(client, channel_id, message):
    channel = client.get_channel(channel_id)
    await channel.send(message)


class Multiverse():
    def __init__(self, client, discord_client_id, discord_client_secret):
        self.client = client
        self.discord_client_id = discord_client_id
        self.discord_client_secret = discord_client_secret
        self.mdb = Marvel()

    def reply(self):
        asyncio.run_coroutine_threadsafe(
            self.send_message(self.client, 1090624671881363500, 'Hello'),
            self.client.loop
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def db(self):
        bacon = cherrypy.session.get("bacon")
        cherrypy.session["bacon"] = "soup"

        return {"hello": bacon}

    @cherrypy.expose
    def get(self):
        user_id = cherrypy.session.get("user_id")
        user = self.mdb.get_user(user_id)
        access_token = user.access_token
        guilds = get_guilds(access_token)
        channels = []
        for guild in guilds:
            if "intrepid" in guild["name"].lower():
                print(guild)
                channels = get_channels(guild["id"])
        return "{}".format(channels)

    @cherrypy.expose
    # def callback(self, state, code, guild_id):
    def callback(self, state, code):
        res = exchange_code(
            self.discord_client_id,
            self.discord_client_secret,
            code
        )

        # webhook_id = res["webhook"]["id"]
        # webhook_token = res["webhook"]["token"]
        # webhook_url = 'https://discord.com/api/webhooks/{webhook_id}/{webhook_token}'.format(
        #     webhook_id=webhook_id,
        #     webhook_token=webhook_token
        # )
        # webhook = SyncWebhook.from_url(webhook_url)
        # webhook.send("Hello, World!")

        access_token = res["access_token"]
        expires_in = res["expires_in"]
        refresh_token = res["refresh_token"]
        user = get_user(res["access_token"])
        id = user["id"]
        username = user["username"]

        guilds = get_guilds(access_token)

        cherrypy.session["user_id"] = id
        self.mdb.add_user(id, username, access_token,
                          refresh_token, expires_in)

        channels = []
        for guild in guilds:
            if "luke" in guild["name"].lower():
                channels = get_channels(access_token, guild["id"])
                print(channels)

        return "Hello, world! {} {} {} {} {} {}".format(state, code, res, user, guilds, channels)

    @cherrypy.expose
    def index(self):
        session_id = cherrypy.session.id

        redirect_uri = "https://local.trailapp.com/robot/callback"
        encoded_uri = urllib.parse.quote_plus(redirect_uri)
        scope = "identify%20guilds%20webhook.incoming"
        scope = "identify%20guilds"
        login_url = "https://discord.com/oauth2/authorize?response_type=code&client_id={}&scope={}&state={}&redirect_uri={}&prompt=consent".format(
            self.discord_client_id,
            scope,
            session_id,
            encoded_uri
        )
        return """
<a href="{}">login</a>
""".format(login_url)
