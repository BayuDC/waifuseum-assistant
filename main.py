from discord import Client, Intents, Message, Embed, TextChannel, Member, Color
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
            embed = Embed(colour=Color.from_rgb(24, 116, 152), title=':ping_pong: Pong!', description=f'Ping Latency : {client.latency}s')
            await message.channel.send(embed=embed)
        case 'say':
            await message.channel.send(' '.join(args))
        case 'start':
            if task.is_running():
                embed = Embed(colour=Color.from_rgb(249, 217, 35), description=':warning: Task is already running!')
                return await message.channel.send(embed=embed)

            embed = Embed(colour=Color.from_rgb(54, 174, 124), description=':white_check_mark: Starting task...')
            await message.channel.send(embed=embed)
            task.start(message.channel)
        case 'stop':
            if not task.is_running():
                embed = Embed(colour=Color.from_rgb(235, 83, 83), description=':x: Task is not running!')
                return await message.channel.send(embed=embed)

            embed = Embed(colour=Color.from_rgb(54, 174, 124), description=':white_check_mark: Stoping task...')
            await message.channel.send(embed=embed)
            task.stop()
        case 'status':
            await task(message.channel)
        case _:
            embed = Embed(colour=Color.from_rgb(235, 83, 83), description=':x: Unknown command!')
            await message.channel.send(embed=embed)


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
