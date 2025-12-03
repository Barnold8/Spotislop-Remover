from loader import loadContents
from Url import *
import requests

def OAuth_Spotify():

    contents = loadContents()
    redirect_URL = "http://127.0.0.1:5000/result"

    state = generateRandomString(16)
    scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public" 

    body = {
        "response_type": 'code',
        "client_id": contents["client_id"],
        "scope": scope,
        "redirect_uri": redirect_URL,
        "state": state
    }   
    return body

def getAccessToken(OAuthToken:str) -> str:    

    contents = {}

    with open("../contents/CLIENT_ID") as client:
        contents["client_id"] = client.read()
    with open("../contents/CLIENT_SECRET") as client:
        contents["client_secret"] = client.read()

    url = "https://accounts.spotify.com/api/token"
    request_body = {
        "grant_type": "authorization_code",
        "code": OAuthToken,
        "redirect_uri": "http://127.0.0.1:5000/result",
        "client_id": contents["client_id"],
        "client_secret": contents["client_secret"],
    }
    
    r = requests.post(url, data=request_body)
    response = r.json()

    return response

def getUserPlaylists(OAuthToken:str)-> None:

    # url = "https://api.spotify.com/v1/me/playlists"
    url = f"https://api.spotify.com/v1/users/{OAuthToken}/playlists"
    headers={"Authorization":"Bearer " + OAuthToken}

    x = requests.get(url,headers=headers)
    pass
