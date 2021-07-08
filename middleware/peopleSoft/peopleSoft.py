from tyk.decorators import *
from gateway import TykGateway as tyk

import os
import sys

bundle_dir = os.path.abspath(os.path.dirname(__file__))
for lib_dir in [ 'vendor/lib/python3.7/site-packages/' ]:
  vendor_dir = os.path.join(bundle_dir, lib_dir)
  sys.path.append(vendor_dir)

from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
import byuutil.headerUtil as byu
import byuutil.peopleSoftUtil as ps

@Hook
def PeopleSoftMiddleware(request, session, spec):
  tyk.log("*** Python version" + str(sys.version), "info")
  tyk.log("*** Python version" + str(sys.version_info), "info")

  # decode jwt
  instance = JWT()
  jot = """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlpXTTJPREE0TWpkak9UQm1NRFZsT0dJNFl6azJOR1kwTXpnNU0yWTFPR0l5T0RJeFpqRmtNdyJ9.eyJpc3MiOiJodHRwczovL2FwaS5ieXUuZWR1IiwiZXhwIjoxNjI1MjM4OTU2LCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL3N1YnNjcmliZXIiOiJCWVUvYmw0NjUiLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FwcGxpY2F0aW9uaWQiOiIxMDUzOSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXBwbGljYXRpb25uYW1lIjoiV1NPMk1vbml0b3IiLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FwcGxpY2F0aW9udGllciI6IlVubGltaXRlZCIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXBpY29udGV4dCI6Ii9lY2hvL3YyIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy92ZXJzaW9uIjoidjIiLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL3RpZXIiOiJVbmxpbWl0ZWQiLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2tleXR5cGUiOiJQUk9EVUNUSU9OIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy91c2VydHlwZSI6IkFQUExJQ0FUSU9OIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9lbmR1c2VyIjoiYmw0NjVAY2FyYm9uLnN1cGVyIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9lbmR1c2VyVGVuYW50SWQiOiItMTIzNCIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvY2xpZW50X2lkIjoiTF9kdE5mQmNQT25McXA3QU5LME9EZWN2bVVFYSIsImh0dHA6Ly9ieXUuZWR1L2NsYWltcy9jbGllbnRfcmVzdF9vZl9uYW1lIjoiQnJ1Y2UgQyIsImh0dHA6Ly9ieXUuZWR1L2NsYWltcy9jbGllbnRfcGVyc29uX2lkIjoiOTAzMjc1NjIyIiwiaHR0cDovL2J5dS5lZHUvY2xhaW1zL2NsaWVudF9zb3J0X25hbWUiOiJMZWUsIEJydWNlIEMiLCJodHRwOi8vYnl1LmVkdS9jbGFpbXMvY2xpZW50X2NsYWltX3NvdXJjZSI6IkNMSUVOVF9TVUJTQ1JJQkVSIiwiaHR0cDovL2J5dS5lZHUvY2xhaW1zL2NsaWVudF9uZXRfaWQiOiJibDQ2NSIsImh0dHA6Ly9ieXUuZWR1L2NsYWltcy9jbGllbnRfc3Vic2NyaWJlcl9uZXRfaWQiOiJibDQ2NSIsImh0dHA6Ly9ieXUuZWR1L2NsYWltcy9jbGllbnRfbmFtZV9zdWZmaXgiOiIgIiwiaHR0cDovL2J5dS5lZHUvY2xhaW1zL2NsaWVudF9zdXJuYW1lIjoiTGVlIiwiaHR0cDovL2J5dS5lZHUvY2xhaW1zL2NsaWVudF9zdXJuYW1lX3Bvc2l0aW9uIjoiTCIsImh0dHA6Ly9ieXUuZWR1L2NsYWltcy9jbGllbnRfbmFtZV9wcmVmaXgiOiIgIiwiaHR0cDovL2J5dS5lZHUvY2xhaW1zL2NsaWVudF9ieXVfaWQiOiI2NDUzOTQzNzMiLCJodHRwOi8vYnl1LmVkdS9jbGFpbXMvY2xpZW50X3ByZWZlcnJlZF9maXJzdF9uYW1lIjoiQnJ1Y2UifQ.n-fhPhuYvb_GhCh1QOgww1vrrqlHGg7NjDSuRa6K24Nbgkdowktt6srMhMegXF2e0xtopou3pkZwhWJCFZ0i-PXEmBBRW3vAd8-P9DBzYvgDb24slisRQU06WB9GyUbJvFz6ZA7uRNbt-0De-E4PNMWv-To0JvrEMhOdxHqZ7bp9gIHbxPMEBcdUtjXXzciT-y1TbCU3T29rSksoVJNDrITuF2iFVX5hRC0KiEU7ith_7U_qfIvUxe_WBuO_ocDRzDSdTxIJid69Xxol1SS5olCuskfq7pXpyu4wnLQDMCFcgDQYQS49vMahHeInBOdnl8VI-ZGSbArhIYbNnMLuiQ"""
  # decoded = instance.decode(jot, None, False)
  decoded = instance.decode(jot, None, False, None, False)
  # decoded = instance.decode(jot, None, options={'verify_exp': False})
  
  tyk.log("+++ jwt" + str(decoded), "info")


  tyk.log("*** PeopleSoftMiddleware START", "info")

  byu.LogHeaders(request.object.headers)

  # disable chunking ???

  # delete peoplesoft headers
  ps.deletePeopleSoftHeaders(request)

  # decode JWT Header
  # {'iss': 'https://api.byu.edu',
  #  'exp': 1625238956,
  #  'http://wso2.org/claims/subscriber': 'BYU/bl465',
  #  'http://wso2.org/claims/applicationid': '10539',
  #  'http://wso2.org/claims/applicationname': 'WSO2Monitor',
  #  'http://wso2.org/claims/applicationtier': 'Unlimited',
  #  'http://wso2.org/claims/apicontext': '/echo/v2',
  #  'http://wso2.org/claims/version': 'v2',
  #  'http://wso2.org/claims/tier': 'Unlimited',
  #  'http://wso2.org/claims/keytype': 'PRODUCTION',
  #  'http://wso2.org/claims/usertype': 'APPLICATION',
  #  'http://wso2.org/claims/enduser': 'bl465@carbon.super',
  #  'http://wso2.org/claims/enduserTenantId': '-1234',
  #  'http://wso2.org/claims/client_id': 'L_dtNfBcPOnLqp7ANK0ODecvmUEa',
  #  'http://byu.edu/claims/client_rest_of_name': 'Bruce C',
  #  'http://byu.edu/claims/client_person_id': '903275622',
  #  'http://byu.edu/claims/client_sort_name': 'Lee, Bruce C',
  #  'http://byu.edu/claims/client_claim_source': 'CLIENT_SUBSCRIBER',
  #  'http://byu.edu/claims/client_net_id': 'bl465',
  #  'http://byu.edu/claims/client_subscriber_net_id': 'bl465',
  #  'http://byu.edu/claims/client_name_suffix': ' ',
  #  'http://byu.edu/claims/client_surname': 'Lee',
  #  'http://byu.edu/claims/client_surname_position': 'L',
  #  'http://byu.edu/claims/client_name_prefix': ' ',
  #  'http://byu.edu/claims/client_byu_id': '645394373',
  #  'http://byu.edu/claims/client_preferred_first_name': 'Bruce'}

  # get rest_url_postfix

  # getActorNetId
  actingFor = False
  actingFor = byu.getHeaderValue(request.object.headers, "Acting-For")
  tyk.log("ActingFor = " + actingFor, "info")
  # if Acting-For

    # if has resource owner

    # else

  # else



  tyk.log("*** PeopleSoftMiddleware End", "info")
  return request, session