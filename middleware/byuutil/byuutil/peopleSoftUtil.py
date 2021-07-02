from tyk.decorators import *
from gateway import TykGateway as tyk

from .headerUtil import LogHeaders, normalizeHeaderKey

def deletePeopleSoftHeaders(request):
    tyk.log("*** deletePeopleSoftHeaders", "info")
    LogHeaders(request.object.headers)

    # Normalized list of header keys
    headerKeys = ["Sm-User", "Principal-Net-Id", "Principal-Byu-Id", "Principal-Id", "Actor-Id", "Actor-Byu-Id", "Actor-Net-Id"]

    # iterate through headers and check against headerKeys list
    for key, value in request.object.headers.items():
        if normalizeHeaderKey(key) in headerKeys:
            tyk.log("+++ REMOVE header: " + key + "->" + value, "info")
            request.delete_header(key)
