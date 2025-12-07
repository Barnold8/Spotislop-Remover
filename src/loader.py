import pkg_resources
import os.path
import json
import requests

from typing import List
from datetime import datetime

def errorOut(dependencies:List[str]) -> None: 

    if len(dependencies) <= 0:
        return

    for library in dependencies:
        print(library)

def satisfiedLibs() -> bool:

    required  = None
    satisfied = True
    installString = "Try running \"pip install -r requirements.txt\" from the \"contents\" directory."

    with open("../contents/requirements.txt") as requirements:
        required = requirements.readlines()
        
    for package in required:
        try:
            dist = pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            print(f"Could not find the lib {package}")
            satisfied = False
            
    if satisfied == False:
        print("\n"+installString)

    return satisfied

def downloadRaw(link:str)->str:

    GET = requests.get(link)
    status = GET.status_code

    if status >= 200 and status < 300:
        
        rawType = link.split(".")
        if len(rawType) >= 2:
            type = rawType[-1]
            if type == "txt" or type == "rst":
                return GET.text
            elif type == "json":
                return GET.json()
            else:
                return GET.raw 

    return f"ERROR: Couldnt grab contents from [{link}]"

def writeBands(raw: dict | List[dict],bandsPath:str,lastUpdatedPath):

    contents = raw
    
    if isinstance(contents,list):
        contents = contents[0]
    elif type(contents) == dict:
        pass
    else:
        return
    
    with open(bandsPath,"w") as file:
        json.dump(contents,file)

    with open(lastUpdatedPath,"w") as file:
        file.write(datetime.today().strftime('%Y-%m-%d'))

def grabBands():
    
    ai_bandsJson     = None
    relativeContents = "../contents"
    listPath         = f"{relativeContents}/ai-bands.json"
    datePath         = f"{relativeContents}/ai-bands-lastUpdated.txt"
    link             = "https://raw.githubusercontent.com/romiem/ai-bands/refs/heads/main/dist/ai-bands.json"
    dateFormat       = "%Y-%m-%d"
    maxDays          = 30 


    if os.path.isfile(listPath) and os.path.isfile(datePath):

        today   = datetime.today()
        oldDate = None

        with open(datePath) as file:
            oldDate = file.read()
            oldDate = datetime.strptime(oldDate,dateFormat)

        difference = today - oldDate
        
        if difference.days >= maxDays:
            ai_bandsJson = downloadRaw(link)
            writeBands(ai_bandsJson,listPath,datePath)

    else:
        ai_bandsJson = downloadRaw(link)
        writeBands(ai_bandsJson,listPath,datePath)
    
    return ai_bandsJson

def loadContents() -> dict:

    contents = {}

    with open("../contents/CLIENT_ID") as client:
        contents["client_id"] = client.read()
    with open("../contents/CLIENT_SECRET") as client:
        contents["client_secret"] = client.read()
    with open("../contents/config.json") as settings:
        contents["settings"] = json.load(settings)

    contents["ai-bands"] = grabBands()

    return contents

def validDictionary(keys: List[str], data:dict) -> bool:

    dict_keys = data.keys()

    for key in keys:
        if key not in dict_keys:
            return False
        
    return True