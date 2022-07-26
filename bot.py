from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY', 'b98b83211a6398f434379ce1b98e45af81e484b7')
SITE_API_URL = environ.get('SITE_API_URL')

bot = Client('ShortLinkBot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Greetins!!💛{message.chat.first_name}!**\n\n"
        "I am Shortest Link Bot. Send Me Any Long Link, I Will Convert It into Short Link. This bot uses your account's API key.\n\n Meet my master @master_sergio💖\n")


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(f'Here Is Your ➤ ({short_link})')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = SITE_API_URL
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()
