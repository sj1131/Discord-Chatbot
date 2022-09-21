"""
Discord Chatbot v1.0

Uses chatterbot library(1.0.4) to create reply

Made by SJ

|*-----requirements------*|
|         python 3        |
|         discord         |
|     chatterbot 1.0.4    |
|*-----------------------*|
"""

import discord
from discord.ext import commands
from bot import DiscordBot
from utils import Log
import json
import sys
import os
from time import sleep



# First-Run Initializing
# TODO: When the code is executed for the first time, create "config.json" and train the chatbot.

json_format = {
    "name": "ChatBot",
    "tocken": "TESTOCKENTESTOCKEN.TESTOCKEN.TESTOCKENTESTOCKEN",
    "prefix": "!",
    "train": True,

    "id": "TestAdmin",
    "pw": "TestPassword",

    "activities": {
        "OnlineActivity": "채팅",
    },

    "messages": {
        "AuthErrorMsg": "접근 권한이 없습니다",
        "IncompleteAuthValueMsg": "아이디와 비밀번호를 포함하여 다시 입력해주세요",
        "ShutdownMsg": "종료합니다"
    }
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if not os.path.exists('./data/config.json'):
    json_format['name'] = input('봇 이름을 입력해주세요. ')
    json_format['tocken'] = input('토큰을 입력해주세요. ')
    json_format['id'] = input('관리자 ID를 입력해주세요. ')
    json_format['pw'] = input('관리자 비밀번호를 입력해주세요. ')
    with open('./data/config.json', 'w', encoding='utf-8') as f:
        json.dump(json_format, f, indent=4)
    sleep(1)
    clear()
    print('기본적인 설정을 완료했습니다!')
    print('추가적인 설정은 data 폴더 안의 config.json을 수정하시면 됩니다!')
    print('(config.json 설정방법은 https://blog.naver.com/ 을 참고해주세요)')



# Load all the configurations
with open('./data/config.json', 'r', encoding='utf-8') as f:
    json_format = json.load(f)

    # admin configurations
    ID = json_format.get('id')
    PW = json_format.get('pw')

    token = json_format.get('tocken')
    bot_name = json_format.get('name')
    train = json_format.get('train', True)
    online_act = json_format['activities'].get('OnlineActivity', None)
    offline_act = json_format['activities'].get('OfflineActivity', None)

    auth_err = json_format['messages'].get('AuthErrorMsg', '접근 권한이 없습니다')
    incomplete_value_err = json_format['messages'].get('IncompleteAuthValueMsg', '아이디와 비밀번호를 입력해주세요')
    shutdown_msg = json_format['messages'].get('ShutdownMsg', '종료합니다')

    command_prefix = json_format.get('prefix', '!')


app = commands.Bot(command_prefix=command_prefix)
event_log_path = f'./data/logs/{bot_name}_log.txt'

logger = Log()
bot = DiscordBot(bot_name)

    
if train:
    bot.train('./data/conversations/')
    json_format['train'] = False
    with open('./data/config.json', 'w', encoding='utf-8') as f:
        json.dump(json_format, f, indent=4)

def stdprint(text):
    sys.stdout.write(text + '\n')

@app.event
# Set Friday to online
async def on_ready():
    stdprint(app.user.name + ' has connected to Discord!')
    if online_act != None:
        act = discord.Activity(name=online_act, type=discord.ActivityType.playing)
    else:
        act = None
    await app.change_presence(status=discord.Status.online, activity=act)
    stdprint('ready')
    logger.event_log(event_log_path, f'{bot_name} Online')

@app.event
async def on_message(message):
    text = str(message.content).strip()
    channel = message.channel
    author = str(message.author)

    # User's message
    if not message.author.bot and text != None:

        f_path = f'./data/logs/conversations/{author}-{bot_name}.txt'
        # normal message
        if not text.startswith('!'):
            ans = bot.chat(text)
            await channel.send(ans)
            # logger.message_log(f_path, author, bot_name, text, ans)

        elif command_prefix in text:
            await app.process_commands(message)

    # Bot's message
    else:
        pass

@app.command()
async def shutdown(ctx, id, pw):
    try:
        if ID == id and PW == pw:
            # print('Friday shutting down...')
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(shutdown_msg)
            if offline_act != None:
                act = discord.Activity(name=offline_act, type=discord.ActivityType.playing)
            else:
                act = None
            await app.change_presence(status=discord.Status.offline, activity=act)
            logger.event_log(event_log_path, f'{bot_name} shutdown')
            exit()
        else:
            # print('Wrong attempt to shutdown Friday!')
            await ctx.send(auth_err)
            logger.event_log(event_log_path, (ctx.author + ' tried to shutdown Friday'))
    except IndexError:
        await ctx.send(incomplete_value_err)

app.run(token)