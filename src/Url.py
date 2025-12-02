from typing import List

def stringifyQuery(contents):

    params = ""

    for key in contents:
        params += key + "=" + contents[key] + "&"
    
    return params[:-1]

def urlBuilder(origin: str, params:List[str])-> str:
    return origin + stringifyQuery(params)

