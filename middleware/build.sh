#!/bin/bash
dir="$(pwd)"
vendordir="vendor"

# for bundle in boomiAuth serviceNowAuth rejectSmUserHeader peopleSoft
for bundle in peopleSoft
do
  /bin/rm -f ${bundle}.zip
  cd ${bundle}
  echo $(pwd)

  # create vendor directory if it does not exist
  if [[ ! -e $vendordir ]]; then
    mkdir $vendordir
  elif [[ ! -d $vendordir ]]; then
    echo "$vendordir already exists but is not a directory" 1>&2
  fi

  # add required package to vendor directory
  docker run --rm -w "/tmp" -v $(pwd):/tmp --entrypoint "/bin/sh" -it tykio/tyk-gateway:v3.1.2 -c "pip3 install --upgrade -r requirements.txt -t $vendordir/lib/python3.7/site-packages/"

  # build byuutil and install in vendor directory
  pip3 install --upgrade -t ./$vendordir/lib/python3.7/site-packages/ ${dir}/byuutil

  # build bundle file
  docker run --rm -w "/tmp" -v $(pwd):/tmp --entrypoint "/bin/sh" -it tykio/tyk-gateway:v3.1.2 -c "/opt/tyk-gateway/tyk bundle build -y -m ${bundle}.json -o ${bundle}.zip"
  
  # check to see if bundle was built
  if [[ ! -f ${bundle}.zip ]] ; then
    echo "[WARN]${bundle}.zip not built!"
  else
    zip -ur ${bundle}.zip $vendordir/
  fi
  
  # mv bundle file to middleware directory
  mv ${bundle}.zip ${dir}
  rm -rf tyk-middleware-path*
  cd ${dir}

  # if making these specific bundles add the cert files
  if [[ -f ${bundle}.zip ]] ; then
    if [[ ${bundle} = 'byuToken' || ${bundle} = 'apiCustomAuth' ]]; then
      zip -u ${bundle}.zip jwtRS256.key jwtRS256.pub.jwk
      echo "Certs Copied into zip."
    fi
  else
    echo "[WARN]${bundle}.zip not found so certs not copied in!"
  fi
  echo $(pwd)

done
