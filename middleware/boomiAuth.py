from tyk.decorators import *
from gateway import TykGateway as tyk
# import middleware

@Hook
def MyPreMiddleware(request, session, metadata, spec):
    loglevel = "info"
    tyk.log("MyPreMiddleware START", loglevel)

    auth_header = request.get_header('Authorization')
    if auth_header:
        tyk.log('Authorization = ' + auth_header, loglevel)

    tyk.log("MyPreMiddleware END", loglevel)
    return request, session, metadata

@Hook
def BoomiAuthMiddleware(request, session, spec):
    tyk.log("*** BoomiAuthMiddleware START", "indo")
    url = request.object.url
    tyk.log("*** url = " + url, "info")
    body = request.object.body
    tyk.log("*** body = " + body, "info")

    # check for x-Jwt-Assertion header
    x_jwt_assertion = request.get_header('X-Jwt-Assertion')

    # if we have the header, insert header X-Wss-Jwt-Assertion with this value
    if x_jwt_assertion:
        request.add_header("X-Wss-Jwt-Assertion", x_jwt_assertion)

    # delete X-Jwt-Assertion header
    request.delete_header('X-Jwt-Assertion')

    tyk.log("*** BoomiAuthMiddleware End", "info")
    return request, session
