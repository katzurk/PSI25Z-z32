

docker rm -f z32-server-python 2>$null
docker build -t z32-server-docker .
docker run -it --network-alias z32-server-python --network z32_network --name z32-server-python z32-server-docker
