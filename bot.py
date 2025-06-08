import discord # type: ignore
import os
import requests # type: ignore
from urlextract import URLExtract # type: ignore
from urllib.parse import urlparse
import json
import io

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user} using Discord.py version {discord.__version__}')

    async def on_message(self, message):
        supportedURL = [
            "www.tiktok.com",
            "vm.tiktok.com",
            "www.instagram.com",
            "twitter.com",
            "x.com",
            "www.reddit.com",
            "bsky.app",
            "www.facebook.com",
            "www.snapchat.com",
            "www.tumblr.com",
            "www.twitch.tv"
        ]

        urls = URLExtract().find_urls(message.content)
        if urls:
            url = urlparse(urls[0]).hostname
            if url in supportedURL:
                cobalt = requests.post('http://cobalt-api:9000', headers = {"Accept": "application/json", "Content-Type": "application/json"}, json={"url": str(urls[0])})
                videoUrl = requests.get(json.loads(cobalt.content)['url'])
                videoToSend = io.BytesIO(videoUrl.content)
                await message.reply(file=discord.File(videoToSend, 'video.mp4'), mention_author=False)
                await message.edit(suppress=True)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

token = os.getenv('TOKEN')
client.run(token)