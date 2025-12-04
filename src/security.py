import secrets
import json
import os
from datetime import datetime

def checkDateIntegrity(date:str) -> bool:

    tempDate = date
    config_path     = "../contents/config.json"

    if '/' in date:
        tempDate = date.replace('/','-')
    try:
        if tempDate != datetime.strptime(tempDate, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:

        with open(config_path,"r+") as file:

            data = json.load(file)
            data["security"]["key-refreshed-on"] = datetime.today().strftime('%Y-%m-%d')

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