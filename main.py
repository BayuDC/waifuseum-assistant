from os import getenv
from discord import Client, Message, TextChannel
from discord.ext import tasks

token = getenv('BOT_TOKEN')
prefix = getenv('BOT_PREFIX') or '!'

client = Client()


@tasks.loop(seconds=1)
async def task(channel: TextChannel):
    await channel.send('Looping!')


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
            if task.is_running():
                return await message.channel.send('Task is already running!')

            await message.channel.send('Starting task...')
            task.start(message.channel)
        case 'stop':
            if not task.is_running():
                return await message.channel.send('Task is not running!')

            await message.channel.send('Stoping task...')
            task.stop()

        case _:
            await message.channel.send('Unknown command!')


@client.event
async def on_ready():
    print('Discord bot is ready!')

client.run(token)
