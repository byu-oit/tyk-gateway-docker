from tyk.decorators import *
from gateway import TykGateway as tyk
imort request

@Hook
def TokenResponseMiddleware(request, response, session, metadata, spec):
    loglevel = "info"
    auth_header = request.get_header('Authorization')
    tyk.log("TokenResponseMiddleware |---", loglevel)
    if auth_header == 'Bearer 19cdb7bd93e8849f1b3260ce7741c0e13':
        tyk.log("if auth_header == true: START", loglevel)
        session.rate = 1000.0
        session.per = 1.0
        metadata["token"] = "47a0c79c427728b3df4af62b9228c8ae"
        request.add_header("Client-Id","dwclogic")
        request.headers["Client-Id"] = "bl645"
    return request, session, metadata

def getTokenIntrospection():

    return