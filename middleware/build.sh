#!/bin/bash

dir="$(pwd)"
# for bundle in boomiAuth serviceNowAuth
for bundle in boomiAuth serviceNowAuth
do
  /bin/rm -f ${bundle}.zip
  cd ${bundle}
  # echo $(pwd)

  docker run --rm -w "/tmp" -v $(pwd):/tmp --entrypoint "/bin/sh" -it tykio/tyk-gateway:v3.1.2 -c "/opt/tyk-gateway/tyk bundle build -y -m ${bundle}.json -o ${bundle}.zip"
  
  mv ${bundle}.zip ${dir}
  rm -rf tyk-middleware-path*
  cd ..
  # echo $(pwd)

  # bundle build -m ${bundle}.json -y -o ${bundle}.zip

  if [[ ! -f ${bundle}.zip ]]
  then
    echo "[WARN]${bundle}.zip not built!"
  fi
done
