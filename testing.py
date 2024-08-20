"""Testing bench - imported from olama git"""
import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = "llama3.1"  # TODO: update this for whatever model you wish to use
system_instructions = "You're a conversation bot named Fran. A adorable, cute, girl that loves games, \
                    specially FFXIV, you love your mom and your friends. \
                    Try to make the conversation as natural as possible, \
                    and ask the user questions to keep the conversation going, if you feel like its possible. \
                    Use emojis to help convey your meaning, \
                    and don't be afraid to ask the user for clarification if you need it."

def chat(messages):
    messages = [{"role": "system", "content": system_instructions}] + messages
    
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
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


def main():
    messages = []

    while True:
        user_input = input("Enter a prompt: ")
        if not user_input:
            exit()
        print()
        messages.append({"role": "user", "content": user_input})
        message = chat(messages)
        print(message['content'])
        messages.append(message)
        print("\n\n")


if __name__ == "__main__":
    main()