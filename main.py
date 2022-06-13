from os import getenv
from discord import Client, Message

token = getenv('BOT_TOKEN')
prefix = getenv('BOT_PREFIX') or '!'

client = Client()


@client.event
async def on_ready():
    print('Discord bot is ready!')


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
        case _:
            await message.channel.send('Unknown command!')


client.run(token)
