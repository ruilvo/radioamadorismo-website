#!/bin/bash

# The script starts from /workspace
cd frontend

if [[ -z "${DEVELOPMENT}" ]]
then
    npm run build
fi

echo "Keeping alive..."
exec tail -f /dev/null
