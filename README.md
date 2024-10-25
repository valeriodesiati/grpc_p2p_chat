# P2P Chat Application

A peer-to-peer chat application built with gRPC and Flask that allows two clients to exchange messages in real-time.

## Features

- **Real-time Messaging**: Send and receive messages between two clients using gRPC.
- **Web Interface**: A simple and responsive web interface for chatting, built with Flask and Bootstrap.
- **Threading**: Uses threading to run both the gRPC server and Flask web server concurrently.

## Getting Started

### Prerequisites

Before running the application, make sure you have the following installed:

- gRPC
- Flask

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/valeriodesiati/grpc-p2p-chat.git
   cd grpc-p2p-chat
   ```

2. Install the required Python packages:

   ```bash
   pip install grpcio grpcio-tools Flask
   ```

3. Compile the Protocol Buffers:

   Make sure you have the `.proto` files in the `protos` directory and run:

   ```bash
   ./compile.sh
   ```

### Running the Application

1. Open a terminal window.
2. Run

   ```bash
   docker-compose up
   ```

3. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000) and [http://localhost:5001](http://localhost:5001) to access the chat interface.

### Usage

- Type your message in the input field and click "Send" to send a message to your peer.
- Messages from your peer will appear in the chat window.

## Directory Structure

```
grpc-p2p-chat/
├── Dockerfile
├── LICENSE
├── client.py
├── client2.py
├── compile.sh
├── docker-compose.yaml
├── protos
│   ├── __pycache__
│   │   ├── chat_pb2.cpython-311.pyc
│   │   └── chat_pb2_grpc.cpython-311.pyc
│   ├── chat.proto
│   ├── chat_pb2.py
│   └── chat_pb2_grpc.py
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Valerio Desiati
