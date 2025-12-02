from flask import Flask,redirect
from Url import *
from API_Handler import *


app = Flask(__name__)

@app.route("/spotify-auth")
def spotify_auth():

    return redirect(urlBuilder("https://accounts.spotify.com/authorize?",OAuth_Spotify()))

@app.route("/result")
def result():
    return "<marquee> To be continued... </marquee>"
