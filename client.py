import sys
import grpc
import queue
import logging
import argparse
import threading
from concurrent import futures 
from flask import Flask, render_template, request, jsonify

# Add the path to where the protobuf files are located
sys.path.append('./protos')
import protos.chat_pb2 as chat_pb2
import protos.chat_pb2_grpc as chat_pb2_grpc

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="P2P Chat Application")
    parser.add_argument('--local_port', type=int, help="Local gRPC server port")
    parser.add_argument('--target_ip', type=str, default="localhost", help="Target peer's IP address")
    parser.add_argument('--target_port', type=int, help="Target peer's gRPC port")
    parser.add_argument('--flask_port', type=int, help="Port for the Flask web server")
    
    return parser.parse_args()

args = parse_args()

LOCAL_PORT = args.local_port  # Local gRPC server port
TARGET_IP = args.target_ip  # Target peer's IP address
TARGET_PORT = args.target_port  # Target peer's gRPC port
FLASK_PORT = args.flask_port  # Port for the Flask web server
MESSAGE_QUEUE = queue.Queue()  # A queue to store incoming messages

app = Flask("P2P Chat")

# Define the Chat service by implementing the gRPC interface
class ChatService(chat_pb2_grpc.ChatServiceServicer):
    # Implement the Chat method to handle streaming chat messages
    def Chat(self, request_iterator, context):
        for message in request_iterator:  # Loop over incoming messages from the request stream
            print(f"Received message: {message.message}")
            MESSAGE_QUEUE.put((message.user, message.message))  # Put the received message in the message queue for retrieval by Flask
            yield message

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)  # Register the ChatService to the gRPC server
    server.add_insecure_port(f'[::]:{LOCAL_PORT}')
    server.start()
    print(f"Server  gRPC started on port {LOCAL_PORT}")
    return server

def send_message_to_peer(user, message, message_queue):
    # Define an iterator to stream outgoing messages
    def message_stream():
        yield chat_pb2.ChatMessage(user=user, message=message)  # Send only the initial message
    
    with grpc.insecure_channel(f'{TARGET_IP}:{TARGET_PORT}') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        # Send the message stream to the peer
        response_iterator = stub.Chat(message_stream())  # Open bidirectional streaming
        
        for reply in response_iterator:  # Iterate over incoming replies
            print(f"Received from peer: {reply.message}")
            return reply.message  # Return the first reply received

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user = data.get('user')
    message = data.get('message')
    
    if message:
        reply = send_message_to_peer(user, message, MESSAGE_QUEUE)  # Send the message to the peer via gRPC
        return jsonify({'user': user, 'reply': reply})  # Return the peer's reply as a JSON response
    return jsonify({'error': 'Message not sent'}), 400

@app.route('/receive_message', methods=['GET'])
def receive_message():
    try:
        # Try to get a message from the queue with a timeout
        user, message = MESSAGE_QUEUE.get(timeout=1)
        return jsonify({'user': user, 'message': message}), 200
    except queue.Empty:
        # Return a 204 status when no messages are available
        return jsonify({'message': None}), 204

def serve_flask():
    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False, port=FLASK_PORT, host="0.0.0.0")
    print(f"Server FLask started on port {FLASK_PORT}")

def serve_grpc():
    print("Starting gRPC server...")
    server = start_server()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()

    grpc_thread = threading.Thread(target=serve_grpc)
    flask_thread = threading.Thread(target=serve_flask)

    grpc_thread.start()
    flask_thread.start()

    grpc_thread.join()
    flask_thread.join()
