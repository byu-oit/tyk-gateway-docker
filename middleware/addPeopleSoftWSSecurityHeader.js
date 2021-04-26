var addPeopleSoftWSSecurityHeader = new TykJS.TykMiddleware.NewMiddleware({});

addPeopleSoftWSSecurityHeader.NewProcessRequest(function(request, session, config) {
    log("|- addPeopleSoftWSSecurityHeader() START---|");
    log("|- " + JSON.stringify(request));
    ps_WSS_RemoveHeaders(request);
    log("|--- request.DeleteHeaders: " + JSON.stringify(request.DeleteHeaders) );

    var errorResults = undefined  // on error return object of error data for returnOverrides.
    //
    if (request.Headers["Acting-For"] == "false"){
        if (request.Headers["Resourceowner_net_id"]) {
            request.SetHeaders["Effective_net_id"] = request.Headers["Resourceowner_net_id"];
            log("1- Successful ActingFor == false: effective_net_id set to: " + request.Headers["Resourceowner_net_id"]);
        }
        else {
            log("|---1 ActingFor NOT false : ");
            errorResults = {
                ResponseError: "Invalid Request",
                ResponseBody: "Header Missing from request",
                ResponseCode: 400,
                ResponseHeaders: {}
            }
            log("|---1 ActingFor NOT false : ");
        }
    }
    else {
       var actingFor = canUseActorPermissions()  // db call: probably replaced with Redis call
        if (actingFor == false){
            log("2|--- DB Query canUserActorPermissions == false : " );
            errorResults = {
                ResponseError: "Not Authorized",
                ResponseBody: "Not Authorized",
                ResponseCode: 403,
                ResponseHeaders: {}
            }
            log("2|--- DB Query canUserActorPermissions == false : ");
        }
        else {
            if  (request.Headers["Actor_net_id"]){
                request.SetHeaders["effective_net_id"] = request.Headers["Actor_net_id"];
                log("2- Successful ActingFor permissions: effective_net_id: " + request.Headers["Actor_net_id"]);
            }
            else {
                log("|---2 Missing Property : ");
                errorResults = {
                    ResponseError: "Invalid Request",
                    ResponseBody: "Header Missing from request",
                    ResponseCode: 400,
                    ResponseHeaders: {}
                }
                log("|---2 Missing Property : ");
            }
        }
    }

    if (errorResults != undefined){
        request.ReturnOverrides = errorResults;
        log("ReturnOverrides" + JSON.stringify(request.ReturnOverrides));
    }

    return addPeopleSoftWSSecurityHeader.ReturnData(request, {});
});

function canUseActorPermissions(){
    // there is a function that calls a Database, we're thinking redis cache of info
    // Returning true or false depending on actors cached identity permissions for such.
    // use method: TykGetKeyData(api_key, api_id) to get cached data (BLOCKING CALL)
    // 50/50 true false return.
    var timestamp = new Date().getTime();
    var actingFor = (timestamp%2?true:false);
    log("|-- canUseActorPermissions result = " + actingFor);
    return true;
}

/* check headers
 */
function ps_WSS_RemoveHeaders(request){
    log("|- checkHeaders(headers) ---|");
    var x = 0
    for(var item in request.Headers) {
        item = item.toLowerCase();
        switch (item) {
            case "sm_user":
                request.DeleteHeaders[x++] = item;
                break;
            case "principal_net_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "principal_byu_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "principal_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "actor_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "actor_byu_id":
                request.DeleteHeaders[x++] = item;
                break;
            case "actor_net_id":
                request.DeleteHeaders[x++] = item;
                break;
            default:
                break;
        }
    }
}