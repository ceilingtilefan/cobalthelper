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
            "vt.tiktok.com",
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
        print(urls)
        if urls:
            url = urlparse(urls[0]).hostname
            print(url)
            if url in supportedURL:
                cobalt = requests.post('http://cobalt-api:9000', headers = {"Accept": "application/json", "Content-Type": "application/json"}, json={"url": str(urls[0]).split('||')[0]})
                cobaltJson = json.loads(cobalt.content)
                mediaToSend = []
                if "||" in message.content:
                    spoiler = True
                else:
                    spoiler = False
                if cobaltJson['status'] == 'picker':
                    for each in cobaltJson['picker']:
                        mediaUrl = requests.get(each['url']) 
                        orig_filename = each['url'].split('/')[-1].split('?')[0]
                        filename = f"SPOILER_{orig_filename}" if spoiler else orig_filename
                        media = io.BytesIO(mediaUrl.content)
                        mediaToSend.append(discord.File(media, filename=filename))
                else:
                    print(cobaltJson)
                    mediaUrl = requests.get(cobaltJson['url'])
                    media = io.BytesIO(mediaUrl.content)
                    orig_filename = cobaltJson['filename']
                    filename = f"SPOILER_{orig_filename}" if spoiler else orig_filename
                    mediaToSend.append(discord.File(media, filename=filename))
                await message.reply(files=mediaToSend, mention_author=False) 
                await message.edit(suppress=True)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

token = os.getenv('TOKEN')
client.run(token)