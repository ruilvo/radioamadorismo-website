#!/bin/bash

# This file runs from its parent dir
cd frontend
npm run build

# Keep container alive
exec tail -f /dev/null
