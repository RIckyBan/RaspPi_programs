#!/bin/bash

URL="https://maker.ifttt.com/trigger"
EVENTNAME="Raspberry_Pi" 
YOUR_KEY="f-4s8Lcz2BkElbrZR7Tr9eJwEzNMauMXRwa283w31-E" 

WEBHOOKSURL="${URL}/${EVENTNAME}/with/key/${YOUR_KEY}"

curl -X POST -H "Content-Type: application/json" -d '{"value1":"'$1'","value2":"'$2'", "value3":"'$3'"}' ${WEBHOOKSURL} 

echo
exit 0
