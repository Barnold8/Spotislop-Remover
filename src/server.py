from flask import Flask,redirect,render_template,request,session 
from Url import *
from API_Handler import *
from data import User, Playlist, combineDicts,idsToArray
import json
import sys

app = Flask(__name__)

def validateUser() -> bool:

    sessionKeys = session.keys()
    expectedUserKeys = ['access_token', 'display_name', 'expires_in', 'profile_picture', 'refresh_token', 'token_type', 'user_id']

    if "messages" not in sessionKeys:
        return False
    if set(session["messages"].keys()) != set(expectedUserKeys):
        return False

    return True

@app.route("/test")
def test():
    validateUser()
    return render_template("index.html",contents="Hello")

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

    messages = User.serialize(user)
    session['messages'] = messages

    return redirect("/spotify/playlists")

@app.route("/spotify/playlists")
def spotify_display_playlists():

    if validateUser():

        user = User.deserialize(session['messages'])
        url = "https://api.spotify.com/v1/me/playlists"
        playlists = getUserPlaylists(url,user.access_token)
        playlists = removeNonUserPlaylists(user.user_id,playlists)

        session['messages'] = User.serialize(user)
        
        return render_template("playlists.html",display_name=f"{user.display_name}'s playlists",playlists=playlists)
    else:
        return render_template("error.html")

@app.route("/spotify/playlists/scan")
def process_playlists():

    if validateUser():

        ids = idsToArray(request.args.get("ids"))
        user = User.deserialize(session['messages'])
        playlists = []

        for id in ids:
            
            playlistIDS = id.split("|") # angry i had to do this because of spotify needing a fucking stupid snapshot id for whatever reason uprooting my code to force this upon it
            
            songs = getSongs(f"https://api.spotify.com/v1/playlists/{playlistIDS[0]}/tracks",user.access_token)
            playlist = Playlist(playlistIDS[0],songs,playlistIDS[1])
            playlists.append(playlist)

        removeAI(playlists,user.access_token)

        session['messages'] = User.serialize(user)

        return f"<html><h1>IDS</h1><p>f</p></html>"
    return render_template("error.html")
