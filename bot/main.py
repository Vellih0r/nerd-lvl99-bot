import discord
import logging

from dotenv import load_dotenv
import os

# load .env
load_dotenv()
TOKEN = os.getenv('TOKEN')

# set up logging
os.makedirs('logs')
handler = logging.FileHandler('logs/discord.log', encoding='utf-8', mode='w')

# bot quickstart
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Bot have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, nerds!')

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
