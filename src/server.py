from flask import Flask,redirect,render_template,request,session 
from Url import *
from API_Handler import *
from data import User, Playlist, combineDicts,idsToArray
from datetime import datetime
import json
import sys

app = Flask(__name__)

def validateUserSession() -> bool:

    sessionKeys = session.keys()
    expectedUserKeys = ['access_token', 'display_name', 'expires_in', 'profile_picture', 'refresh_token', 'token_type', 'user_id']
    importantFields = ['access_token', 'display_name', 'expires_in', 'refresh_token', 'user_id']

    if "messages" not in sessionKeys:
        return False
    
    if set(session["messages"].keys()) != set(expectedUserKeys):
        return False
   
    for key, value in session["messages"].items():
        if value == None:
            return False
        
        if key in importantFields: # fair bit of duplicate code since its mostly string validation with no specific metrics but it keeps it readable 
            match key:
                case "access_token":
                    token =  session["messages"]["access_token"]
                    if len(token) <= 0:
                        return False
                    
                case "display_name":
                    name = session["messages"]["display_name"]
                    if len(name) > 30 or len(name) <= 0:
                        return False
                    
                case "expires_in": 
                    try:
                        currentDate = session["messages"]["expires_in"].replace("/","-") # cos the formatting only accepts - and not /, needs to be fixed
                        validDate = datetime.fromisoformat(currentDate)
                        if datetime.today() > validDate: # if the token is expired
                            return False
                    except ValueError as e:
                        return False
                    
                case "refresh_token":
                    token = session["messages"]["refresh_token"]
                    if len(token) <= 0:
                        return False

                case "user_id":
                    token = session["messages"]["user_id"]
                    if len(token) <= 0:
                        return False

    return True

def validateUserAuth(userCode: str) -> bool:    # for clarification, this is used to verify the users auth PRE access token grant
    MAXLEN = 306
    if userCode == None:
        return False

    if len(userCode) < MAXLEN:
        return False
    
    return True

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

    if validateUserSession():

        user = User.deserialize(session['messages']) # 
        url = "https://api.spotify.com/v1/me/playlists"
        playlists = getUserPlaylists(url,user.access_token)
        playlists = removeNonUserPlaylists(user.user_id,playlists)        
        session['messages'] = User.serialize(user)

        return render_template("playlists.html",display_name=f"{user.display_name}'s playlists",playlists=playlists)
    else:
        return render_template("error.html")

@app.route("/spotify/playlists/scan")
def process_playlists():

    if validateUserSession():

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
