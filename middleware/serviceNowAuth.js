var serviceNowAuth = new TykJS.TykMiddleware.NewMiddleware({});

serviceNowAuth.NewProcessRequest(function(request, session, config) {
    log("|- NewProcessRequest() ---|");
    log(JSON.stringify(request.Headers));


    // iterate through headers looking for X-Jwt-Assertion
    for(var item in request.Headers) {
        console.log(item + ": " + request.Headers[item]);

        // compare formated header key
        if ('X-Jwt-Assertion' == formatHeaderKey(item)) {
            // concatenate XJWTAssertion with header value
            var authStr = 'XJWTAssertion ' + String(request.Headers[item]);

            // add X-Wss-Jwt-Assertion header
            request.SetHeaders['Authorization'] = authStr;
            console.log('\tAdd header Authorization: ' + authStr);

            // remove X-Jwt-Assertion header
            request.DeleteHeaders[0] = item;
            console.log("\tRemove header: " + item);
            break;
        }
    }    

    return serviceNowAuth.ReturnData(request, {});
});

function formatHeaderKey(str) {
    // convert str to header key format
    var separateWord = str.toLowerCase().split(/[\s_-]+/);
    for (var i = 0; i < separateWord.length; i++) {
       separateWord[i] = separateWord[i].charAt(0).toUpperCase() + separateWord[i].substring(1);
    }
    return separateWord.join('-');
 }
