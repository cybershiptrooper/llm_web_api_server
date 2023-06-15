from . import *
import concurrent.futures

def post_to_gpt(prompt):
    """
    Post a prompt to the GPT-3 API and return the response.
    """
    gpt_request = {
        "engine": "text-davinci-003",
        "temperature": 0.2,
        "max_tokens": 3600,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "prompt": prompt,
    }

    return openai.Completion.create(**gpt_request)


def post_to_dalle(prompt):
    """
    Post a prompt to the DALL-E API and return the response.
    """
    dalle_request = {
        "prompt": prompt,
        "num_return_sequences": 1,
        "size": "256x256",
    }

    return openai.Image.create(**dalle_request)[0]['url']

def post_to_dalle_dummy(prompts: list[str]) -> list[str]:
    return "https://www.w3schools.com/images/picture.jpg"

def post_to_dalle_parallel(prompts: list[str]) -> list[str]:
    # use multithreading to call dalle api in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(post_to_dalle_dummy, prompts)
    return list(results)