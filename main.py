"""DiscordBot"""
import os
# import asyncio
import discord
from dotenv import load_dotenv
from AI_Tools.fran_brain import FranBrain as Fran
# from news import get_news_from_xml
#pylint: disable=W0718

SUMI_ID = 1
fran = Fran()

# Load the environment variables
load_dotenv(dotenv_path='.env.local', override=True)
load_dotenv(dotenv_path='.env', override=False)

discord_api = os.environ.get('DISCORD_API')

# Create a new instance of the Discord and Gpt client
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    """Event handler for when the bot is ready"""
    print('Bot is ready.')

    # Start the task to send message at 9am
    # await discord_client.loop.create_task(check_news())

# Event handler to send message at 9am
# @discord_client.event
# async def check_news():
#     """Send a message if get news from the FFXIV news feed."""
#     # Check every hour
#     await asyncio.sleep(3600)
#     while True:
#         channel = await discord_client.fetch_user(SUMI_ID)
#         today_news = await get_news_from_xml()
#         if today_news:
#             gpt_response = fran.parse_ffxiv_news(today_news)
#             await channel.send(gpt_response)

# Event handler for when a message is received
@discord_client.event
async def on_message(message):
    """Check if the message is from the bot itself to avoid infinite loops"""
    if message.author == discord_client.user:
        return

    if message.author.id != SUMI_ID:
        await message.channel.send("I can't talk to strangers.")
        return

    #checks if the message is an image
    if message.attachments:
        return
        # gpt_response = fran.get_response_for_image(message.attachments[0])
    else:
        gpt_response = fran.get_response_for_text(message.content)
    try:
        await message.channel.send(gpt_response)
    except Exception as e:
        fran.memory_wipe()
        await message.channel.send("I'm sorry, I'm not sure how to respond to that.")
        print(e)

discord_client.run(discord_api)
