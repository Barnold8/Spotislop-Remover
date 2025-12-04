from Url import *
import data
import requests


def OAuth_Spotify():

    state = generateRandomString(16)

    redirect_URL = data.contents["settings"]["redirects"]["spotify-auth"]
    scope = data.compileScopes(data.contents["settings"]["scopes"])

    body = {
        "response_type": 'code',
        "client_id": data.contents["client_id"],
        "scope": scope,
        "redirect_uri": redirect_URL,
        "state": state
    }   

    return body

def getAccessToken(OAuthToken:str) -> str:    

    url = "https://accounts.spotify.com/api/token"

    request_body = {
        "grant_type": "authorization_code",
        "code": OAuthToken,
        "redirect_uri": "http://127.0.0.1:5000/result",
        "client_id": data.contents["client_id"],
        "client_secret": data.contents["client_secret"],
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
