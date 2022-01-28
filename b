#!/bin/bash

curl localhost:8080/post -X POST -H "Content-Type: application/json" -d '{"input":"output"}'
