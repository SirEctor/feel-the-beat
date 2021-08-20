#!/bin/bash

STATUS=$(curl -s -o /dev/null --head -w "%{http_code}" -X GET "https://feelthebeat.tech//")

if [[ $STATUS != "200" ]]; then
    exit 1
fi

exit 0