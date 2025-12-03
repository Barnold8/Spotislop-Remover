from flask import Flask,redirect,render_template,request
from Url import *
from API_Handler import *
import sys

app = Flask(__name__)

@app.route("/spotify-auth")
def spotify_auth():
    return redirect(urlBuilder("https://accounts.spotify.com/authorize?",OAuth_Spotify()))

@app.route("/")
def index():
    return render_template("index.html",content="Hello")

@app.route("/spotify-auth/result")
def result():

    MAXLEN    = 306
    userCode  = request.args.get('code')
    userState = request.args.get('state')

    if userCode == None or userState == None:
        return render_template("error.html",error="Missing auth information")

    if len(userCode) < MAXLEN:
        return render_template("error.html",error="Returned auth code did not meet minimum character length")
    
    return f"<h1>Auth accepted</h1>"
