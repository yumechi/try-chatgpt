from speaker.metan import Metan
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


def remove_control_characters(s) -> str:
    # refer: https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")


def safety_input(title: str) -> str:
    while True:
        try:
            t = input(title)
            return remove_control_characters(t)
        except:  # noqa: E722
            pass
    raise Exception("Not reach this line")

def request_openai(message_stack: list[str]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_stack,
    )
    content = response.choices[0].message.content
    return content.strip()

def run(text: str) -> None:
    message_stack = [
        {
            "role": "user",
            "content": text,
        },
    ]
    while text:
        openai_message = request_openai(message_stack)
        try:
            metan = Metan(style=0)
            metan.play_sound(openai_message, get_temp_filename())
        except:  # noqa: E722
            # if voicevox does not work...
            print(f"system answer:\n{openai_message}")
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
