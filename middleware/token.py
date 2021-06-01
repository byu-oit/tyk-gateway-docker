
from gateway import TykGateway as tyk
from tyk.decorators import *
#import requests, json

@Hook
def TokenResponseMiddleware(request, response, session, metadata, spec):
    loglevel = "info"
    auth_header = request.get_header('Authorization')
    tyk.log("TokenResponseMiddleware |---", loglevel)
#     if auth_header == 'Bearer 19cdb7bd93e8849f1b3260ce7741c0e13':
#         tyk.log("if auth_header == true: START", loglevel)
#         session.rate = 1000.0
#         session.per = 1.0
#         metadata["token"] = "47a0c79c427728b3df4af62b9228c8ae"
#         request.add_header("Client-Id","dwclogic")
#         request.headers["Client-Id"] = "bl645"
    responseText = getTokenIntrospection()
    return request, response, session, metadata, spec

def getTokenIntrospection():
    # create url for persons v3 to get email address with netId
    token_url = "https://oauth.api-dev.byu.edu/oauth2/token"

    #test_api_url = "<<URL of the API you want to call goes here>>"

    #client (application) credentials on apim.byu.edu
    client_id = 'test'
    client_secret = 'k6I9OzE2spLPga0VlJu1Ccaa7brroFc3'

    #step A, B - single call with client credentials as the basic auth header - will return access_token
    data = {'grant_type': 'client_credentials'}

    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

    print(access_token_response.headers)
    tyk.log(access_token_response.headers)
    print(access_token_response.text)
    tyk.log(access_token_response.text)

    tokens = json.loads(access_token_response.text)

    print("access token: " + tokens['access_token'])

    #step B - with the returned access_token we can make as many calls as we want

#     api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
#     api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
    tyk.log("token request returning...")
    return api_call_response.text