#!/bin/bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./protos/chat.proto # compile proto
python client.py --local_port 50050 --target_ip "localhost" --target_port 50051 --flask_port 5000 & #start first client
python client.py --local_port 50051 --target_ip "localhost" --target_port 50050 --flask_port 5001 #start second client