#!/bin/bash
docker build -t grpc_p2p_chat .
docker tag grpc_p2p_chat valeriodesiati/grpc_p2p_chat:latest
docker push valeriodesiati/grpc_p2p_chat:latest