from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

# Getting spotify API token to access the web API features

def get_token():
    auth_string= client_id + ":" + client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_byte64= str(base64.b64encode(auth_bytes), "utf-8")

    url="https://accounts.spotify.com/api/token"
    headers={
        "Authorization": "Basic " + auth_byte64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result= json.loads(result.content)
    token=json_result["access_token"]
    return token
    
    # Defining a function to create authorization headers using the access token

def auth_get_header(token):
    return{"Authorization": "Bearer " + token}
    
# Searching for Artist ID 

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers= auth_get_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result= json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print("No artists with this name...")
        return None
    
    return json_result[0]

# Pulling top songs of artist using artist ID

def get_songs(token,artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers= auth_get_header(token)
    result=get(url, headers=headers)
    json_result= json.loads(result.content)["tracks"]
    return json_result

# Asking for artist name

artist = input("Artist name?: ")
token = get_token()
result = search_for_artist(token, artist)
artist_id=result["id"]
songs=get_songs(token, artist_id)

# Displaying top songs using Index

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")
