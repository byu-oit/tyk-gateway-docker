Tyk Gateway Docker
=================================

This container only contains the Tyk OSS API Gateway, the Tyk Dashboard is provided as a separate container and needs to be configured separately.


# Installation


## Docker-Compose

With docker-compose, simply run 
```
$ docker-compose up -d
```
This starts up the Tyk Docker Container and Redis boxes in Daemon mode (-d)
```
$ docker logs -f tyk-gateway-docker_tyk-gateway_1
```
This will give you a log output terminal, crate a new one because it lock the current terminal when you run it.
```
$docker-compose up
```
this does the same as the 2 previous calls in one call and locks the current terminal until you stop serives.

Visit the [docs page](http://sedky.ca/tyk-gw-docker-dev-env/docs/gateway/overview) for a walkthrough on everything.

## Stopping the service
Stopping the system: with docker-compose, simply run
```
$ docker-compose down
```
This closes down all the Docker Containers, so it will kill any tokens or data stored in the local Redis Cache

To restart the Tyk Docker and keep the redis cache going...
you can start and stop it by itself.
```
$ ▶ docker ps       
CONTAINER ID   IMAGE                      COMMAND                  CREATED        STATUS          PORTS                    NAMES
3696a0c2698f   tykio/tyk-gateway:v3.1.2   "./entrypoint.sh"        20 hours ago   Up 15 minutes   0.0.0.0:8080->8080/tcp   tyk-gateway-docker_tyk-gateway_1
37743df5f18d   redis:5.0-alpine           "docker-entrypoint.s…"   20 hours ago   Up 20 hours     0.0.0.0:6379->6379/tcp   tyk-gateway-docker_tyk-redis_1
```
This list is the currently running containers, and you want to stop the Tyk only so you do not lose your keys
``` 
$ docker stop 369
```
This stops that container, it can be 36 unless there are 2 containers running that both start with 36,
so I generally us 3 or 4 characters of the containers id ex: 3696a0c2698f

#more

