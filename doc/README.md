# Tyk Architecture

## Component overview and traffic routing

![Tyk DNS and SSL](./tyk-dns-and-ssl.png)

There will be three gateways: Oregon, Virginia, and Provo. Tyk will manage the gateways in Oregon and Virginia. BYU will manage the gateway in Provo.

We will use a Route 53 Hosted Zone, and Record Sets with geo-proximity Routing to route client traffic to the closest gateway.

An SSL Certificate will be added to each node where SSL termination takes place. These nodes are red in the diagram above. They include:

* Tyk Developer Portal (SaaS)
* Tyk Dashboard (SaaS)
* Tyk Managed Gateway (SaaS, Oregon)
* Tyk Managed Gateway (SaaS, Virginia)
* BYU Reverse Proxy (Provo)

For APIs that only have a single instance, all gateways will route traffic to that single instance.

For APIs that have instances in multiple regions, the gateways will route traffic to the closest instance. It will be the responsibility of the API provider (aka domain team) to implement geo-proximity based routing for their API. The API Management team will implement the echo API as a multi-region API to prove this functionality out, and to provide a reference implementation for other teams.

## OAuth Tokens and JWTs

![Tyk Token and JWT](./tyk-token-and-jwt.png)

All API clients will use OAuth 2.0 for authentication. The supported grant types will include:

* Auth Code
* Implicit
* PKCE
* Client Credentials

Almost all APIs will accept a JWT that contains the claims listed at [https://developer.byu.edu/docs/design-api/byu-usage-json-web-token](https://developer.byu.edu/docs/design-api/byu-usage-json-web-token). Custom code running on the gateways will be responsible for translating OAuth access tokens into JWTs with the appropriate claims.

A couple of our API platforms are not able to consume JWTs (notably, PeopleSoft and C-Framework). Rather, these platforms accept identity data via an HTTP header. Currently, these platforms are secured at the network layer (i.e. gateways are inside the same trusted zone as the platform servers). **TODO: Figure out how to securely allow these platform servers to trust traffic from gateways managed by Tyk**

Ory Hydra (fronted by Ory Oathkeeper) will be used for OAuth. The gateways will proxy these requests, allowing the token revocation process to be hooked, so that JWTs can be invalidated.

APIs registered in Tyk will not use Token Authentication. Rather, they will use a custom plugin authentication that follows the flow of the diagram above. This eliminates the need to synchronize access tokens with Tyk.
