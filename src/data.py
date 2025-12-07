import loader
import sys
from typing import List
from datetime import datetime,timedelta

class User:

    def __init__(self,userPayload: dict):
        self.access_token       = userPayload["access_token"]
        self.refresh_token      = userPayload["refresh_token"]
        self.token_type         = userPayload["token_type"]
        self.profile_pitcure    = userPayload["profile_picture"]
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
            "access_token"  : user.access_token,
            "refresh_token" : user.refresh_token,
            "token_type"    : user.token_type,
            "expires_in"    : User.serialiseTime(user.expiration) 
        }
        return serialised


    def deserialize(data:dict) -> 'User':

        user = User(
            {
                "access_token"  : data["access_token"],
                "refresh_token" : data["refresh_token"],
                "token_type"    : data["token_type"],
                "expires_in"    : User.deserialiseTime(data["expires_in"])
            }
        )

        return user

class IMG:

    def __init__(self,href:str,width:int,height:int):
        self.href = href
        self.width = width
        self.height = height

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

contents = loader.loadContents() # this is on a wider scope to avoid reading from disk everytime a user needs to interact with the flask server