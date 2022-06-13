from os import getenv
from discord import Client, Intents, Message, TextChannel, Member
from discord.ext import tasks
from datetime import datetime
from requests import head

token = getenv('BOT_TOKEN')
prefix = getenv('BOT_PREFIX') or '!'
api_url = getenv('API_URL')
member_id = getenv('ID_MEMBER')

intents = Intents.default()
intents.members = True
client = Client(intents=intents)


@tasks.loop(minutes=1)
async def task(channel: TextChannel):
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        response = head(api_url)

        if response.status_code == 200:
            await channel.send(f'`[{now}]` Waifuseum api is **up!**')
        else:
            await channel.send(f'`[{now}]` Waifuseum api is **down!**')
    except Exception as e:
        print(e)


@client.event
async def on_message(message: Message):
    if not message.content.startswith(prefix) or message.author.bot:
        return

    (command, *args) = message.content[len(prefix):].split()

    match command.lower():
        case 'ping':
            await message.channel.send('Pong!')
        case 'say':
            await message.channel.send(' '.join(args))
        case 'start':
            if api_url is None:
                return await message.channel.send('`API_URL` is not set!')
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
    if member_id is None:
        return

    role = member.guild.get_role(int(member_id))
    if role is None:
        return

    await member.add_roles(role)


@client.event
async def on_ready():
    print('Discord bot is ready!')

client.run(token)
