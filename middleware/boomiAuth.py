from tyk.decorators import *
from gateway import TykGateway as tyk
# # import json, requests

# import os
# import sys

# bundle_dir = os.path.abspath(os.path.dirname(__file__))
# for lib_dir in [ 'vendor/lib/python3.7/site-packages/' ]:
#   vendor_dir = os.path.join(bundle_dir, lib_dir)
#   sys.path.append(vendor_dir)

# sys.path.append(bundle_dir)

# import boomiAuthUtil


# @Hook
# def MyPreMiddleware(request, session, metadata, spec):
#     loglevel = "info"
#     tyk.log("MyPreMiddleware START", loglevel)

#     # MyUtilFunction(request, session, metadata, spec)

#     auth_header = request.get_header('Authorization')
#     if auth_header:
#         tyk.log('Authorization = ' + auth_header, loglevel)

#     tyk.log("MyPreMiddleware END", loglevel)
#     return request, session, metadata

@Hook
def BoomiAuthMiddleware(request, session, spec):
    # boomiAuthUtil.log()
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
