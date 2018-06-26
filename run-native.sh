#!/usr/bin/env bash

docker build -t asyncio-bug-native -f Dockerfile-native .
docker run asyncio-bug-native
