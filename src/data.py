import loader
from typing import List

def compileScopes(scopes: List[str]) -> str:

    return " ".join(x for x in scopes)

contents = loader.loadContents() # this is on a wider scope to avoid reading from disk everytime a user needs to interact with the flask server