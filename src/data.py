import loader
import sys
from typing import List
from datetime import datetime,timedelta

class User:

    def __init__(self,userPayload: dict):
        self.access_token       = userPayload["access_token"]
        self.refresh_token      = userPayload["refresh_token"]
        self.token_type         = userPayload["token_type"]
        self.profile_picture    = userPayload["profile_picture"]
        self.user_id            = userPayload["user_id"]
        self.display_name       = userPayload["display_name"]
        self.expiration         = User.getExpirationDateTime(userPayload["expires_in"]) if type(userPayload["expires_in"]) == int else userPayload["expires_in"]

    def getExpirationDateTime(seconds: int) -> datetime:
        now = datetime.today()
        expiration = now + timedelta(0,seconds)
        return expiration
    
    def serialiseTime(expiration : datetime) -> str:
        return expiration.strftime('%m/%d/%Y')

    def deserialiseTime(data: str) -> datetime:
        return datetime.strptime(data,'%m/%d/%Y')

    def serialize(user: 'User') -> dict:
        
        serialised = {
            "access_token"    : user.access_token,
            "refresh_token"   : user.refresh_token,
            "token_type"      : user.token_type,
            "expires_in"      : User.serialiseTime(user.expiration),
            "profile_picture" : IMG.serialize(user.profile_picture),
            "user_id"         : user.user_id,
            "display_name"    : user.display_name
        }

        return serialised


    def deserialize(data:dict) -> 'User':

        user = User(
            {
                "access_token"    : data["access_token"],
                "refresh_token"   : data["refresh_token"],
                "token_type"      : data["token_type"],
                "expires_in"      : User.deserialiseTime(data["expires_in"]),
                "profile_picture" : IMG.deserialize(data["profile_picture"]),
                "user_id"         : data["user_id"],
                "display_name"    : data["display_name"]
            }
        )

        return user

class IMG:

    def __init__(self,url:str,width:int,height:int):
        self.url = url
        self.width = width
        self.height = height

    def serialize(img: 'IMG') -> dict:

        serialised = {
            "url"   :img.url,
            "width" :img.width,
            "height":img.height
            }
        
        return serialised

    def deserialize(data:dict) -> 'IMG':

        img = IMG(data["url"],data["width"],data["height"])

        return img

class Playlist:
    
    def __init__(self, ID:str,tracks:dict):
        
        self.ID = ID
        self.tracks = tracks

    def removeHuman(self,AI:List[dict]) -> None:
        # dystopian ass name
    
        tracks = []
        names = [name["name"] for name in AI]

        for track in self.tracks:
            artists = grabArtistsNames(track["track"]["artists"])
            if any(item in names for item in artists):
                tracks.append(track)
        
        for track in tracks:
            print(track["track"]["artists"])

        self.tracks = tracks


def compileScopes(scopes: List[str]) -> str:

    return " ".join(x for x in scopes)

def combineDicts(*dicts):

    final_dict = None

    if len(dicts) >= 1:
        final_dict = dicts[0]
    else:
        return None
    
    dicts[1:]

    for dict in dicts:
        final_dict = final_dict | dict

    return final_dict

def idsToArray(ids:str) -> List[str]:
    return [id for id in ids.split(",")]

def grabArtistsNames(artists:List[dict]):
    return [artist["name"] for artist in artists]


contents = loader.loadContents() # this is on a wider scope to avoid reading from disk everytime a user needs to interact with the flask server