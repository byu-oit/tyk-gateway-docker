#!/bin/bash

dir="$(pwd)"
docker run --rm -w "/tmp" -v $(pwd):/tmp --entrypoint "/bin/sh" -it tykio/tyk-gateway:v3.1.2 -c "pip3 install -r requirements.txt -t ./vendor/lib/python3.7/site-packages/"
for bundle in byu-token api-custom-auth
do
  /bin/rm -f ${bundle}.zip
    docker run --rm -w "/tmp" -v $(pwd):/tmp --entrypoint "/bin/sh" -it tykio/tyk-gateway:v3.1.2 -c "/opt/tyk-gateway/tyk bundle build -y -m ${bundle}.json -o ${bundle}.zip"
  if [[ ! -f ${bundle}.zip ]]
  then
    echo "[WARN]${bundle}.zip not built!"
  else
    zip -ur ${bundle}.zip vendor/ jwtRS256.key jwtRS256.pub.jwk
  fi
done