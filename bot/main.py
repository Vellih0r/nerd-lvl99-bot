import discord
import logging
from typing import Optional, Union

from dotenv import load_dotenv
import os
import json
from random import choice

from tictactoe_game import tictactoe, result_to_text, get_game_id

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

def load_json(filename: str) -> Optional[Union[list[dict], dict]]:
    try:
        with open(filename, 'r') as f:
            obj = json.loads(f.read())
            return obj
    except Exception as e:
        logging.error(f'Error loading json={filename} - {e}')
    return None

questions = load_json('json_data/questions.json')
MCQs = load_json('json_data/mcq.json')

# bot quickstart
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Bot have logged in as {client.user}')

# track questions
active_questions = {}
active_mcqs = {}
ttt_games = {}
user_to_gameid = {}

text_to_emoji = {'one': '1️⃣', 'two': '2️⃣', 'three': '3️⃣', 'four': '4️⃣'}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, nerds!')

    if message.content.startswith('!help'):
        pass

    if message.content.startswith('!ttt'):
        if message.author.id in user_to_gameid:
            await message.reply('You are already in a game')
            return
        if len(message.mentions) != 1:
            await message.reply('Command usage: !ttt @user')
            return

        tagged_user = message.mentions[0]
        tagged_user_id = tagged_user.id
        
        id = get_game_id()
        gamedata = tictactoe()
        user_to_gameid[message.author.id] = id
        user_to_gameid[tagged_user_id] = id
        ttt_games[id] = {'x': message.author.id, 'o':tagged_user_id, 'data':gamedata}
        await message.reply(f'Game created!\n{ttt_games[id]['data']['gamefield']}')

    if message.author.id in user_to_gameid:
        id = user_to_gameid[message.author.id]

        if message.content.startswith('!end'):
            game = ttt_games[id]
            del user_to_gameid[game['x']]
            del user_to_gameid[game['o']]
            del ttt_games[id]
            return
        else:
            gd = ttt_games[id]['data']
            if gd['x_turn']:
                if message.author.id == ttt_games[id]['o']:
                    await message.reply("It's ❌ turn! But you play as ⭕")
                    return
                e = '❌'
            else:
                if message.author.id == ttt_games[id]['x']:
                    await message.reply("It's ⭕ turn! But you play as ❌")
                    return
                e = '⭕'

            gd = tictactoe(gd, message.content)
            ttt_games[id]['data'] = gd

            if gd['result'] !=3:
                result = gd['result']
                await message.reply(result_to_text(result))
                del ttt_games[id]
            else:
                await message.reply(gd['text'])
            

    if message.content.startswith('!mcq'):
        try:
            q = choice(MCQs)
            
            logging.debug(f'mcq choosen: {q}')
            content = f'mcq number: {q["number"]}\n'
            content += q["question"]
            content += f'\n```{q["lang"]}\n{q["code"]}```'
            content += f'\n1. {q["one"]}\n2. {q["two"]}\n 3. {q["three"]}\n4. {q["four"]}'
            msg = await message.channel.send(content)
            active_mcqs[msg.id] = (message.author.id, q)
            for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]:
                await msg.add_reaction(emoji)
        except IndexError as e:
            content = 'mcq list is empty. Sorry >_<'
            logging.error(f'Empty mcq list: {e}')
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
    if reaction.message.id in active_mcqs:
        author_id, q = active_mcqs[reaction.message.id]

        if user.id != author_id:
            return
        
        if reaction.emoji == text_to_emoji[q["answer"]]:
            await reaction.message.reply('✅Correct! Good job')
        else:
            await reaction.message.reply(f'❌Wrong... Skill issue detected\n\nExplanation:\n_{q["explanation"]}_\nAnswer: {q['answer']}')

        del active_mcqs[reaction.message.id]

client.run(TOKEN)
