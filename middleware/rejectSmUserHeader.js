var rejectSmUserHeader = new TykJS.TykMiddleware.NewMiddleware({});

rejectSmUserHeader.NewProcessRequest(function(request, session, config) {
    log("|- NewProcessRequest() ---|");
    //log("|--- request.ReturnOverrides: " + JSON.stringify(request.ReturnOverrides) );
    log("|--- session: " + JSON.stringify(session) );
    //var headerResults = checkHeaders(request.Headers);
    //if(headerResults != undefined){
        log("|--- headerResults NOT undefined : " + JSON.stringify(headerResults) );
        request.ReturnOverrides = headerResults;
        log("|--- headerResults NOT undefined : " + JSON.stringify(headerResults) );
    //}

    log(JSON.stringify(request.Headers));
    return rejectSmUserHeader.ReturnData(request, {});
});

/* check headers
 */
// function checkHeaders(headers){
//     log("|- checkHeaders(headers) ---|");
//     log("|--- " + JSON.stringify(headers));
//     var item;
//     for(item in headers){
//         log("|----- " + item);
//         if(item.toLowerCase() == "smuser"){
//             return {
//                 ResponseError: "Invalid Request",
//                 ResponseBody: "Invalid Request",
//                 ResponseCode: 400,
//                 ResponseHeaders : {
//                     "X-Foo": "Bar",
//                     "X-Baz": "Qux"
//                 }
//             }
//         }
//     }
//     return undefined;
// }
