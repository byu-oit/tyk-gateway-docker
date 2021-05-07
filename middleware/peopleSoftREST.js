var peopleSoftREST = new TykJS.TykMiddleware.NewMiddleware({});

peopleSoftREST.NewProcessRequest(function(request, session, config) {
    log("|- NewProcessRequest()  peopleSoftRest ---|");
    log(JSON.stringify(request.Headers));    

    request.SetHeaders["DISABLE_CHUNKING"] = "true";

    // delete headers
    var i = 0;
    request.DeleteHeaders[i++] = "sm_user";
    request.DeleteHeaders[i++] = "principal_net_id";
    request.DeleteHeaders[i++] = "principal_byu_id";
    request.DeleteHeaders[i++] = "principal_id";
    request.DeleteHeaders[i++] = "actor_id";
    request.DeleteHeaders[i++] = "actor_byu_id";
    request.DeleteHeaders[i++] = "actor_net_id";
    
    // get header Acting-For
    var actingFor = getHeaderValue(request, "Acting-For");

    // denormalize "edu.byu.wso2.apim.extensions.DenormalizePeopleSoftURL"

    if ("false" == actingFor) {
        applicationUser = getHeaderValue("usertype");;
        if (applicationUser) {
            // add_RO_SMUserHeader
            retuest.SetHeaders['sm_user'] = getHeaderValue("resourceowner_net_id");

            // add_RO_BYUIdHeader
            request.SetHeaders["principal_byu_id"] = getHeaderValue("resourceowner_byu_id");

            // add_RO_NetIdHeader
            request.SetHeaders["resourceowner_net_id"] = getHeaderValue("principal_net_id");

            // add_RO_PersonIdHeader
            request.SetHeaders["principal_id"] = getHeaderValue("resourceowner_person_id");
        }
        else {
            // add_CLIENT_SMUserHeader
            request.SetHeaders['sm_user'] = getHeaderValue("client_net_id");

            // add_CLIENT_BYUIdHeader
            request.SetHeaders["principal_byu_id"] = getHeaderValue("client_byu_id");
            
            // add_CLIENT_NetIdHeader
            request.SetHeaders["principal_net_id"] = getHeaderValue("client_net_id");
            
            // add_CLIENT_PersonIdHeader
            request.SetHeaders["principal_id"] = getHeaderValue("client_person_id");
        }
    }
    else {
        // check actor permissions 
        canUseActor = checkActorPermissions();

        if (false == canUseActor) {
            request.DeleteHeaders[i++] = "To";
            setPropertyValue("RESPONSE", "true");
            setPropertyValue("NO_ENTITY_BODY", "remove")
            setErrorMessageBody('<format> <am:fault xmlns:am="http://wso2.org/apimanager"> <am:code>BYU-100</am:code> <am:type>Status report</am:type> <am:message>Acting-For Error</am:message> <am:description>Client application is not authorized to use Acting-For header </am:description> </am:fault> </format>');
            set
        }
        else {
            // add_CLIENT_BYUIdHeader
            request.SetHeader["principal_byu_id"] = getHeaderValue("client_byu_id");
            // add_CLIENT_NetIdHeader
            request.SetHeader["principal_net_id"] = getHeaderValue("client_net_id");
            // add_CLIENT_PersonIdHeader
            request.SetHeader["principal_id"] = getHeaderValue("client_person_id");
            // addActorNetIdHeader
            request.SetHeader["actor_net_id"] = getHeaderValue("actorNetId");
            // addActorSMUserHeader
            request.SetHeader["actorNetId"] = getHeaderValue("actorNetId");

            // <class description="LookupActorIdentifiers" name="edu.byu.wso2.apim.extensions.BYUIdentifiersLookup">
            //     <property name="DsName" value="jdbc/BYUPRODB"/>
            //     <property name="PropertyPrefix" value="actor"/>
            //     <property name="NetIdPropertyToUse" value="actorNetId"/>
            // </class>

            // addActorBYUIdHeader
            request.SetHeader["actor_byu_id"] = getHeaderValue("actorBYUId");
            // addActorPersonIdHeader
            request.SetHeader["actor_id"] = getHeaderValue("actorPersonId");
        }
    }

    return peopleSoftREST.ReturnData(request, {});
});

function getHeaderValue(request, key) {
    var value = "";
    // search headers for key
    for(var item in request.Headers) {
        console.log(item + ": " + request.Headers[item]);
        // compare formated header key
        if (key == formatHeaderKey(item)) {
            value = String(request.Headers[item]);
            break;
        }
    }
    return value;
}

function formatHeaderKey(str) {
    // convert str to header key format
    var separateWord = str.toLowerCase().split(/[\s_-]+/);
    for (var i = 0; i < separateWord.length; i++) {
       separateWord[i] = separateWord[i].charAt(0).toUpperCase() + separateWord[i].substring(1);
    }
    return separateWord.join('-');
}

function checkActorPermissions() {
    return true;
}

function setPropertyValue(key, value) {
    return "test Value"
}

function setErrorMessageBody(str) {
    return true;
}

function setReturnCode(returnCode) {
    return true;
}
