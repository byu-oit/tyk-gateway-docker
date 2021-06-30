from tyk.decorators import *
from gateway import TykGateway as tyk

import os
import sys
bundle_dir = os.path.abspath(os.path.dirname(__file__))
for lib_dir in [ 'vendor/lib/python3.7/site-packages/' ]:
  vendor_dir = os.path.join(bundle_dir, lib_dir)
  sys.path.append(vendor_dir)

import byuutil.headerUtil as byu

@Hook
def BoomiAuthMiddleware(request, session, spec):
    tyk.log("*** BoomiAuthMiddleware START", "info")

    byu.LogHeaders(request.object.headers)

    # check for Sm-User header
    for key, value in request.object.headers.items():
        # tyk.log("*** header " + key + "->" + value, "info")
        if (byu.normalizeHeaderKey(key) == 'X-Jwt-Assertion'):
            # if we have the header, insert header X-Wss-Jwt-Assertion with this value
            tyk.log("*** FOUND X-Jwt-Assertion header: " + key + "->" + value, "info")
            # add new heaer
            request.add_header("X-Wss-Jwt-Assertion", value)
            # delete X-Jwt-Assertion header
            request.delete_header(key)
            break

    tyk.log("*** BoomiAuthMiddleware End", "info")
    return request, session
