#!/bin/bash

#cd /opt/tyk-gateway/middleware
rm -rf /opt/tyk-gateway/middleware/bundles
for bundle in token
do
  rm -f ${bundle}.zip
  /opt/tyk-gateway/tyk bundle build -m ${bundle}.json -y -k /privkey.pem -o ${bundle}.zip
  if [[ ! -f ${bundle}.zip ]]
  then
    echo "[WARN]${bundle}.zip not built!"
  fi
done
python3 -m http.server