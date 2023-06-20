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

    url = "https://firefall-stage.adobe.io/v1/completions"
    
    headers = {
        "x-gw-ims-org-id": "dc",
        "x-api-key": "dc-stage-virgoweb", 
        "Authorization": "Bearer " + "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktYXQtMS5jZXIiLCJraWQiOiJpbXNfbmExLXN0ZzEta2V5LWF0LTEiLCJpdHQiOiJhdCJ9.eyJpZCI6IjE2ODcyNjQ1Nzg4ODZfYzc3OGM3MDMtYmFjYS00YzZmLWE5NDAtY2ViZGI3NjZhNDFjX3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJkYy1zdGFnZS12aXJnb3dlYiIsInVzZXJfaWQiOiJDNTA3NTAxODYwRjlDNTg4MEE0OTQxMDhAYzYyZjI0Y2M1YjViN2UwZTBhNDk0MDA0IiwiYXMiOiJpbXMtbmExLXN0ZzEiLCJhYV9pZCI6IkM1MDc1MDE4NjBGOUM1ODgwQTQ5NDEwOEBjNjJmMjRjYzViNWI3ZTBlMGE0OTQwMDQiLCJjdHAiOjAsImZnIjoiWFJMTko2UjQ2UjJYQTREWjdHWk1BMklBMkE9PT09PT0iLCJzaWQiOiIxNjg3MTc3MTk2OTIxX2M3ZDY1YzBhLTcwZjUtNDcwOC1hMDhiLWY3YzEwOTI3NmE3Yl91ZTEiLCJtb2kiOiJlZDIwYTMyMSIsInBiYSI6Ik1lZFNlY0VWRSxMb3dTZWMsTWVkU2VjLE1lZFNlY05vRVYiLCJleHBpcmVzX2luIjoiODY0MDAwMDAiLCJzY29wZSI6IkFkb2JlSUQsb3BlbmlkLERDQVBJLGFkZGl0aW9uYWxfaW5mby5hY2NvdW50X3R5cGUsYWRkaXRpb25hbF9pbmZvLm9wdGlvbmFsQWdyZWVtZW50cyxhZ3JlZW1lbnRfc2lnbixhZ3JlZW1lbnRfc2VuZCxzaWduX2xpYnJhcnlfd3JpdGUsc2lnbl91c2VyX3JlYWQsc2lnbl91c2VyX3dyaXRlLGFncmVlbWVudF9yZWFkLGFncmVlbWVudF93cml0ZSx3aWRnZXRfcmVhZCx3aWRnZXRfd3JpdGUsd29ya2Zsb3dfcmVhZCx3b3JrZmxvd193cml0ZSxzaWduX2xpYnJhcnlfcmVhZCxzaWduX3VzZXJfbG9naW4sc2FvLkFDT01fRVNJR05fVFJJQUwsZWUuZGN3ZWIsdGtfcGxhdGZvcm0sdGtfcGxhdGZvcm1fc3luYyxhYi5tYW5hZ2UsYWRkaXRpb25hbF9pbmZvLmluY29tcGxldGUsYWRkaXRpb25hbF9pbmZvLmNyZWF0aW9uX3NvdXJjZSx1cGRhdGVfcHJvZmlsZS5maXJzdF9uYW1lLHVwZGF0ZV9wcm9maWxlLmxhc3RfbmFtZSIsImNyZWF0ZWRfYXQiOiIxNjg3MjY0NTc4ODg2In0.UIZoFX9_CtKLgKfTsiKiSpLBqshVfPO95WEA2f5-Dd_iXZ6ULT_N8ShyxiSPmnH_suZG_-Jq-EgmP5uiYBH-S3X0dR9DJaWlU3Rl7ssib9GfxRJlcf9dnOcHA2oYsxuoeOOi2WwKFUljUviNkI193CF9wzntkVMKsLPyAWZiXN7qeCbsHRDO_sAL1nBCjj1QKspc08ZmlUYLuF_-fccOx2uKlNDn8SoMdWJvhVP19iEWsuO7VlHTc5UaUMn3YZr-4eSnMPV2wv4iEAM4PdwQZYkBiTATMhqDpkxhTok74sn660G1N1l5qWLQLuNQk4lmlpD5hNCPjpXr0GxcMke3Nw",
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
    url = "https://gpt-jinshi.openai.azure.com/openai/deployments/gpt-4-32k-jingshi/chat/completions?api-version=2023-03-15-preview"
    
    headers = {
        "api-key": "b11e8b01c8b44b9db9482f8cd7b410d4", 
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