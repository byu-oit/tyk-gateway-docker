from tyk.decorators import *
from gateway import TykGateway as tyk

@Hook
def ServiceNowAuth(request, session, spec):
    tyk.log("*** ServiceNowAuth START", "indo")
    # url = request.object.url
    # tyk.log("*** url = " + url, "info")
    # body = request.object.body
    # tyk.log("*** body = " + body, "info")

    # LogHeaders(request.object.headers)

    # check for X-Jwt-Assertion header
    x_jwt_assertion = request.get_header('X-Jwt-Assertion')

    # if we have the header, insert header X-Wss-Jwt-Assertion with this value
    if x_jwt_assertion:
        # concatenate XJWTAssertion with header value
        authStr = "X-Jwt-Assertion " + x_jwt_assertion

        # add X-Wss-Jwt-Assertion header
        tyk.log("add header Authorization: " + authStr, "info")
        request.add_header("Authorization", authStr)

        # delete X-Jwt-Assertion header
        tyk.log("remove header X-Jwt-Assertion", "info")
        request.delete_header('X-Jwt-Assertion')

    tyk.log("*** ServiceNowAuth End", "info")
    return request, session

def LogHeaders(headers):
    for key, value in headers.items():
        tyk.log("*** header " + key + "->" + value, "info")
