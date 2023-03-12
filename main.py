import json
import os
import openai

openai.organization = os.environ["ORGANIZATION_KEY"]
openai.api_key = os.environ["API_KEY"]

models = openai.Model.list()

def run(text: str) -> None:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    print("Received response:" + json.dumps(response, ensure_ascii=False))
    return response.choices[0].message.content

if __name__ == "__main__":
    text = input('What your question?\n>')
    print(run(text))

