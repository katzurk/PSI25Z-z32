#!/bin/bash

docker rm -f z32-server-python
docker build -t z32-server-docker .
docker run -it --network-alias z32-server-python --network z32_network --name z32-server-python z32-server-docker
