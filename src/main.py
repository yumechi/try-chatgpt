from speaker.metan import Metan
import json
import os
import openai
import time
import unicodedata

openai.organization = os.environ["ORGANIZATION_KEY"]
openai.api_key = os.environ["API_KEY"]


def get_current_timestamp() -> str:
    return str(round(time.time() * 1000))


def get_temp_filename() -> str:
    # TODO: こちらから注入すべきかは悩ましい
    return get_current_timestamp() + ".wav"

def remove_control_characters(s):
    # refer: https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def safety_input(title: str) -> str:
    while True:
        try:
            t = input(title)
            return remove_control_characters(t)
        except:
            pass
    raise Exception("Not reach this line")

def run(text: str) -> None:
    message_stack = [
        {
            "role": "user",
            "content": text,
        },
    ]
    while text:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_stack,
        )
        openai_message = response.choices[0].message.content
        metan = Metan(style=0)
        metan.play_sound(openai_message, get_temp_filename())
        text = safety_input(
            "What is your next step? (If you are finished talking, please type 'quit'.)\n> "
        )
        if text == "quit":
            break
        message_stack.extend(
            [
                {
                    "role": "system",
                    "content": openai_message,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ]
        )


if __name__ == "__main__":
    text = safety_input("What is your question ?\n> ")
    run(text)
