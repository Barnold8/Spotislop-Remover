from Url import *
import data
import requests


def OAuth_Spotify():

    state = generateRandomString(16)

    redirect_URL = data.contents["settings"]["redirects"]["spotify-oauth"]
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
    redirect_URL = data.contents["settings"]["redirects"]["spotify-oauth"]

    request_body = {
        "grant_type": "authorization_code",
        "code": OAuthToken,
        "redirect_uri": redirect_URL,
        "client_id": data.contents["client_id"],
        "client_secret": data.contents["client_secret"],
    }
    
    r = requests.post(url, data=request_body)
    response = r.json()

    return response

def getUserPlaylists(accessToken:str)-> None:

    url = "https://api.spotify.com/v1/me/playlists"

    headers = {
  
        "Authorization": "Bearer " + accessToken

    }
    
    response = requests.get(url, headers=headers)

    print(response.text,sys.stderr)


    return response