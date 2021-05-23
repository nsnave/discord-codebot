#!/bin/bash
echo "Building base image codebox..."
docker build ./codebox -t codebox:latest

echo "Compiling necessary files and building sandbox image..."
bash ./build.sh

