var addPeopleSoftWSSecurityHeader = new TykJS.TykMiddleware.NewMiddleware({});

addPeopleSoftWSSecurityHeader.NewProcessRequest(function(request, session, config) {
    log("|- addPeopleSoftWSSecurityHeader() ---|");
    //log("|--- request.ReturnOverrides: " + JSON.stringify(request.ReturnOverrides) );
    log("|--- session: " + JSON.stringify(session) );
    var headerResults = checkHeaders(request.Headers);
    if(headerResults){
        log("|--- headerResults NOT undefined : " + JSON.stringify(headerResults) );
        request.ReturnOverrides = headerResults;
        log("|--- headerResults NOT undefined : " + JSON.stringify(headerResults) );
    }
    else {
        //timestamp_middleware = new Date().getTime();
        //request.SetHeaders['byu-entity'] = create_byuEntity();
        var secret = "secret";
        var message = create_byuEntity();
        var hash = CryptoJS.HmacSHA256( message, secret );
        var hashInBase64 = CryptoJS.enc.Base64.stringify(hash);
        request.SetHeaders['auth-jwt-byu-entity'] = hashInBase64;
    }
    log(JSON.stringify(request.Headers));
    return addPeopleSoftWSSecurityHeader.ReturnData(request, {});
});

/* check headers
 */
function checkHeaders(headers){
    log("|- checkHeaders(headers) ---|");
    log("|--- " + JSON.stringify(headers));
    var item;
    for(item in headers){
        log("|----- " + item);
        if(item.toLowerCase() == "smuser"){
            return {
                ResponseError: "Invalid Request",
                ResponseBody: "Invalid Request",
                ResponseCode: 400,
                ResponseHeaders : {
                    "X-Foo": "Bar",
                    "X-Baz": "Qux"
                }
            }
        }
    }
    return undefined;
}

