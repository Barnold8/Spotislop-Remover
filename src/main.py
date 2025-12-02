import requests


def setup(): 

    f = None

    with open("../contents/CLIENT_ID") as file:
        f = file.readlines()

    return f[0]

def stringifyQuery(contents):

    params = ""

    for key in contents:
        params += key + "=" + contents[key] + "&"
    
    return params[:-1]


if __name__ == "__main__":
    
    client = setup()
    redirect = "https://github.com/Barnold8/Spotislop-Remover"

    state = "kyHBOCqrn9fee8WA"
    scope = "user-read-private user-read-email"

    body = {

        "response_type": 'code',
        "client_id": client,
        "scope": scope,
        "redirect_uri": redirect,
        "state": state

    }



    # print(buildParams(body))


    x = requests.get('https://accounts.spotify.com/authorize?' + stringifyQuery(body))

    # print(x,x.reason)

    # print('https://accounts.spotify.com/authorize?' + buildParams(body))