from tyk.decorators import *
from gateway import TykGateway as tyk

@Hook
def ServiceNowAuth(request, session, spec):
    # boomiAuthUtil.log()
    tyk.log("*** ServiceNowAuth START", "indo")
    url = request.object.url
    tyk.log("*** url = " + url, "info")
    body = request.object.body
    tyk.log("*** body = " + body, "info")

    # check for X-Jwt-Assertion header
    x_jwt_assertion = request.get_header('X-Jwt-Assertion')

    # if we have the header, insert header X-Wss-Jwt-Assertion with this value
    if x_jwt_assertion:
        # concatenate XJWTAssertion with header value
        authStr = "X-Jwt-Assertion " + x_jwt_assertion
        # add X-Wss-Jwt-Assertion header
        request.add_header("Authorization", authStr)
        tyk.log("add header Authorization: " + authStr, "info")
        # delete X-Jwt-Assertion header
        request.delete_header('X-Jwt-Assertion')
        tyk.log("remove header X-Jwt-Assertion", "info")

    tyk.log("*** ServiceNowAuth End", "info")
    return request, session

    # // iterate through headers looking for X-Jwt-Assertion
    # for(var item in request.Headers) {
    #     console.log(item + ": " + request.Headers[item]);

    #     // compare formated header key
    #     if ('X-Jwt-Assertion' == formatHeaderKey(item)) {
    #         // concatenate XJWTAssertion with header value
    #         var authStr = 'XJWTAssertion ' + String(request.Headers[item]);

    #         // add X-Wss-Jwt-Assertion header
    #         request.SetHeaders['Authorization'] = authStr;
    #         console.log('\tAdd header Authorization: ' + authStr);

    #         // remove X-Jwt-Assertion header
    #         request.DeleteHeaders[0] = item;
    #         console.log("\tRemove header: " + item);
    #         break;
    #     }
