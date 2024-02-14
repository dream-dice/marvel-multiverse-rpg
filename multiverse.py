import asyncio
import requests
import urllib.parse

import cherrypy

API_ENDPOINT = 'https://discord.com/api/v10'


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


def get_channels(access_token, guild_id):
    headers = {
        'Authorization': 'Bearer %s' % access_token
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

    def reply(self):
        asyncio.run_coroutine_threadsafe(
            self.send_message(self.client, 1090624671881363500, 'Hello'),
            self.client.loop
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def d616(self):
        # self.reply()
        access_token = 'PzvIb3VTIe6XqN1yHiEQLWeFllaVRd'
        user = get_user(access_token)
        guilds = get_guilds(access_token)
        # channel = get_channel(access_token, '1090624670467899424')
        return {
            "user": user,
            "guilds": guilds
        }

    @cherrypy.expose
    def callback(self, state, code):
        res = exchange_code(self.discord_client_id,
                            self.discord_client_secret, code)

        return "Hello, world! {} {} {}".format(state, code, res)

    @cherrypy.expose
    def index(self):
        session_id = cherrypy.session.id

        redirect_uri = "https://local.trailapp.com/robot/callback"
        encoded_uri = urllib.parse.quote_plus(redirect_uri)
        login_url = "https://discord.com/oauth2/authorize?response_type=code&client_id={}&scope=identify%20guilds&state={}&redirect_uri={}&prompt=consent".format(
            self.discord_client_id,
            session_id,
            encoded_uri
        )
        return """
<a href="{}">login</a>
""".format(login_url)
