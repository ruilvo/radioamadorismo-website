#!/bin/bash

echo "Cleaning up..."
rm -rf node_modules/*

echo "Installing modules..."
npm i

if [[ -z "${DEVELOPMENT}" ]]
then
    echo "Building frontend..."
    npm run build
fi

echo "Keeping alive..."
exec tail -f /dev/null
