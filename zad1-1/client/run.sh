#!/bin/bash

docker rm -f z32-client-python
docker build -t z32-client-docker .
mkdir -p output

docker run -it --network z32_network -v "$(pwd)/output:/output" --name z32-client-python z32-client-docker $1