from loader import loadContents
from Url import *

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
