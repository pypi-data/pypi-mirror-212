__version__ = '0.1.0'
import requests
import json 

url = "http://0.0.0.0:3000/openai_listener"

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