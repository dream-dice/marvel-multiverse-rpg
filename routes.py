import asyncio

import cherrypy


async def send_message(client, channel_id, message):
    channel = client.get_channel(channel_id)
    await channel.send(message)


class D616():
    def __init__(self, client):
        self.client = client

    def reply(self):
        asyncio.run_coroutine_threadsafe(
            self.send_message(self.client, 1090624671881363500, 'Hello'),
            self.client.loop
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        self.reply()
        return {"a": 1}
