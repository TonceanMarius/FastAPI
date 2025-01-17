from openai import OpenAI,OpenAIError
import os
import logging
from dotenv import load_dotenv

api = os.getenv("OPEN_API_KEY")
OpenAI.api_key = api

from openai import OpenAI, OpenAIError

def dalle(user_prompt: str):
    client = OpenAI()

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=user_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except OpenAIError.InvalidRequestError as e:
        print(f"Invalid request error: {e}")
        return None
    except OpenAIError as e:
        print(f"An error occurred: {e}")
        return None


def chatgpt(user_prompt):

    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a creative assistant helping refine image prompts for AI-generated art."},
        {"role": "user", "content": f"Refine this prompt for a DALLE-E image: {user_prompt}"}
    ]
    )
    
    return completion.choices[0].message.content