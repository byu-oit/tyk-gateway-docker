from tyk.decorators import *
from gateway import TykGateway as tyk

@Hook
def MyPostMiddleware(request, session, metadata, spec):
    auth_header = request.get_header('Authorization')
    if auth_header == '47a0c79c427728b3df4af62b9228c8ae':
        session.rate = 1000.0
        session.per = 1.0
        metadata["token"] = "47a0c79c427728b3df4af62b9228c8ae"
        request.SetHeader['Client-Id'] = metadata["token"]
    return request, session, metadata
