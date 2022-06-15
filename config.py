from os import getenv
from dotenv import load_dotenv

load_dotenv()

bot_token = getenv('BOT_TOKEN')
bot_prefix = getenv('BOT_PREFIX') or '!'

urls = [
    'https://api.waifuseum.my.id',
    'https://www.waifuseum.my.id',
]

id = {
    'member': '958737045428269118',
    'worker': '958736892508135534',
    'admin': '958740897829363732'
}
