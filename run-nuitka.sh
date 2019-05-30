#!/usr/bin/env bash

docker build -t asyncio-bug-nuitka -f Dockerfile-nuitka .
docker run --add-host www.google.com:17.142.160.59 asyncio-bug-nuitka
