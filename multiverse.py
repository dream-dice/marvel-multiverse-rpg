import asyncio
import os
import requests
import urllib.parse

from dotenv import load_dotenv
import cherrypy

from marvel import Marvel

API_ENDPOINT = 'https://discord.com/api/v10'

load_dotenv()
token = os.environ['TOKEN']
callback_url = os.environ['DISCORD_CALLBACK']


def get_user(access_token):
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    r = requests.get('%s/users/@me' % API_ENDPOINT, headers=headers)
    r.raise_for_status()
    return r.json()


def get_guilds(bearer, access_token):
    headers = {
        'Authorization': '%s %s' % (bearer, access_token)
    }
    r = requests.get('%s/users/@me/guilds' % API_ENDPOINT, headers=headers)
    r.raise_for_status()
    return r.json()


def message(channel_id, message):
    headers = {
        'Authorization': 'Bot %s' % token
    }
    r = requests.post('%s/channels/%s/messages' %
                      (API_ENDPOINT, channel_id), headers=headers, data={"content": message})
    r.raise_for_status()
    return r.json()


def get_bot_role_id(client_id, guild_id):
    headers = {
        'Authorization': 'Bot %s' % token
    }

    r = requests.get('%s/guilds/%s/roles' %
                     (API_ENDPOINT, guild_id), headers=headers)
    r.raise_for_status()
    roles = r.json()
    bot_roles = [role for role in roles if "tags" in role and "bot_id" in role["tags"]
                 and role["tags"]["bot_id"] == client_id]
    return bot_roles[0]["id"]


def get_channels(guild_id):
    headers = {
        'Authorization': 'Bot %s' % token
    }
    r = requests.get('%s/guilds/%s/channels' %
                     (API_ENDPOINT, guild_id), headers=headers)
    r.raise_for_status()
    return r.json()


def get_bot_channels(client_id, guild_id):
    bot_role_id = get_bot_role_id(client_id, guild_id)
    channels = get_channels(guild_id)
    filtered_channels = [channel for channel in channels if channel.get(
        "parent_id") is not None and channel.get("bitrate") is None]
    channels_with_bot_access = [channel for channel in filtered_channels if any(
        overwrite['id'] == bot_role_id and overwrite['allow'] != '0' for overwrite in channel['permission_overwrites'])]
    if len(channels_with_bot_access) == 0:
        return filtered_channels
    return channels_with_bot_access


def exchange_code(client_id, client_secret, code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': callback_url
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


class Multiverse():
    def __init__(self, discord_client_id, discord_client_secret):
        self.discord_client_id = discord_client_id
        self.discord_client_secret = discord_client_secret
        self.mdb = Marvel()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def login_url(self):
        session_id = cherrypy.session.id
        redirect_uri = callback_url
        encoded_uri = urllib.parse.quote_plus(redirect_uri)
        scope = "identify%20guilds%20webhook.incoming"
        scope = "identify%20guilds"
        login_url = "https://discord.com/oauth2/authorize?response_type=code&client_id={}&scope={}&state={}&redirect_uri={}&prompt=consent".format(
            self.discord_client_id,
            scope,
            session_id,
            encoded_uri
        )
        return {"url": login_url}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def channels(self, guild_id):
        user_id = cherrypy.session.get("user_id")
        if not user_id:
            cherrypy.response.status = 401
            return {"error": "Not authorized."}

        channels = get_bot_channels(self.discord_client_id, guild_id)
        channels_info = [{"name": channel["name"], "id": channel["id"]}
                         for channel in channels]
        return {"channels": channels_info}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get(self):
        user_id = cherrypy.session.get("user_id")
        if not user_id:
            cherrypy.response.status = 401
            return {"error": "Not authorized."}
        print("hello", user_id)
        user = self.mdb.get_user(user_id)
        print("hello", user)
        guilds = get_guilds('Bearer', user["access_token"])

        bot_guilds = get_guilds('Bot', token)

        intersection = [guild for guild in guilds if guild["id"]
                        in [bot_guild["id"] for bot_guild in bot_guilds]]
        guilds_info = [{"name": guild["name"], "id": guild["id"]}
                       for guild in intersection]

        first_guild_id = guilds_info[0]["id"]
        channels = get_bot_channels(self.discord_client_id, first_guild_id)
        channels_info = [{"name": channel["name"], "id": channel["id"]}
                         for channel in channels]

        return {"username": user["username"], "guilds": guilds_info, "channels": channels_info}

    @cherrypy.expose
    def callback(self, state, code):
        res = exchange_code(
            self.discord_client_id,
            self.discord_client_secret,
            code
        )

        access_token = res["access_token"]
        expires_in = res["expires_in"]
        refresh_token = res["refresh_token"]
        user = get_user(res["access_token"])
        print("hello 2", user)

        id = user["id"]
        username = user["username"]

        cherrypy.session["user_id"] = id
        user = self.mdb.get_user(id)


        if user == None:
            self.mdb.add_user(id, username, access_token,
                              refresh_token, expires_in)
        else:
            self.mdb.update_user(id, username, access_token,
                                 refresh_token, expires_in)

        raise cherrypy.HTTPRedirect('/web')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def db(self):
        session_id = cherrypy.session.id
        test_value = cherrypy.session.get("test")
        cherrypy.session["test"] = "test"
        return {"session_id": session_id, "test": test_value}
        
        

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def refresh(self):
        session_id = cherrypy.session.id
        user_id = cherrypy.session.get("user_id")
        user = self.mdb.get_user(user_id)

        res = revoke_access_token(
            user.access_token,
            self.discord_client_id,
            self.discord_client_secret
        )

        res = refresh_token(
            user.refresh_token,
            self.discord_client_id,
            self.discord_client_secret
        )

        access_token = res["access_token"]
        expires_in = res["expires_in"]

        username = user.username

        self.mdb.update_user(id, username, access_token,
                             res["refresh_token"], expires_in)

        return {"res": res}

    @cherrypy.expose
    def index(self):
        session_id = cherrypy.session.id
        user_id = cherrypy.session.get("user_id")
        if user_id:
            raise cherrypy.HTTPRedirect('/web')
        else:
            raise cherrypy.HTTPRedirect('/web/login')
