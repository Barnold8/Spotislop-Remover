from flask import Flask,redirect,render_template,request,session 
from Url import *
from API_Handler import *
from data import User, Playlist, combineDicts,idsToArray
from datetime import datetime
from security import validateUserAuth, validateUserSession
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

    userCode  = request.args.get('code')

    if validateUserAuth(userCode):

        user_information = getAccessToken(userCode)
        user_information = combineDicts(user_information,getUserInformation(user_information["access_token"]))
        user = User(user_information)
        messages = User.serialize(user)
        session['messages'] = messages

        return redirect("/spotify/playlists")
    return render_template("error.html")

@app.route("/spotify/playlists")
def spotify_display_playlists():

    if validateUserSession(session):

        user = User.deserialize(session['messages']) # 
        url = "https://api.spotify.com/v1/me/playlists"
        playlists = getUserPlaylists(url,user.access_token)
        playlists = removeNonUserPlaylists(user.user_id,playlists)   
        refresh_token = user.remindToRefreshToken()     
        session['messages'] = User.serialize(user)

        return render_template("playlists.html",display_name=f"{user.display_name}'s playlists",playlists=playlists,token_refresh=refresh_token)
    else:
        return render_template("error.html")

@app.route("/spotify/playlists/scan")
def process_playlists():

    if validateUserSession(session):

        ids = idsToArray(request.args.get("ids"))
        user = User.deserialize(session['messages'])
        playlists = []
        for id in ids:
            
            playlistIDS = id.split("|") # angry i had to do this because of spotify needing a fucking stupid snapshot id for whatever reason uprooting my code to force this upon it
            
            songs = getSongs(f"https://api.spotify.com/v1/playlists/{playlistIDS[0]}/tracks",user.access_token)
            playlist = Playlist(playlistIDS[0],songs,playlistIDS[1])
            playlists.append(playlist)

        removeAI(playlists,user.access_token)
        refresh_token = user.remindToRefreshToken()
        session['messages'] = User.serialize(user)

        return f"<html><h1>IDS</h1><p>f</p></html>"
    return render_template("error.html")
