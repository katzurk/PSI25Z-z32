#!/bin/bash

docker rm -f z32-client-projekt
docker build -t z32-client-docker .
docker run -it --cap-add=NET_ADMIN --network z32_network --name z32-client-projekt z32-client-docker