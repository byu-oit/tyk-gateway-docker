
from gateway import TykGateway as tyk
from tyk.decorators import *

import os
import sys
# bundle_dir = os.path.abspath(os.path.dirname(__file__))
# for lib_dir in [ 'vendor/lib/python3.6/site-packages/', 'vendor/lib64/python3.6/site-packages/' ]:
#   vendor_dir = os.path.join(bundle_dir, lib_dir)
#   sys.path.append(vendor_dir)

import json
import requests

@Hook
def TokenResponseMiddleware(request, response, session, metadata, spec):
    logLevel = "info"
    tyk.log("TokenResponseMiddleware Begin |---", logLevel)
    tyk.log("bundle_dir" + os.path.abspath(os.path.dirname(__file__)), logLevel)
#     tyk.log("|--- ResponseHook response object: " + str(response), logLevel)

    bodyJsonStr = response.raw_body.decode()
#     tyk.log("|--- bodyJsonStr=" + str(bodyJsonStr), logLevel)
    body = json.loads(bodyJsonStr)
#     tyk.log("|--- body=" + str(body), logLevel)

    access_token = body["access_token"]
    tyk.log("|--- access_token = " + str(access_token), logLevel)
    expires_in = body["expires_in"]
    tyk.log("|--- expires_in = " +  str(expires_in), logLevel)
    token_type = body["token_type"]
    tyk.log("|--- token_type = " +  str(token_type), logLevel)
    scope = body["scope"]
    tyk.log("|--- scope = " +  str(scope), logLevel)

#   Token Introspection ----------------------------------------------------------------------
    token_url = "https://oauth.api-dev.byu.edu/oauth2/introspect"

    data = {'token': access_token}
    headersData = {
        'Authorization':'Bearer ' + access_token,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept':  '*/*'
    }
    access_token_response = requests.post(token_url, data=data, headers=headersData)
    tyk.log(str(access_token_response.headers), logLevel)
    tyk.log(access_token_response.text, logLevel)

    introspectionData = json.loads(access_token_response.text)
    tyk.log(str(introspectionData), logLevel)

#     api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
#     api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

#   Generate JWT HERE or on first use of Token?

    tyk.store_data(access_token, "access_token is the key to this sentence.", expires_in)

    token_data = tyk.get_data(access_token)
    tyk.log("access_token data stored = " + str(token_data), logLevel)

    tyk.log("TokenResponseMiddleware END |---", logLevel)
    return request, response, session, metadata, spec

