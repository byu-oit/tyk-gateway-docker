from tyk.decorators import *
from gateway import TykGateway as tyk

@Hook
def BoomiAuthMiddleware(request, session, spec):
    tyk.log("*** BoomiAuthMiddleware START", "indo")

    # LogHeaders(request.object.headers)

    # check for x-Jwt-Assertion header
    x_jwt_assertion = request.get_header('X-Jwt-Assertion')

    # if we have the header, insert header X-Wss-Jwt-Assertion with this value
    if x_jwt_assertion:
        tyk.log("*** Found header X-Jwt-Assertion", "info")
        # add new heaer
        request.add_header("X-Wss-Jwt-Assertion", x_jwt_assertion)
        # delete X-Jwt-Assertion header
        request.delete_header('X-Jwt-Assertion')

    tyk.log("*** BoomiAuthMiddleware End", "info")
    return request, session

def LogHeaders(headers):
    for key, value in headers.items():
        tyk.log("*** header " + key + "->" + value, "info")
