import requests
import numpy as np
import time
import datetime
import json
from authkey import token


def R_index():
    """
    Returns the R-index fetched from FMI's Nurmijärvi station's JSON-file
    
    Returns:
        (float): the most recent R-index at Nurmijärvi station
    """
    
    # Fetch the JSON-file
    r = requests.get("https://space.fmi.fi/MIRACLE/RWC/r-index/api/NUR.json")
    
    # Get the time data and R-index data for all different categories
    data = json.loads(r.content)["data"]
    data_t = [data[i]["x"][-1] for i in range(len(data)) if len(data[i]["x"]) != 0]
    data_r = [data[i]["y"][-1] for i in range(len(data)) if len(data[i]["y"]) != 0]

    # Order according to time and pick newest
    R = [x for _, x in sorted(zip(data_t, data_r))][-1]

    # Return the R-index
    return R


def timestamp():
    """
    Returns a timestamp in the format DDD MMM dd hh:mm:ss yyyy based on the current Unix time in seconds.
    
    Returns:
        (datetime): the current timestamp (DDD MMM dd hh:mm:ss yyyy).
    """
    
    return datetime.datetime.fromtimestamp(time.time()).strftime('%c')


def post(channel_id = None, message = None):
    """
    Creates a post to the desired channel with the desired message contents.
    
    Parameters:
        channel_id (string): The channel ID of the channel one wants to post to, channel IDs can be found in channel information boxes in Mattermost.
        message (string): The message one wants to post.
        
    Returns:
        None
    """
    
    # Check that a channel ID and a message have been provided
    if channel_id == None:
        print("No channel ID provided!")
        return
    if message == None:
        print("No message provided!")
        return

    
    # The API URL through which posts are made
    post_url = "https://mattermost.utu.fi/api/v4/posts"
    # Parameters for requests to post correctly
    headers = { "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                }
    json_data = {   "channel_id": channel_id,
                    "message": message,
                    }
    
    # Posting with Python's requests
    response = requests.post(post_url, headers=headers, json=json_data)
        
        
def read(channel_id = None):
    """
    Reads the messages that have arrived on a channel within one second of current time, return message contents for other operations.
    
    Parameters:
        channel_id (string): The channel ID of the channel one wants to post to, channel IDs can be found in channel information boxes in Mattermost.
        
    Returns:
        data (string): The contents of the first chosen message (unfortunately not in any order) as a string.
    """
    
    # Check that a channel ID has been provided
    if channel_id == None:
        print("No channel ID provided!")
        return None
    
    # The API URL though which posts are read
    read_url = lambda channel_id: f"https://mattermost.utu.fi/api/v4/channels/{channel_id}/posts"
    # Parameters for requests to read correctly
    headers = { "Content-Type": "application/json",
               "Authorization": f"Bearer {token}",
               }
    params = {
        'since': int(time.time()*1000-1000),
    }

    # Get the whole Requests-object 
    response = requests.get(read_url(channel_id), params=params, headers=headers,)   

    # Parse for message contents, could be also done with JSON, but message IDs complicate matters when trying to choose just some message that has arrived 
    # Decode the binary data to a readable string format
    data = response.content.decode()
    # Look for JSON 'posts' variable contents
    data = data[data.find("posts\":{") + len("posts\":{"):]
    
    # If 'posts' is empty, return empty string
    if data[0] == "}":
        return ""
    # Else parse 'posts' content for the first 'message' content
    else:
        data = data[data.find("message\":\"") + len("message\":\""):]
        data = data[:data.find("\"")]

    # Return the parsed message
    return data