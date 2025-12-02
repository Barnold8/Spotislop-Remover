def stringifyQuery(contents):

    params = ""

    for key in contents:
        params += key + "=" + contents[key] + "&"
    
    return params[:-1]
