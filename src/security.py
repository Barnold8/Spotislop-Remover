import secrets
import json
import os
from datetime import datetime

def checkDateIntegrity(date:str) -> bool:

    tempDate = date
    config_path     = "../contents/config.json"

    try:
        if tempDate != datetime.strptime(tempDate, "%Y/%m/%d").strftime('%Y/%m/%d'):
            raise ValueError
        return True
    except ValueError:

        with open(config_path,"r+") as file:

            data = json.load(file)
            data["security"]["key-refreshed-on"] = datetime.today().strftime('%Y/%m/%d')

            file.seek(0)
            json.dump(data, file)
            file.truncate()
            
        return False

def hasExpired(daysToExpire:int,lastUpdated:str) -> bool:

    format = '%Y/%m/%d'
    today = datetime.today()
    lastUpdatedDate = datetime.strptime(lastUpdated,format)
    difference = today-lastUpdatedDate
    
    if difference.days >= daysToExpire:
        return True

    return False

def secret_key() -> str:

    MINIMUM_CHAR_LENGTH = 16
    secret_path     = "../contents/SERVER_SECRET"
    config_path     = "../contents/config.json"
    charLen         = -1
    settings        = None
    secret_key      = None
    days_to_expire  = None
    last_updated    = None

    with open(config_path) as file:
        settings       = json.load(file)
        charLen        = settings["security"]["key-length"]
        days_to_expire = settings["security"]["key-refresh"]
        last_updated   = settings["security"]["key-refreshed-on"]

    if charLen < MINIMUM_CHAR_LENGTH:
        return None

    if os.path.isfile(secret_path) != True:
        with open(secret_path,"w") as file:
            secret_key = secrets.token_hex(charLen)
            file.write(secret_key)
    else:
        with open(secret_path,"r+") as file:
            secret_key = file.read()
            if len(secret_key) <= 0:
                secret_key = secrets.token_hex(charLen)
                file.write(secret_key)

            elif checkDateIntegrity(last_updated) == False or hasExpired(days_to_expire,last_updated) == False:
                file.seek(0)
                secret_key = secrets.token_hex(charLen)
                file.write(secret_key)
                file.truncate()
        
    return secret_key

def validateUserSession(session) -> bool:

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
