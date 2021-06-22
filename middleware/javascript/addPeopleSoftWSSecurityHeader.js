var addPeopleSoftWSSecurityHeader = new TykJS.TykMiddleware.NewMiddleware({});

addPeopleSoftWSSecurityHeader.NewProcessRequest(function(request, session, config) {
    log("|- addPeopleSoftWSSecurityHeader() START---|");
    var errorResults = undefined;  // on error return object of error data for returnOverrides.
    var actingFor1 = String(request.Headers["Acting-For"]);
    if ( actingFor1 == "false"){
        if (request.Headers["Resourceowner_net_id"]) {
            request.SetHeaders["Effective_net_id"] = String(request.Headers["Resourceowner_net_id"]);;
            log("1- Successful ActingFor == false: effective_net_id set to: " + request.Headers["Resourceowner_net_id"]);
        }
        else {
            errorResults = {
                ResponseError: "Invalid Request",
                ResponseBody: "Header Missing from request",
                ResponseCode: 400,
                ResponseHeaders: {
                    "X-Foo": "Bar",
                    "X-Baz": "Qux"
                }
            }
            log("|---1 ActingFor NOT false : Returning: returnOverrides Data");
        }
    }
    else {
        log("Acting-For was NOT false::  " + actingFor1)
        var actingFor2 = canUseActorPermissions()  // db call: probably replaced with Redis call
        if (actingFor2 == false){
            errorResults = {
                ResponseError: "Not Authorized",
                ResponseBody: "Not Authorized",
                ResponseCode: 403,
                ResponseHeaders: {
                    "X-Foo": "Bar",
                    "X-Baz": "Qux"
                }
            }
            log("2|--- DB Query canUserActorPermissions == false :  Returning: returnOverrides Data");
        }
        else {
            if  (request.Headers["Actor_net_id"]){
                request.SetHeaders["effective_net_id"] = String(request.Headers["Actor_net_id"]);
                log("2- Successful ActingFor permissions: effective_net_id: " + request.Headers["Actor_net_id"]);
            }
            else {
                errorResults = {
                    ResponseError: "Invalid Request",
                    ResponseBody: "Header Missing from request",
                    ResponseCode: 400,
                    ResponseHeaders: {
                        "X-Foo": "Bar",
                        "X-Baz": "Qux"
                    }
                }
                log("|---2 Missing Property : Returning: returnOverrides Data");
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
    return false;
}