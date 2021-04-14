var boomiAuth = new TykJS.TykMiddleware.NewMiddleware({});

boomiAuth.NewProcessRequest(function(request, session, config) {
    log("|- NewProcessRequest() ---|");
    //log("|--- request.ReturnOverrides: " + JSON.stringify(request.ReturnOverrides) );
    log("|--- session: " + JSON.stringify(session) );
    var headerResults = checkHeaders(request.Headers);
    if(headerResults != undefined){
        log("|--- headerResults NOT undefined : " + JSON.stringify(headerResults) );
        request.ReturnOverrides = headerResults;
        log("|--- headerResults NOT undefined : " + JSON.stringify(headerResults) );
    }
    else {
        timestamp_middleware = new Date().getTime();
        var secret = "secret";
        var message = create_byuEntity();
        var hash = CryptoJS.HmacSHA256( message, secret );
        var hashInBase64 = CryptoJS.enc.Base64.stringify(hash);
        request.SetHeaders['auth-jwt-byu-entity'] = hashInBase64;
    }
    log(JSON.stringify(request.Headers));
    return boomiAuth.ReturnData(request, {});
});