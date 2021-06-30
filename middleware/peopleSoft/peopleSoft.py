from tyk.decorators import *
from gateway import TykGateway as tyk

import os
import sys
bundle_dir = os.path.abspath(os.path.dirname(__file__))
for lib_dir in [ 'vendor/lib/python3.7/site-packages/' ]:
  vendor_dir = os.path.join(bundle_dir, lib_dir)
  sys.path.append(vendor_dir)

import byuutil.headerUtil as byu
import byuutil.peopleSoftUtil as ps

@Hook
def PeopleSoftMiddleware(request, session, spec):
  tyk.log("*** PeopleSoftMiddleware START", "info")

  byu.LogHeaders(request.object.headers)

  ps.deletePeopleSoftHeaders(request)

  tyk.log("*** PeopleSoftMiddleware End", "info")
  return request, session