from Url import *
from data import contents, compileScopes,IMG
import requests
import sys

def OAuth_Spotify() -> dict:

    state = generateRandomString(16)

    redirect_URL = contents["settings"]["redirects"]["spotify-oauth"]
    scope = compileScopes(contents["settings"]["scopes"])

    body = {
        "response_type": 'code',
        "client_id": contents["client_id"],
        "scope": scope,
        "redirect_uri": redirect_URL,
        "state": state
    }   

    return body

def getAccessToken(OAuthToken:str) -> dict:    

    url = "https://accounts.spotify.com/api/token"
    redirect_URL = contents["settings"]["redirects"]["spotify-oauth"]

    request_body = {
        "grant_type": "authorization_code",
        "code": OAuthToken,
        "redirect_uri": redirect_URL,
        "client_id": contents["client_id"],
        "client_secret": contents["client_secret"],
    }
    
    r = requests.post(url, data = request_body)
    response = r.json()

    return response

def getUserPlaylists(url:str,accessToken:str,playlists: List[dict] = []) -> List[dict]:

    headers = {
        "Authorization": "Bearer " + accessToken
    }

    response = requests.get(url, headers=headers).json()
    nextLink = response["next"]
    
    if nextLink != None:
        return getUserPlaylists(
            nextLink,
            accessToken,
            playlists + response["items"]
        )
    
    return playlists

def removeNonUserPlaylists(UID:str,playlists: List[dict]) -> List[dict]:

    sieved = [playlist for playlist in playlists if playlist["owner"]["id"] == UID]
    return sieved


def getUserInformation(accessToken:str) -> dict:

    headers = {
        "Authorization": "Bearer " + accessToken
    }

    url = "https://api.spotify.com/v1/me"
    response = requests.get(url, headers=headers).json()

    img = response["images"][0]

    return {
        "display_name"      : response["display_name"],
        "user_id"           : response["id"],
        "profile_picture"   : IMG(
            img["url"],
            img["width"],
            img["height"]
        )
    }