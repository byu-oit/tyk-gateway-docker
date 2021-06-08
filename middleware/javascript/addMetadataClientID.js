var addMetadataClientID = new TykJS.TykMiddleware.NewMiddleware({});

addMetadataClientID.NewProcessRequest(function(request, session, config) {
    log("starting addMetadataClientID");
    log("--request: " + JSON.stringify(request));
    log("--session: " + JSON.stringify(session));
    log("--config: " + JSON.stringify(config));
    //var response = getTokenData();
    //log("response: " + response)
    //var respObj = JSON.parse(response);

    return addMetadataClientID.ReturnData(request, {});
});

function getTokenData(body){
    var newRequest = {
        "Method": "POST",
        "Body": JSON.stringify(body),
        "Headers": {},
        "Domain": "http://foo.com",
        "Resource": "/event/quotas",
        "FormData": {"field": "value"}
    };
    return TykMakeHttpRequest(JSON.stringify(newRequest));
}