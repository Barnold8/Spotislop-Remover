from typing import List
from random import randint
import string
import sys


def generateRandomString(length:int) -> str:

    chars = [list(string.ascii_uppercase) + list(string.digits) + list(string.ascii_lowercase)]
    chars = [item for items in chars for item in items]

    randomString = ""

    for i in range(length):
        randomString += chars[randint(0,len(chars)-1)]

    return randomString

def stringifyQuery(contents):

    params = ""

    for key in contents:
        params += key + "=" + contents[key] + "&"
    
    return params[:-1]

def urlBuilder(origin: str, params:List[str])-> str:
    return origin + stringifyQuery(params)

