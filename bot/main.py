import discord
import logging

from dotenv import load_dotenv
import os

# logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(level)s] %(name)s : %(message)s' 
)

# load .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
if TOKEN is None:
    logging.error('Token not set')
    raise RuntimeError('Token not set')

# set up logging
handler = logging.StreamHandler()

# bot quickstart
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Bot have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, nerds!')

client.run(TOKEN)
