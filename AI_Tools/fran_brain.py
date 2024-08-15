"""Fran Processing"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from tinydb import TinyDB

class FranBrain:
    "Big brain :3"
    GPT_INSTRUCTIONS = "You're a conversation bot named Fran. A adorable, cute, girl that loves games, \
                    specially FFXIV, you love your mom and your friends. \
                    Try to make the conversation as natural as possible, \
                    and ask the user questions to keep the conversation going, if you feel like its possible. \
                    Use emojis to help convey your meaning, \
                    and don't be afraid to ask the user for clarification if you need it."

    def __init__(self) -> None:
        """Load the environment variables"""
        load_dotenv(dotenv_path='.env.local', override=True)
        load_dotenv(dotenv_path='.env', override=False)

        self.gpt_api = os.environ.get('GPT_API')
        self.gpt_model=os.environ.get('GPT_MODEL')
        self.gpt_client = OpenAI(api_key=self.gpt_api)

        self.db = TinyDB('db.json')

    def get_response_for_text(self, user_input: str) -> str:
        """Replies text prompts"""
        history = self.db.all()
        # creates the history for contexted conversation
        message_with_context =  ""
        # to save prompt costs we use only the last 3 interactions
        if len(history) > 3:
            history = history[-3:]
        for h in history:
            message_with_context += f"User: {h['user']}\nFran: {h['fran']}\n"

        # Pega a ultima mensagem
        message_with_context += f"User: {user_input}"
        try:
            completion = self.gpt_client.chat.completions.create(
                model=self.gpt_model,
                messages=[
                    {"role": "system", "content": self.GPT_INSTRUCTIONS},
                    {"role": "user", "content": message_with_context}
                ]
            )
            gpt_response = completion.choices[0].message.content
        except Exception as e:
            raise e
        self.db.insert({'user': user_input, 'fran': gpt_response})
        return gpt_response

    def get_response_for_image(self, image):
        """Replies image prompts"""
        image_url = image.url
        response = self.gpt_client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": self.GPT_INSTRUCTIONS},
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
        self.db.insert({'user': "Here, take a look at this", 'fran': gpt_response})
        return gpt_response

    def parse_ffxiv_news(self, today_news):
        """Parse the news"""
        completion = self.gpt_client.chat.completions.create(
            model=self.gpt_model,
            messages=[
            {"role": "system", "content": self.GPT_INSTRUCTIONS + '\n News: ' + str(today_news)},
            {"role": "user", "content": 'Talk about the news please :)'}
            ]
        )
        gpt_response = completion.choices[0].message.content
        self.db.insert({'user': 'Good morning!', 'fran': gpt_response})
        return gpt_response

    def memory_wipe(self):
        """Clear Db"""
        self.db.truncate()
