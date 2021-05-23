#!/bin/bash
# gcc client.c -static -static-libgcc -static-libstdc++ -o client
docker build . -t sandbox:latest

