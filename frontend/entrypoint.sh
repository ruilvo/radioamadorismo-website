#!/bin/bash

npm i

if [[ -z "${DEVELOPMENT}" ]]
then
    npm run build
fi

echo "Keeping alive..."
exec tail -f /dev/null
