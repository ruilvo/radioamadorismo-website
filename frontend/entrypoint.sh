#!/bin/bash

DEVLOPMENT_ENV=${DEVELOPMENT:-0}

if [ !DEVLOPMENT_ENV ] then
    npm run build
fi

# Keep container alive
exec tail -f /dev/null
