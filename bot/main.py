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
MSQs = []
try:
    with open('questions.json', 'r') as f:
        json_data = f.read()
        questions = json.loads(json_data)
except Exception as e:
    logging.error(f'Error loading json: {e}')

try:
    with open('msq.json', 'r') as f:
        json_data = f.read()
        MSQs = json.loads(json_data)
except Exception as e:
    logging.error(f'Error loading json: {e}')

# bot quickstart
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Bot have logged in as {client.user}')

# track questions
active_questions = {}
active_msqs = {}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, nerds!')

    if message.content.startswith('!help'):
        pass

    if message.content.startswith('!mcq'):
        try:
            q = choice(MSQs)
            active_msqs[message.id] = (message.author.id, q)
            logging.debug(f'msq choosen: {q}')
            content = f'msq number: {q["number"]}\n'
            content += q["question"]
            content += f'\n```{q["lang"]}\n{q["code"]}```'
            content += f'\n1. {q["one"]}\n2. {q["two"]}\n 3. {q["three"]}\n4. {q["four"]}'
            msg = await message.channel.send(content)
            for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]:
                await msg.add_reaction(emoji)
        except IndexError as e:
            content = 'msq list is empty. Sorry >_<'
            logging.error(f'Empty msq list: {e}')
            await message.channel.send(content)
        except Exception as e:
            content = 'Unknown error o_O'
            logging.error(f'Error asking question: {e}')
            await message.channel.send(content)

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
            logging.error(f'Empty question list: {e}')
        except Exception as e:
            content = 'Unknown error o_O'
            logging.error(f'Error asking question: {e}')
        finally:
            await message.channel.send(content)

    if message.author.id in active_questions:
        q = active_questions[message.author.id]
        if message.content.lower() == q["answer"]:
            await message.reply('✅Correct! Good job')
        else:
            await message.reply(f'❌Wrong... Skill issue detected\n\nExplanation:\n_{q["explanation"]}_')

        del active_questions[message.author.id]

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    if reaction.message.id in active_msqs:
        author_id, q = active_msqs[reaction.message.id]

        if user.id != author_id:
            return
    
        if reaction.emoji.name == q["answer"]:
            await reaction.message.reply('✅Correct! Good job')
        else:
            await reaction.message.reply(f'❌Wrong... Skill issue detected\n\nExplanation:\n_{q["explanation"]}_')

        del active_msqs[user.id]


client.run(TOKEN)
