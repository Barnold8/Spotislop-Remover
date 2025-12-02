from flask import Flask,redirect
from Url import *

def setup(): 

    f = None

    with open("../contents/CLIENT_ID") as file:
        f = file.readlines()

    return f[0]

app = Flask(__name__)



@app.route("/spotify-auth")
def spotify_auth():
    
    client = setup()
    redirect_URL = "http://127.0.0.1:5000/result"

    state = generateRandomString()
    scope = "user-read-private user-read-email" # actually change this

    body = {

        "response_type": 'code',
        "client_id": client,
        "scope": scope,
        "redirect_uri": redirect_URL,
        "state": state

    }    

    return redirect(urlBuilder("https://accounts.spotify.com/authorize?",body))

@app.route("/result")
def result():
    return "<marquee> To be continued... </marquee>"
