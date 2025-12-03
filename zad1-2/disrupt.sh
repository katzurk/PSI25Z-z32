#!/bin/bash

docker exec z32-client-c tc qdisc add dev eth0 root netem delay 1000ms 500ms loss 50%