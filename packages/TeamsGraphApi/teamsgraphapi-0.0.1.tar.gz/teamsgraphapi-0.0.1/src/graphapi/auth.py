base_url = 'https://graph.microsoft.com/v1.0'

def authentication_headers(token):
     
    headers = {
        "Content-Type": "application/json"
    }
    headers["Authorization"] = "Bearer " + token
    return headers
        