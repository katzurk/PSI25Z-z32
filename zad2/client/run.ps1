

docker rm -f z32-client-c 2>$null
docker build -t z32-client-docker .
docker run -it --network z32_network --name z32-client-c z32-client-docker
