from . import *
import concurrent.futures
import requests

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

def post_to_gpt_firefall(prompt):
    """
    Post a prompt to the GPT-3 API and return the response.
    """
    print(prompt)
    gpt_request = {
        "dialogue":{
            "question": prompt
        },
        "llm_metadata": {
            "model_name": "gpt-4-32k",
            "temperature": 0.2,
            "max_tokens": 30000,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "n": 1,
            "llm_type": "azure_chat_openai"
        }
    }

    url = "<TOFILL>"
    
    headers = {
        "x-gw-ims-org-id": "<TOFILL>",
        "x-api-key": "<TOFILL>", 
        "Authorization": "<TOFILL>",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=gpt_request, headers=headers)
    print (response.content)
    return response

def post_to_gpt_azure(prompt):
    """
    Post a prompt to the GPT-4-32k API and return the response.
    """
    print(prompt)

    gpt_request = {
        "messages": [{"role":"user","content": prompt}],
        "max_tokens": 18000,
        "temperature": 0.3,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "top_p": 1.0,
        "stop": None
    }
    url = "<TOFILL>"
    
    headers = {
        "api-key": "<TOFILL>", 
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=gpt_request, headers=headers)
    print (response.content)
    return response

def post_to_dalle(prompt):
    """
    Post a prompt to the DALL-E API and return the response.
    """
    dalle_request = {
        "prompt": prompt,
        "n": 1,
        "size": "256x256",
    }
    print(dalle_request)
    return openai.Image.create(**dalle_request)['data'][0]['url']

def post_to_dalle_dummy(prompts: list[str]) -> list[str]:
    return "https://www.w3schools.com/images/picture.jpg"

def post_to_dalle_parallel(prompts: list[str]) -> list[str]:
    # use multithreading to call dalle api in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(post_to_dalle, prompts)
    return list(results)