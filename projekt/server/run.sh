#!/bin/bash

docker rm -f z32-server-projekt
docker build -t z32-server-docker -f dockerfile ..
docker run -it --network-alias z32-server-projekt --network z32_network --name z32-server-projekt z32-server-docker