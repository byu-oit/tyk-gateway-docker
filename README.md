Tyk Gateway Docker
=================================

This container only contains the Tyk OSS API Gateway, the Tyk Dashboard is provided as a separate container and needs to be configured separately.


# Installation


## Docker-Compose

With docker-compose, simply run 
```
$ docker-compose up -d
```

Visit the [docs page](http://sedky.ca/tyk-gw-docker-dev-env/docs/gateway/overview) for a walkthrough on everything.

Stopping the system: with docker-compose, simply run
```
$ docker-compose down
```
This will kill any tokens or data stored in the local Redis Cache

To control the Tyk Gateway alone, you can start and stop it by itself.
```
$ docker ps 
```
