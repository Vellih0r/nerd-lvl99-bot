import discord
import logging

from dotenv import load_dotenv
import os
import json
from random import choice

# logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s : %(message)s' 
)

# load .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
if TOKEN is None:
    logging.error('Token not set')
    raise RuntimeError('Token not set')

# load .json
questions = []
try:
    with open('questions.json', 'r') as f:
        json_data = f.read()
        questions = json.loads(json_data)
        f.close()
except Exception as e:
    logging.error("Error loading json: ", e)

# set up logging
handler = logging.StreamHandler()

# bot quickstart
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Bot have logged in as {client.user}')

# track questions
active_questions = {}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id in active_questions:
        q = active_questions[message.author.id]
        if message.content.lower() == q["answer"]:
            await message.reply('✅Correct! Good job')
        else:
            await message.reply("❌Wrong... Skill issue detected")

        del active_questions[message.author.id]

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, nerds!')

    if message.content.startswith('!challenge'):
        try:
            q = choice(questions)
            active_questions[message.author.id] = q
            logging.debug(f'Question choosen: {q}')
            content = f'Question number: {q["number"]}\n'
            content += q["question"]
            content += f'\n```{q["lang"]}\n{q["code"]}```'
        except IndexError as e:  
            content = 'Question list is empty. Sorry >_<'
            logging.error('Empty question list:', e)
        except Exception as e:
            content = 'Unknown error o_O'
            logging.error('Error asking question:', e)
        finally:
            await message.channel.send(content)

client.run(TOKEN)
