#!/bin/bash
URL="http://127.0.0.1:8000/"

if [ -f msg.conf ] ; then
    . msg.conf
fi

curl -X POST --data "From=8182847345&Body=$1&MessageUUID=1" $URL