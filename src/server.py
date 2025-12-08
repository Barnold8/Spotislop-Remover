from flask import Flask,redirect,render_template,request,session 
from Url import *
from API_Handler import *
from data import User, combineDicts
import json
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",contents="Hello")

@app.route("/spotify-auth")
def spotify_auth_redirect():
    return redirect(urlBuilder("https://accounts.spotify.com/authorize?",OAuth_Spotify()))

@app.route("/spotify-auth/oauth")
def spotify_oauth():

    MAXLEN    = 306
    userCode  = request.args.get('code')
    userState = request.args.get('state')

    ## Make some automatic checking function to put here 
    if userCode == None or userState == None:
        return render_template("error.html",error="Missing auth information")

    if len(userCode) < MAXLEN:
        return render_template("error.html",error="Returned auth code did not meet minimum character length")
    ## Make some automatic checking function to put here 

    user_information = getAccessToken(userCode)
    user_information = combineDicts(user_information,getUserInformation(user_information["access_token"]))
    user = User(user_information)
    
    messages = json.dumps(User.serialize(user))
    session['messages'] = messages

    return redirect("/spotify/display-playlists")

@app.route("/spotify/display-playlists")
def spotify_display_playlists():

    user = User.deserialize(json.loads(session['messages']))
    url = "https://api.spotify.com/v1/me/playlists"
    playlists = getUserPlaylists(url,user.access_token)
    playlists = removeNonUserPlaylists(user.user_id,playlists)

    return render_template("playlists.html",display_name=f"{user.display_name}'s playlists",playlists=playlists)



