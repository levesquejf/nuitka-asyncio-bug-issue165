#!/usr/bin/env bash

docker build -t asyncio-bug-nuitka -f Dockerfile-nuitka .
docker run asyncio-bug-nuitka
