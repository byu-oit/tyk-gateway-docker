
from gateway import TykGateway as tyk
from tyk.decorators import *
import json, requests, base64
import jwt

@Hook
def APICustomAuth(request, session, metadata, spec):
    logLevel = "info"
    tyk.log("APICustomAuth Begin |---", logLevel)

    auth_token = response.headers['Authorization']
    tyk.log("|--- auth_token=" + auth_token, logLevel)
#    body = json.loads(bodyJsonStr)
#     tyk.log("|--- body=" + str(body), logLevel)

#     access_token = body["access_token"]
#     tyk.log("|--- access_token = " + str(access_token), logLevel)
#     expires_in = body["expires_in"]
#     tyk.log("|--- expires_in = " +  str(expires_in), logLevel)
#     token_type = body["token_type"]
#     tyk.log("|--- token_type = " +  str(token_type), logLevel)
#     scope = body["scope"]
#     tyk.log("|--- scope = " +  str(scope), logLevel)

#   Token Introspection ----------------------------------------------------------------------
#     token_url = "https://oauth.api-dev.byu.edu/oauth2/introspect"
#     data = {'token': access_token}
#     headersData = {
#         'Authorization':'Bearer ' + access_token,
#         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'Accept':  '*/*'
#     }
#     access_token_response = requests.post(token_url, data=data, headers=headersData)
#     tyk.log(str(access_token_response.headers), logLevel)
#     tyk.log(access_token_response.text, logLevel)
#     iData = json.loads(access_token_response.text)
#     tyk.log(str(iData), logLevel)

#   Generate JWT HERE or on first use of Token -----------------------------------------------

#     with open('/opt/tyk-gateway/middleware/jwtRS256.key', 'rb') as fh:
#         signing_key = jwt.jwk_from_pem(fh.read())

#     new_jwt = jwt.JWT().encode(iData, signing_key, alg='RS256')
#     tyk.log(str("Signature: " + new_jwt), logLevel)

#     new_jwt = str(jotHdr64) + "." + str(mStr64) + "." + signature
#     tyk.log("new_jwt: " + str(new_jwt), logLevel)
#   Store JWT under the access_token ---------------------------------------------------------
#     tyk.store_data(access_token, new_jwt, expires_in)

#     token_data = tyk.get_data(access_token)
#     tyk.log("access_token data stored = " + str(token_data), logLevel)

    tyk.log("APICustomAuth END |---", logLevel)
    return request, response, session, metadata, spec
