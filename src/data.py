import loader
import sys
from typing import List
from datetime import datetime,timedelta

class User:

    def __init__(self,userPayload: dict):

        print(userPayload,sys.stderr)

        self.access_token  = userPayload["access_token"]
        self.refresh_token = userPayload["refresh_token"]
        self.token_type    = userPayload["token_type"]
        self.expiration    = User.getExpirationDateTime(userPayload["expires_in"])

    def getExpirationDateTime(seconds: int):

        now = datetime.today()
        expiration = now + timedelta(0,seconds)

    def serialize(user: 'User') -> dict:
        
        serialised = {
            "access_token"  : user.access_token,
            "refresh_token" : user.refresh_token,
            "token_type"    : user.token_type,
            "expires_in"    : user.expiration 
        }
        return serialised


    def deserialize(data:dict) -> 'User':

        user = User(
            {
                "access_token"  : data["access_token"],
                "refresh_token" : data["refresh_token"],
                "token_type"    : data["token_type"],
                "expires_in"    : data["expires_in"]
            }
        )

        return user

def compileScopes(scopes: List[str]) -> str:

    return " ".join(x for x in scopes)

contents = loader.loadContents() # this is on a wider scope to avoid reading from disk everytime a user needs to interact with the flask server