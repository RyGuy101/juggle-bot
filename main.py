#!/usr/bin/env python3

import discord
import requests
import validators
import io
from html.parser import HTMLParser

class ImgFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img_src = None

    def handle_starttag(self, tag, attrs):
        if self.img_src is None and tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.img_src = attr[1]
                    break

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = '!juggle'
    if message.content.startswith(command):
        try:
            jugglinglab_url = message.content[len(command):].strip()
            if not validators.url(jugglinglab_url):
                jugglinglab_url = "https://jugglinglab.org/anim?pattern=" + jugglinglab_url
            img_finder = ImgFinder()
            img_finder.feed(requests.get(jugglinglab_url).text)
            await message.channel.send(file=discord.File(io.BytesIO(requests.get(img_finder.img_src).content), filename="anim.gif"))
        except Exception as e:
            print(e)

from client_secret import CLIENT_SECRET
client.run(CLIENT_SECRET)
