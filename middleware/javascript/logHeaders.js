var logHeaders = new TykJS.TykMiddleware.NewMiddleware({});

logHeaders.NewProcessRequest(function(request, session, config) {
    log("|- NewProcessRequest() showHeaders.js---|");
    // log(JSON.stringify(request.Headers));

    // iterate through headers looking for X-Jwt-Assertion
    for(var item in request.Headers) {
        log(item + ": " + request.Headers[item]);
    }    

    return logHeaders.ReturnData(request, {});
});

