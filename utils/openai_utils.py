from . import *

def post_to_gpt(prompt):
    """
    Post a prompt to the GPT-3 API and return the response.
    """
    gpt_request = {
        "engine": "text-davinci-003",
        "temperature": 0.2,
        "max_tokens": 2000,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "prompt": prompt,
    }

    return openai.Completion.create(**gpt_request)