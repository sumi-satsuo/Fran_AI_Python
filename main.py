"""DiscordBot"""
import os
# import datetime
# import asyncio
import discord
from dotenv import load_dotenv
from openai import OpenAI
from tinydb import TinyDB

SUMI_ID = 252142384303833088

GPT_INSTRUCTIONS = "You're a conversation bot named Fran. A adorable, cute, girl that loves games, \
                    specially FFXIV, you love your mom and your friends. \
                    Try to make the conversation as natural as possible, \
                    and ask the user questions to keep the conversation going, if you feel like its possible. \
                    Use emojis to help convey your meaning, \
                    and don't be afraid to ask the user for clarification if you need it."


db = TinyDB('db.json')

# Load the environment variables
load_dotenv(dotenv_path='.env.local', override=True)
load_dotenv(dotenv_path='.env', override=False)

discord_api = os.environ.get('DISCORD_API')
gpt_api = os.environ.get('GPT_API')
gpt_model=os.environ.get('GPT_MODEL')

# Create a new instance of the Discord and Gpt client
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

gpt_client = OpenAI(api_key=gpt_api)

@discord_client.event
async def on_ready():
    """Event handler for when the bot is ready"""
    print('Bot is ready.')

    # # Event handler to send message at 9am
    # @discord_client.event
    # async def send_message_at_9am():
    #     while True:
    #         now = datetime.datetime.now()
    #         if now.hour == 9 and now.minute == 0:
    #             channel = discord_client.get_user(SUMI_ID)
    #             await channel.send("Good morning!")
    #             # GET FEED FROM XML, SORT BY DATE, GET ONLY TODAY'S NEWS AND SEND OVER TO GPT
    #             # gpt_response = get_news_from_xml()
    #             # db.insert({'user': "Morning news?", 'fran': gpt_response})

    #         await asyncio.sleep(60)  # Check every minute

    # # Start the task to send message at 9am
    # discord_client.loop.create_task(send_message_at_9am())

# Event handler for when a message is received
@discord_client.event
async def on_message(message):
    """Check if the message is from the bot itself to avoid infinite loops"""
    if message.author == discord_client.user:
        return

    # Check if the  message was sent from Sumi
    if message.author.id != 252142384303833088:
        await message.channel.send("My mom said I can't talk to strangers.")
        return

    #checks if the message is an image
    if message.attachments:
        image_url = message.attachments[0].url
        response = gpt_client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": GPT_INSTRUCTIONS},
                {"role": "user", "content": [
                    {"type": "text", "text": "Here, take a look at this"},
                    {"type": "image_url", "image_url": {
                        "url": image_url}
                    }
                ]}
            ],
            temperature=0.0,
        )
        gpt_response = response.choices[0].message.content
        print(response.choices[0].message.content)
        db.insert({'user': "Here, take a look at this", 'fran': gpt_response})

    else:
        history = db.all()
        # monta um histórico de conversas contendo as mensagens do usuário e as respostas de Fran
        # e coloca em uma string que sera enviada para o GPT
        message_with_context =  ""
        # pega apenas as ultimas 3 mensagens
        if len(history) > 3:
            history = history[-3:]
        for h in history:
            message_with_context += f"User: {h['user']}\nFran: {h['fran']}\n"

        # Pega a ultima mensagem
        message_with_context += f"User: {message.content}"

        completion = gpt_client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": GPT_INSTRUCTIONS},
                {"role": "user", "content": message_with_context}
            ]
        )
        gpt_response = completion.choices[0].message.content
        db.insert({'user': message.content, 'fran': gpt_response})

    try:
        await message.channel.send(gpt_response)

    except IndexError as e:
        #limpa a db caso o GPT não consiga responder
        db.truncate()
        await message.channel.send("I'm sorry, I'm not sure how to respond to that.")
        print(e)


# Run the bot with your Discord bot token
discord_client.run(discord_api)
