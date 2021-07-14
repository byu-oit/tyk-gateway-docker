
byuJwtRoot = "http://byu.edu/claims/"

byuClientClaims = {
    "http://byu.edu/claims/client_subscriber_net_id": "",
    "http://byu.edu/claims/client_claim_source": "",
    "http://byu.edu/claims/client_person_id": "",
    "http://byu.edu/claims/client_byu_id": "",
    "http://byu.edu/claims/client_net_id": "",
    "http://byu.edu/claims/client_sort_name": "",
    "http://byu.edu/claims/client_surname": "",
    "http://byu.edu/claims/client_surname_position": "",
    "http://byu.edu/claims/client_preferred_first_name": ""
    "http://byu.edu/claims/client_rest_of_name": "",
    "http://byu.edu/claims/client_name_prefix": "",
    "http://byu.edu/claims/client_name_suffix": ""
}

byuResourceOwnerClaims = {
    "http://byu.edu/claims/resourceowner_person_id": "",
    "http://byu.edu/claims/resourceowner_byu_id": "",
    "http://byu.edu/claims/resourceowner_net_id": "",
    "http://byu.edu/claims/resourceowner_surname": "",
    "http://byu.edu/claims/resourceowner_surname_position": "",
    "http://byu.edu/claims/resourceowner_rest_of_name": "",
    "http://byu.edu/claims/resourceowner_preferred_first_name": "",
    "http://byu.edu/claims/resourceowner_sort_name": "",
    "http://byu.edu/claims/resourceowner_prefix": "",
    "http://byu.edu/claims/resourceowner_suffix": ""
}

tykClaimsRoot = {
    "http://tyk.io/claims/"
}

tykClaims = {
    "http://tyk.io/claims/client_id" : "",
    "http://tyk.io/claims/version" : "",
    "http://tyk.io/claims/environment" : "",
    "http://tyk.io/claims/apicontext" : ""
}

def getEmptyJWT():


# Hydra Response
# {
#     'active':  True,
#     'scope':  'openid hydra-clients token-introspection offline_access',
#     'client_id':  'test',
#     'sub':  'dwclogic',
#     'exp':  1623961886,
#     'iat':  1623958285,
#     'iss':  'https: //oauth.api-dev.byu.edu/',
#     'token_type':  'access_token',
#     'ext':  {
#         'client':  {
#             'id':  'test',
#              'owner':  'jgubler'
#         },
#          'scopes':  [
#             'openid',
#              'hydra-clients',
#              'token-introspection',
#              'offline_access'
#         ],
#          'user':  {
#             'byu_id':  '951624834',
#              'display_name':  'David Caldwell',
#              'net_id':  'dwclogic',
#              'person_id':  '452257202',
#              'preferred_first_name':  'David',
#              'prefix':  '',
#              'rest_of_name':  'David W',
#              'sort_name':  'Caldwell,
#              David W',
#              'suffix':  '',
#              'surname':  'Caldwell',
#              'surname_position':  ''
#         }
#     }
# }

