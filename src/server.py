from flask import Flask,redirect,render_template,request
from Url import *
from API_Handler import *
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",content="Hello")

@app.route("/spotify-auth")
def spotify_auth_redirect():
    return redirect(urlBuilder("https://accounts.spotify.com/authorize?",OAuth_Spotify()))

@app.route("/spotify-auth/oauth")
def spotify_oauth():

    MAXLEN    = 306
    userCode  = request.args.get('code')
    userState = request.args.get('state')

    if userCode == None or userState == None:
        return render_template("error.html",error="Missing auth information")

    if len(userCode) < MAXLEN:
        return render_template("error.html",error="Returned auth code did not meet minimum character length")


    token = getAccessToken(userCode)["access_token"]

    items = getUserPlaylists(
        "https://api.spotify.com/v1/me/playlists",
        token,
        []
    )

    x = "<ul>"

    for item in items:
        x += f"<li>{item["name"]}</li>"

    x += "</ul>"

    return f"<h1>Auth accepted</h1>{x}"


