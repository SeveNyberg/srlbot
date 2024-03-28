import requests
import csv
import numpy as np
import time
import datetime
from authkey import token


def R_index():
    # Making a GET request
    r = requests.get("https://space.fmi.fi/image/realtime/UT/NUR/NURdata_01.txt")

    data = r.content.decode().splitlines()
    x = list(csv.reader(data, delimiter = " "))
    x.reverse()

    Bdata = np.array([[val for val in row if val != ""] for row in x[:60]])[:,-3:].astype(float)

    R_index_1 = np.abs(Bdata[:29, 0]-Bdata[1:30, 0]) + np.abs(Bdata[:29, 1]-Bdata[1:30, 1]) + np.abs(Bdata[:29, 2]-Bdata[1:30, 2])
    R_index_2 = np.abs(Bdata[30:-1, 0]-Bdata[31:, 0]) + np.abs(Bdata[30:-1, 1]-Bdata[31:, 1]) + np.abs(Bdata[30:-1, 2]-Bdata[31:, 2])
    R_data = [np.sum(R_index_1), np.sum(R_index_2)]
    R_index = (R_data[0] + 2 * R_data[1])/3 /600 *1350 - 140
    
    return R_index


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