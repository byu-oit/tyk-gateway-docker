
from gateway import TykGateway as tyk
from tyk.decorators import *

import os
import sys
bundle_dir = os.path.abspath(os.path.dirname(__file__))
for lib_dir in [ 'vendor/lib/python3.7/site-packages/' ]:
  vendor_dir = os.path.join(bundle_dir, lib_dir)
  sys.path.append(vendor_dir)

import json, requests, jwt, base64, datetime

@Hook
def TokenResponseMiddleware(request, response, session, metadata, spec):
    logLevel = "info"
    tyk.log("TokenResponseMiddleware Begin |---", logLevel)

    bodyJsonStr = response.raw_body.decode()
#     tyk.log("|--- bodyJsonStr=" + str(bodyJsonStr), logLevel)
    body = json.loads(bodyJsonStr)
#     tyk.log("|--- body=" + str(body), logLevel)

    access_token = body["access_token"]
    tyk.log("|--- access_token = " + str(access_token), logLevel)
    expires_in = body["expires_in"]
    tyk.log("|--- expires_in = " +  str(expires_in), logLevel)
#     token_type = body["token_type"]
#     tyk.log("|--- token_type = " +  str(token_type), logLevel)
#     scope = body["scope"]
#     tyk.log("|--- scope = " +  str(scope), logLevel)

#   Token Introspection ----------------------------------------------------------------------
#   Environment friendly re-factor here.
    token_url = "https://oauth.api-dev.byu.edu/oauth2/introspect"
    data = {'token': access_token}
    headersData = {
        'Authorization':'Bearer ' + access_token,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept':  '*/*'
    }
    access_token_response = requests.post(token_url, data=data, headers=headersData)
#     tyk.log(str(access_token_response.headers), logLevel)
#     tyk.log(access_token_response.text, logLevel)
    iData = json.loads(access_token_response.text)
    tyk.log(str(iData), logLevel)

#     Now make the JWT expire in 15 minutes
    nowInt = datetime.datetime.utcnow() + datetime.timedelta(seconds=900)
    expire_at = int(nowInt.timestamp())
    iData['exp'] = expire_at
    tyk.log(str(iData), logLevel)

#   Generate JWT HERE or on first use of Token -----------------------------------------------
    with open( bundle_dir + '/jwtRS256.key', 'rb') as fh:
        signing_key = jwt.jwk_from_pem(fh.read())

    new_jwt = jwt.JWT().encode(iData, signing_key, alg='RS256')
#     tyk.log("new_jwt: " + str(new_jwt), logLevel)

    tyk.log("new_jwt: " + str(new_jwt), logLevel)

#   Store JWT under the access_token ---------------------------------------------------------
    tyk.store_data(access_token, new_jwt, expires_in)

#     token_data = tyk.get_data(access_token)
#     tyk.log("access_token data stored = " + str(token_data), logLevel)

    tyk.log("TokenResponseMiddleware END |---", logLevel)
    request.add_header('APICustomAuth', 'Finished Again')
    return request, response, session, metadata, spec
