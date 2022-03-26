#!/bin/bash
trap "rm server;kill 0" EXIT

go build -o server
./server -port=8081 &
./server -port=8082 &
./server -port=8083 -api=1 &

sleep 2
echo ">>> start tesst"
curl "http://localhost:9999/api?key=Tom" &
curl "http://localhost:9999/api?key=Tom" &
curl "http://localhost:9999/api?key=Tom" &

wait