# Spotislop remover 

## About
> ⚠️ **Know that this project runs the webserver in HTTP which is insecure and should be treated as such if you are to put this on the wider internet**

<div><img style="float: left;" src="https://www.hypebot.com/wp-content/uploads/2022/01/Spotify-No.png" width=100><p style="margin-left: 17%;"> Spotislop remover is a web app that aims to remove AI "artists" from a users selection of playlists. This uses the <a href="https://developer.spotify.com/documentation/web-api">Spotify API</a> to achieve this. </p></div> 

<div style="margin-top:15%;">

## Installation 

### Prerequisites

- Python
- Spotify account

### Making a venv

It is recommended to create a venv for this app such that you don't need to worry or care about versions of libraries already installed on your system and also to avoid installing packages system wide. If this doesn't matter to you, skip this step

To make a venv you simply need to be within the **\<src>** folder and run the command

```python -m venv .```

This will generate a new venv for your web app. From there you can access the scripts folder and run the corresponding activate file for your system. For more information see [here](https://docs.python.org/3/library/venv.html)

</div>

### installing libraries/modules

To install all the required libraries, you can run the following command from the **\<src> directory**<br>
``` pip install -r ../contents/requirements.txt```

This project runs on:

- [pkg_resources](https://pypi.org/project/setuptools/) - To automatically check dependencies
- [flask](https://flask.palletsprojects.com/en/stable/) - To run the webserver
- [requests](https://pypi.org/project/requests/) - To interact with the spotify API


## Required files

There are some files that are required for the server to run but are not given to you. These files are found in the **\<contents>** directory. Other files that are needed but not given to you are generated the first time you run the app. The files required are:

- CLIENT_ID
- CLIENT_SECRET

These are required to communicate with the API in the [authentication](https://developer.spotify.com/documentation/web-api/tutorials/code-flow) stage and require you the user to make your own app on the [spotify developer dashboard](https://developer.spotify.com/documentation/web-api). Don't worry, just follow the following steps:

1. Go to the [spotify developer website](https://developer.spotify.com/)
2. Log in with your spotify account
3. Go to your [dashboard](https://developer.spotify.com/dashboard)
4. Create app
5. Fill in the app information
    1. In the redirect URIs section, you will need to add the **"redirects"** urls from the **config.json** file found in the **\<contents>** directory. If you wish to use another IP and port, you will need to change these in the config file and also update the app.run line in [main.py](src/main.py)


Your app structure should look like


```.
├── contents
│   ├── ai-bands-lastUpdated.txt
│   ├── ai-bands.json
│   ├── CLIENT_ID
│   ├── CLIENT_SECRET
│   ├── config.json
│   ├── requirements.txt
│   └── SERVER_SECRET
├── src
│   ├── static
│   │    ├── images
│   │    │   └── spotify.png
│   │    ├── js
│   │    │   └── playlists.js
│   │    ├── styles
│   │    │   ├── playlists.css
│   │    │   ├── toast.css
│   │    │   └── webCart.css
├── templates
│   ├── error.html
│   ├── index.html
│   └── playlists.html
├── API_Handler.py
├── data.py
├── loader.py
├── main.py
├── satisfiedLibs.py
├── security.py
├── server.py
├── Url.py
```

## Understanding config.json

When you clone the app, you will be given a file that looks like the following:

```json
{
    "redirects": {
        "spotify-oauth": "http://127.0.0.1:5000/spotify-auth/oauth"
    },
    "scopes": [
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public"
    ],
    "security": {
        "key-length": 32,
        "key-refresh" : 30,
        "key-refreshed-on": "2025/12/04"
    }
}
```

### Redirects

This is minimal in the app's current state since this is the only callback needed for the API to work. When you authenticate a user, the spotify API will send information back to the address found in **"spotify-oauth"**

### Scopes

Scopes in this app are used to tell the spotify API what kind of permissions we want from the user. Removing any of these could result in the app recieving errors from the spotify API instead of data. You can find out more about scopes [here](https://developer.spotify.com/documentation/web-api/concepts/scopes)

### Security

#### About
This portion is partly security but it's more of a way for the app to retain session data across routes for a given user. This allows the web app to remember who the user is across web pages on the app and circumvents the user having to log in on every page. This is a security issue because the user holds onto relevant information to their account access like their [access_token](https://getstream.io/glossary/api-token/) which, if a bad actor gets their hands on, could result in data loss, destruction of their overall profile and potential theft of user data. The way session is held is with a secret key, the secret key is to ensure that the session cookie can be signed and the user can be confirmed as themselves. More can be found [here](https://flask.palletsprojects.com/en/stable/config/#:~:text=Default%3A%20None-,SECRET_KEY,-%C2%B6)

#### key-length

This integer tells the app to check if the SERVER_SECRET is a certain length. If the length is not met, the app refuses to run. It is recommended to be at least 16 characters but the default is 32

#### key-refresh

This integer tells the app how many days a SERVER_SECRET can exist before it is refreshed. The integer is in days and thus the default is 30 days. It is recommended to keep the integer <= 30

#### key-refreshed-on

This string tells the app when the key was refreshed. If the current date the app boots up is after the **key-refresh** period, a new key is generated. 