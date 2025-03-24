#!/bin/bash

# Sending single request
curl -s http://localhost:30000/v1/chat/completions \
  -d '{"model": "meta-llama/Meta-Llama-3.1-8B-Instruct", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'

curl -s http://localhost:30000/v1/chat/completions \
  -d '{"model": "meta-llama/Meta-Llama-3.1-8B-Instruct", "messages": [{"role": "user", "content": "What is the capital of Japan?"}]}'

curl -s http://localhost:30000/v1/chat/completions \
  -d '{"model": "meta-llama/Meta-Llama-3.1-8B-Instruct", "messages": [{"role": "user", "content": "What is the capital of Korea?"}]}'



curl -s http://localhost:30000/v1/chat/completions \
  -d '{"model": "meta-llama/Llama-2-7b-chat-hf ", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'

curl -s http://localhost:30000/v1/chat/completions \
  -d '{"model": "meta-llama/Llama-2-7b-chat-hf ", "messages": [{"role": "user", "content": "What is the capital of Japan?"}]}'

curl -s http://localhost:30000/v1/chat/completions \
  -d '{"model": "meta-llama/Llama-2-7b-chat-hf ", "messages": [{"role": "user", "content": "What is the capital of Korea?"}]}'