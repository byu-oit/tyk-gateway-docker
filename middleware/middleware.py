from tyk.decorators import *
from gateway import TykGateway as tyk

@Hook
def MyPreMiddleware(request, session, metadata, spec):
    loglevel = "info"
    tyk.log("### MyPreMiddleware START", loglevel)

    auth_header = request.get_header('Authorization')
    if auth_header:
        tyk.log("### Authorization = " + auth_header, loglevel)
    tyk.log("### MyPreMiddleware END", loglevel)

  return request, session, metadata
