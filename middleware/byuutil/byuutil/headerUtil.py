from tyk.decorators import *
from gateway import TykGateway as tyk
import re

def LogHeaders(headers):
    for key, value in headers.items():
        tyk.log("*** header " + key + "->" + value, "info")

def normalizeHeaderKey(str):
    # split string by ' ' or '_' or '-' and capitalize
    seperateWord = [word.title() for word in re.split('[\s_-]+', str)]
    # joins elements of list1 by '-'
    retStr = '-'.join(seperateWord)
    return retStr

def getHeaderValue(headers, str):
    for key, value in headers.items():
        if normalizeHeaderKey(key) == str:
            return value
    return None
