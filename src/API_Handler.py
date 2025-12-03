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

    # headers = {
    #     'content-type': 'application/x-www-form-urlencoded',
    #     'Authorization': 'Basic ' + OAuthToken
    # }
    # url = 'https://accounts.spotify.com/api/token'
    # x = requests.post(url,headers=headers)

    # print(x.text,sys.stderr)

    return x

def getUserPlaylists(OAuthToken:str)-> None:

    # url = "https://api.spotify.com/v1/me/playlists"
    url = f"https://api.spotify.com/v1/users/{OAuthToken}/playlists"
    headers={"Authorization":"Bearer " + OAuthToken}

    x = requests.get(url,headers=headers)
    pass
