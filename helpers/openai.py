import openai
import os

from openai import OpenAI, AsyncOpenAI

from configs import openai_key


async def query_openai_api(prompt: str):

    client = AsyncOpenAI(
        api_key=openai_key,
    )

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].text.strip()

# Пример использования:
# print(query_openai_api("Translate the following English text to French: '{}'.format('Hello, world!')"))
