from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI
from handlers import (
    start,
    help_command,
    add_channel,
    list_channels,
    set_caption,
    set_button,
    handle_private_message,
    channel_details,
    edit_caption,
    edit_button,
    remove_channel,
    back_to_menu,
    handle_channel_message
)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client['telegram_bot']
channels_collection = db['channels']
app = Client("custom_caption_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_states = {}

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await start(client, message)

@app.on_message(filters.command("help"))
async def help_command_handler(client, message):
    await help_command(client, message)

@app.on_message(filters.command("add"))
async def add_channel_handler(client, message):
    await add_channel(client, message)

@app.on_message(filters.command("channels"))
async def list_channels_handler(client, message):
    await list_channels(client, message)

@app.on_message(filters.command("set_caption"))
async def set_caption_handler(client, message):
    await set_caption(client, message)

@app.on_message(filters.command("set_button"))
async def set_button_handler(client, message):
    await set_button(client, message)

@app.on_message(filters.text & filters.private)
async def handle_private_message_handler(client, message):
    await handle_private_message(client, message)

@app.on_callback_query(filters.regex(r"channel_(.*)"))
async def channel_details_handler(client, callback_query):
    await channel_details(client, callback_query)

@app.on_callback_query(filters.regex(r"edit_caption_(.*)"))
async def edit_caption_handler(client, callback_query):
    await edit_caption(client, callback_query)

@app.on_callback_query(filters.regex(r"edit_button_(.*)"))
async def edit_button_handler(client, callback_query):
    await edit_button(client, callback_query)

@app.on_callback_query(filters.regex(r"remove_channel_(.*)"))
async def remove_channel_handler(client, callback_query):
    await remove_channel(client, callback_query)

@app.on_callback_query(filters.regex(r"back_to_menu"))
async def back_to_menu_handler(client, callback_query):
    await back_to_menu(client, callback_query)

@app.on_message(filters.channel)
async def handle_channel_message_handler(client, message):
    await handle_channel_message(client, message)

if __name__ == "__main__":
    app.run()
