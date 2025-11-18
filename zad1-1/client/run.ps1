docker rm -f z32-client-python
docker build -t z32-client-docker .

New-Item -ItemType Directory -Force -Path "output" | Out-Null

docker run -it --network z32_network -v "${pwd}\output:/output" --name z32-client-python z32-client-docker $args
