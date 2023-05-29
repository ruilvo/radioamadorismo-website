#!/bin/bash

if [[ -z "${DEVELOPMENT}" ]]
then
    npm i
    npm run build
fi

echo "Keeping alive..."
exec tail -f /dev/null
