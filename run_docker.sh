#!/bin/bash

docker run --gpus '"device=4,5,6,7"' \
    --shm-size 8g -it \
    -p 30000:30000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "{YOUR_TOKEN}" \
    --ipc=host \
    --name {DOCKER_NAME} \
    lmsysorg/sglang:v0.4.1.post5-cu121

# apt-get update
# apt-get install tmux