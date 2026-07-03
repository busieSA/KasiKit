

def success(data=None, message="Ok"):
    return {
        "success" : True,
        "message" : message,
        "data" : data 
    }