# P2P Chat Application

A peer-to-peer chat application built with gRPC and Flask that allows two clients to exchange messages in real-time.

## Features

- **Real-time Messaging**: Send and receive messages between two clients using gRPC.
- **Web Interface**: A simple and responsive web interface for chatting, built with Flask and Bootstrap.
- **Threading**: Uses threading to run both the gRPC server and Flask web server concurrently.

## Installation and run

1. Clone the repository:

   ```bash
   git clone https://github.com/valeriodesiati/grpc-p2p-chat.git
   cd grpc-p2p-chat
   ```

2. Run

   ```bash
   docker-compose up
   ```

3. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000) and [http://localhost:5001](http://localhost:5001) to access the chat interface.

### Usage

- Type your message in the input field and click "Send" to send a message to your peer.
- Messages from your peer will appear in the chat window.

## Directory Structure

```bash
grpc-p2p-chat/
   ├── Dockerfile
   ├── LICENSE
   ├── README.md
   ├── client.py
   ├── compile.sh
   ├── docker-compose.yaml
   ├── docker_deploy.sh
   ├── protos
   │   ├── __pycache__
   │   │   ├── chat_pb2.cpython-311.pyc
   │   │   └── chat_pb2_grpc.cpython-311.pyc
   │   ├── chat.proto
   │   ├── chat_pb2.py
   │   └── chat_pb2_grpc.py
   ├── requirements.txt
   ├── start_clients.sh
   ├── static
   │   ├── css
   │   │   └── styles.css
   │   └── js
   │       └── script.js
   └── templates
      └── chat.html
```

## License

See the [LICENSE](LICENSE) file for details.

## Author

Valerio Desiati
