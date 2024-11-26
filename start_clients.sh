#!/bin/bash
python client.py --local_port 50050 --target_ip "localhost" --target_port 50051 --flask_port 5000 &
python client.py --local_port 50051 --target_ip "localhost" --target_port 50050 --flask_port 5001