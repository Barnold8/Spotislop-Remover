from loader import *
from server import *


def setup(): 

    f = None

    with open("../contents/CLIENT_ID") as file:
        f = file.readlines()

    return f[0]



if __name__ == "__main__" and satisfiedLibs():

    # print("Running...")

    # client = setup()
    # redirect = "https://github.com/Barnold8/Spotislop-Remover"

    # state = "kyHBOCqrn9fee8WA"
    # scope = "user-read-private user-read-email"

    # body = {

    #     "response_type": 'code',
    #     "client_id": client,
    #     "scope": scope,
    #     "redirect_uri": redirect,
    #     "state": state

    # }

    app.run()
