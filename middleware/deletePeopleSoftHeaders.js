var deletePeopleSoftHeaders = new TykJS.TykMiddleware.NewMiddleware({});

deletePeopleSoftHeaders.NewProcessRequest(function(request, session, config) {
    log("|- addPeopleSoftWSSecurityHeader() START---|");
    //log("|- " + JSON.stringify(request));
    log("|- checkHeaders(headers) ---|");
    var x = 0
    for(var item in request.Headers) {
        //log("item = " + item);
        switch (item) {
            case "Sm_user":
                request.DeleteHeaders[x++] = item;
                break;
            case "Principal_net_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "Principal_byu_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "Principal_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "Actor_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "Actor_byu_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "Actor_net_id":
                request.DeleteHeaders[x++] = item;
                break;
            default:
                break;
        }
    }
    log("|--- request.DeleteHeaders: " + JSON.stringify(request.DeleteHeaders) );
    return deletePeopleSoftHeaders.ReturnData(request, {});
});
