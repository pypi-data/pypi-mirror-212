__version__ = '0.1.1'
import requests
import json 

url = "https://bettershot-w6mm.zeet-berri.zeet.app/openai_listener"

def log(messages, completion, openai_api_key): 
    payload = {
    "messages": messages,
    "completion": completion,
    "openai_api_key": openai_api_key
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response)
    return {"response" : response}