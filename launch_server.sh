#!/bin/bash

# 3.1-8B 1 GPU
python3 -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --host 0.0.0.0 --port 30000
# 2-7B 1 GPU
python3 -m sglang.launch_server --model-path meta-llama/Llama-2-7b-chat-hf --port 30000
# 2-7B 2 GPU
python3 -m sglang.launch_server --model-path meta-llama/Llama-2-7b-chat-hf --port 30000 --tp 2 --enable-p2p-check
# 3.2-3B 1 GPU
python3 -m sglang.launch_server --model-path meta-llama/Llama-3.2-3B-Instruct --host 0.0.0.0 --port 30000