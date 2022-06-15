from discord import Client, Intents, Message, TextChannel, Member
from discord.ext import tasks
from datetime import datetime
from requests import head
from config import *


intents = Intents.default()
intents.members = True
client = Client(intents=intents)


@tasks.loop(minutes=1)
async def task(channel: TextChannel):
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        for url in urls:
            response = head(url)
            await channel.send(f'`[{now}]` `{url}` **{response.reason}**')
    except Exception as e:
        print(e)


@client.event
async def on_message(message: Message):
    if not message.content.startswith(bot_prefix) or message.author.bot:
        return

    (command, *args) = message.content[len(bot_prefix):].split()

    match command.lower():
        case 'ping':
            await message.channel.send('Pong!')
        case 'say':
            await message.channel.send(' '.join(args))
        case 'start':
            if task.is_running():
                return await message.channel.send('Task is already running!')

            await message.channel.send('Starting task...')
            task.start(message.channel)
        case 'stop':
            if not task.is_running():
                return await message.channel.send('Task is not running!')

            await message.channel.send('Stoping task...')
            task.stop()
        case 'status':
            await task(message.channel)
        case _:
            await message.channel.send('Unknown command!')


@client.event
async def on_member_join(member: Member):
    if id['member'] is None:
        return

    role = member.guild.get_role(id['member'])
    if role is None:
        return

    await member.add_roles(role)


@client.event
async def on_ready():
    print('Discord bot is ready!')

client.run(bot_token)
