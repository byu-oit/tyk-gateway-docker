var boomiAuth = new TykJS.TykMiddleware.NewMiddleware({});

boomiAuth.NewProcessRequest(function(request, session, config) {
    log("|- NewProcessRequest() ---|");
    log(JSON.stringify(request.Headers));

    // iterate through headers looking for X-Jwt-Assertion
    for(var item in request.Headers) {
        console.log(item + ": " + request.Headers[item]);

        // compare formated header key
        if ('X-Jwt-Assertion' == formatHeaderKey(item)) {
            // add X-Wss-Jwt-Assertion header
            request.SetHeaders['X-Wss-Jwt-Assertion'] = String(request.Headers[item]);
            console.log('\tAdd header X-Wss-Jwt-Assertion header: ' + request.Headers[item]);

            // remove X-Jwt-Assertion header
            request.DeleteHeaders[0] = item;
            console.log("\tRemove header: " + item);
        }
    }    

    return boomiAuth.ReturnData(request, {});
});

function formatHeaderKey(str) {
    // convert str to header key format
    var separateWord = str.toLowerCase().split(/[\s_-]+/);
    for (var i = 0; i < separateWord.length; i++) {
       separateWord[i] = separateWord[i].charAt(0).toUpperCase() + separateWord[i].substring(1);
    }
    return separateWord.join('-');
 }
 


  