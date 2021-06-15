
from gateway import TykGateway as tyk
from tyk.decorators import *
import json, requests, base64
import jwt
import datetime

@Hook
def APICustomAuth(request, session, metadata, spec):
    logLevel = "info"
    tyk.log("APICustomAuth Begin |---", logLevel)

    auth_token = request.get_header('Authorization')
    tyk.log("|--- auth_token=" + auth_token, logLevel)

#   Token Introspection ----------------------------------------------------------------------
    token_url = "https://oauth.api-dev.byu.edu/oauth2/introspect"
    data = {'token': auth_token}
    headersData = {
        'Authorization':'Bearer ' + auth_token,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept':  '*/*'
    }
    access_token_response = requests.post(token_url, data=data, headers=headersData)
#     tyk.log(access_token_response.text, logLevel)

    iData = json.loads(access_token_response.text)
    tyk.log("iData: " + str(iData), logLevel)
    if 'error' in iData:
        tyk.log("ERROR FROM HYDRA :----------", logLevel)
#         tyk.log("request: " + str(request), logLevel
        return request, session, metadata
    else:
        client_id = iData['client_id']
        tyk.log(client_id, logLevel)
        exp = iData['exp']
        tyk.log(str(exp), logLevel)

        token_data = tyk.get_data(auth_token)
        tyk.log(str(token_data), logLevel)
        token_decoded = token_data.decode()
        tyk.log("access_token from Redis = " + token_decoded, logLevel)

    #   Generate JWT HERE or on first use of Token -----------------------------------------------
        with open('/opt/tyk-gateway/middleware/jwtRS256.pub.jwk', 'rb') as fh:
            verifying_key = jwt.jwk_from_dict(json.load(fh))

        tyk.log("verify_key: " + str(verifying_key), logLevel)
#         tyk.log("get decoded JWT: ---------", logLevel)
        cur_jwt = jwt.JWT().decode(token_decoded, verifying_key, do_time_check=True)
        tyk.log("cur_jwt: " + str(cur_jwt), logLevel)

    #   Decision section ----------
        metadata["client_id"] = client_id
        metadata["token"] = client_id
#         request.set_header('X-Jwt-Assertion', cur_jwt)
        tyk.log("APICustomAuth END |---", logLevel)
        return request, session, metadata
