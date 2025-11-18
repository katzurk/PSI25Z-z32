docker rm -f z32-server-c
docker build -t z32-server-docker .

docker run -it `
    --network-alias z32-server-c `
    --network z32_network `
    --name z32-server-c `
    z32-server-docker `
    $args
