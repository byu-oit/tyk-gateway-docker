from tyk.decorators import *
from gateway import TykGateway as tyk

import re

@Hook
def rejectSmUserHeader(request, session, spec):
    tyk.log("*** rejectSmUserHeader START", "indo")
    # LogHeaders(request.object.headers)

    # check for Sm-User header
    for key, value in request.object.headers.items():
        # tyk.log("*** header " + key + "->" + value, "info")
        normalizedKey = normalizeHeaderKey(key)
        if (normalizedKey == "Sm-User"):
            tyk.log("*** FOUND Sm-User header: " + key + "->" + value, "info")
            # Set a custom error:
            request.object.return_overrides.response_error = 'Not authorized'
            request.object.return_overrides.response_code = 401
            return request, session
 
    tyk.log("*** NOT FOUND Sm-User header", "info")
    return request, session

def LogHeaders(headers):
    for key, value in headers.items():
        tyk.log("*** header " + key + "->" + value, "info")

def normalizeHeaderKey(str):
    # split string by ' ' or '_' or '-' and capitalize
    seperateWord = [word.title() for word in re.split('[\s_-]+', str)]
    # joins elements of list1 by '-'
    retStr = '-'.join(seperateWord)
    return retStr
