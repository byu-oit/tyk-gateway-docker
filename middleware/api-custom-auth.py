
from gateway import TykGateway as tyk
from tyk.decorators import *
import json, requests, base64, jwt, datetime

logLevel = "info"

# Function for APIs usoing the Hydra tokens:
# Still to do: ------------------------------------------------------------------------------
#   2. put URLs in the config_data of api json and use instead.
#   3. put private keys for signing into global code, pull from disk first keep in mem using Singleton pattern
#   4. upload to cloud, add package files to bundle in build.sh like Peter
#--------------------------------------------------------------------------------------------
@Hook
def APICustomAuth(request, session, metadata, spec):
    tyk.log("APICustomAuth Begin |---", logLevel)

    auth_token = request.get_header('Authorization')
#     tyk.log("|--- auth_token=" + auth_token, logLevel)
    host = request.get_header('Host')
    tyk.log("|--- host=" + host, logLevel)

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
#   Hydra returns error data instead --------------------------------------------------------
    if 'error' in iData:
        tyk.log("ERROR FROM HYDRA :----------", logLevel)
#         tyk.log("request.ReturnOverrides: " + str(request.object.return_overrides), logLevel)
        request.object.return_overrides.headers['content-type'] = 'application/json'
        request.object.return_overrides.response_code = iData['error']['code']
        request.object.return_overrides.response_error = iData['error']['message'] + ": status = " + iData['error']['status']
#         tyk.log("request.ReturnOverrides: " + str(request.object.return_overrides), logLevel)
        tyk.log("THIS REQUEST IS DENIED DUE TO EXPIRED ACCESS TOKEN: " + auth_token, logLevel)
        return request, session, metadata
    else:
        client_id = iData['client_id']
        tyk.log(client_id, logLevel)
        exp = iData['exp']
        tyk.log(str(exp), logLevel)

        token_data = tyk.get_data(auth_token)
#         tyk.log(str(token_data), logLevel)
        token_decoded = token_data.decode()
#         tyk.log("base64encoded JWT from Redis = " + token_decoded, logLevel)

#       Validate JWT HERE or on first use of Token -----------------------------------------------
        with open('/opt/tyk-gateway/middleware/jwtRS256.pub.jwk', 'rb') as fh:
            verifying_key = jwt.jwk_from_dict(json.load(fh))

#         tyk.log("verify_key: " + str(verifying_key), logLevel)
#         tyk.log("get decoded JWT: ---------", logLevel)

#         This is where the JWT may not pass the time check....
        try:
            cur_jwt = jwt.JWT().decode(token_decoded, verifying_key, do_time_check=True)

        except:
            tyk.log("JWTDecode threw exception -------", logLevel)
            cur_jwt = jwt.JWT().decode(token_decoded, verifying_key, do_time_check=False)
            tyk.log("jwt UTF-8: " + str(cur_jwt), logLevel)

            exp = cur_jwt['exp']
            nowInt = datetime.datetime.utcnow() + datetime.timedelta(seconds=899)
            expire_at = int(nowInt.timestamp())
            cur_jwt['exp'] = expire_at
            tyk.log(str(cur_jwt), logLevel)

#           RE-Generate JWT HERE  -----------------------------------------------
            with open('/opt/tyk-gateway/middleware/jwtRS256.key', 'rb') as fh:
                signing_key = jwt.jwk_from_pem(fh.read())

            new_jwt = jwt.JWT().encode(cur_jwt, signing_key, alg='RS256')

            tyk.log("new_jwt: " + str(new_jwt), logLevel)
            token_decoded = new_jwt

        else:
            tyk.log("JWT is valid ------------", logLevel)
            tyk.log(str(cur_jwt), logLevel)

#       Add data to metadata object for tyk analytics and so it autoGens a key ----------
        metadata["client_id"] = client_id
        metadata["token"] = client_id
        request.add_header('X-Jwt-Assertion', token_decoded)
        tyk.log("APICustomAuth END |---", logLevel)
        return request, session, metadata

