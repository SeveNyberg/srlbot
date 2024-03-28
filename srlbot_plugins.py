import requests
import numpy as np
import time
import datetime
import json
from authkey import token


def R_index():
    
    # a la Aleksi
    # url="https://space.fmi.fi/MIRACLE/RWC/r-index/api/NUR.json"
    # result=$(jq '{time: .data[0].x, R: .data[0].y, curr_time: .data[0].x[-1], curr_\
    # R: .data[0].y[-1]}' <(curl -s $url))
    
    r = requests.get("https://space.fmi.fi/MIRACLE/RWC/r-index/api/NUR.json")
    return json.loads(r.content)["data"][0]["y"][-1]


def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%c')


def post(channel_id = None, message = None):
    
    if channel_id == None:
        raise("No channel ID provided!")
    
    if message == None:
        raise("No message provided!")

    
    # The API URL through which posts are made
    post_url = "https://mattermost.utu.fi/api/v4/posts"
    headers = { "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                }
    json_data = {   "channel_id": channel_id,
                    "message": message,
                    }
    
    response = requests.post(post_url, headers=headers, json=json_data)
        
        
def read(channel_id = None):
    
    if channel_id == None:
        raise("No channel ID provided!")
    
    # The API URL thourgh which posts are read for commands
    read_url = lambda channel_id: f"https://mattermost.utu.fi/api/v4/channels/{channel_id}/posts"
    
    #curl -H 'Authorization: Bearer 4jymwea6btbqmre61wx6XXXXXX' http://localhost:8065/api/v4/channels/y4srrjqzoj8aunnnakb8px79eo/posts\?since\=1603220326473
    headers = { "Content-Type": "application/json",
               "Authorization": f"Bearer {token}",
               }

    params = {
        'since': int(time.time()*1000-1500),
    }

    response = requests.get(
        read_url(channel_id),
        params=params,
        headers=headers,
    )   

    data = response.content.decode()
    data = data[data.find("posts\":{") + len("posts\":{"):]
    
    if data[0] == "}":
        return ""
    else:
        data = data[data.find("message\":\"") + len("message\":\""):]
        data = data[:data.find("\"")]

    return data