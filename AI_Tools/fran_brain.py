"""Fran Processing"""
import json
import requests
from tinydb import TinyDB
# pylint: disable=W0719

class FranBrain:
    "Big brain :3"


    def __init__(self) -> None:
        """Load the environment variables"""

        self.model = "llama3.1"
        self.system_instructions = "You're a conversation bot named Fran. A adorable, cute, girl that loves games, \
                        Try to make the conversation as natural as possible, \
                        and ask the user questions to keep the conversation going, if you feel like its possible. \
                        Use emojis to help convey your meaning, \
                        and don't be afraid to ask the user for clarification if you need it."

        self.db = TinyDB('db.json')

    def chat(self, messages):
        """Chat with ollama"""
        messages = [{"role": "system", "content": self.system_instructions}] + messages

        r = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": self.model, "messages": messages, "stream": True},
        stream=True,
        timeout=30
        )
        r.raise_for_status()
        output = ""

        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])

            if body.get("done") is False:
                message = body.get("message", "")
                content = message.get("content", "")
                output += content
                # the response streams one token at a time, print that as we receive it
                # print(content, end="", flush=True)

            if body.get("done", False):
                message["content"] = output
                return message

    def get_response_for_text(self, user_input: str) -> str:
        """Parse the text, manages the db and ask the AI for the response to provide"""
        history = self.db.all()
        # creates the history for contexted conversation
        messages =  []
        # to save prompt costs we use only the last 3 interactions
        if len(history) > 3:
            history = history[-3:]
        for message in history:
            messages.append(message)

        parsed_message_from_discord = [{"role": "user", "content": user_input}]
        try:
            message = self.chat(parsed_message_from_discord)
            self.db.insert(message)
            response = message['content']
        except Exception as e:
            raise e
        return response

    # def parse_ffxiv_news(self, today_news):
    #     """Parse the news"""
    #     completion = self.gpt_client.chat.completions.create(
    #         model=self.gpt_model,
    #         messages=[
    #         {"role": "system", "content": self.GPT_INSTRUCTIONS + '\n News: ' + str(today_news)},
    #         {"role": "user", "content": 'Talk about the news please :)'}
    #         ]
    #     )
    #     gpt_response = completion.choices[0].message.content
    #     self.db.insert({'user': 'Good morning!', 'fran': gpt_response})
    #     return gpt_response

    def memory_wipe(self):
        """Clear Db"""
        self.db.truncate()
