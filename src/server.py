from flask import Flask,redirect
from Url import *
from loader import loadContents

app = Flask(__name__)

@app.route("/spotify-auth")
def spotify_auth():
    
    contents = loadContents()
    redirect_URL = "http://127.0.0.1:5000/result"

    state = generateRandomString(16)
    scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public" # actually change this

    body = {

        "response_type": 'code',
        "client_id": contents["client_id"],
        "scope": scope,
        "redirect_uri": redirect_URL,
        "state": state

    }    

    return redirect(urlBuilder("https://accounts.spotify.com/authorize?",body))

@app.route("/result")
def result():
    return "<marquee> To be continued... </marquee>"
