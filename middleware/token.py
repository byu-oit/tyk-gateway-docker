
from gateway import TykGateway as tyk
from tyk.decorators import *
import json
import requests

@Hook
def TokenResponseMiddleware(request, response, session, metadata, spec):
    logLevel = "info"
    tyk.log("TokenResponseMiddleware Begin |---", logLevel)

#     tyk.log("ResponseHook response object: " + str(response), logLevel)

    bodyJsonStr = response.raw_body.decode()
#     tyk.log("bodyJsonStr=" + str(bodyJsonStr), logLevel)
    body = json.loads(bodyJsonStr)
#     tyk.log("body=" + str(body), logLevel)
    token = body["access_token"]
    tyk.log("token=" + token, logLevel)

#   Generate JWT HERE or on first use of Token?

    tyk.store_data(token, "Token is the key to this sentence.", 3598)

    token_data = tyk.get_data(token)
    tyk.log("token data stored = " + str(token_data), logLevel)

    tyk.log("TokenResponseMiddleware END |---", logLevel)
    return request, response, session, metadata, spec

