import sys
import grpc
import queue
import logging
import threading
from concurrent import futures 
from flask import Flask, render_template, request, jsonify

# Add the path to where the protobuf files are located
sys.path.append('./protos')
import protos.chat_pb2 as chat_pb2
import protos.chat_pb2_grpc as chat_pb2_grpc

LOCAL_PORT = 50050  # Local gRPC server port
TARGET_IP = "localhost"  # Target peer's IP address
TARGET_PORT = 50051  # Target peer's gRPC port
FLASK_PORT = 5000  # Port for the Flask web server
MESSAGE_QUEUE = queue.Queue()  # A queue to store incoming messages 

app = Flask("P2P Chat")

# Define the Chat service by implementing the gRPC interface
class ChatService(chat_pb2_grpc.ChatServiceServicer):
    # Implement the Chat method to handle streaming chat messages
    def Chat(self, request_iterator, context):
        for message in request_iterator: # Loop over incoming messages from the request stream
            print(f"Received message: {message.message}")
            MESSAGE_QUEUE.put((message.user, message.message)) # Put the received message in the message queue for retrieval by Flask
            yield message

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server) # Register the ChatService to the gRPC server
    server.add_insecure_port(f'[::]:{LOCAL_PORT}')
    server.start()
    print(f"Server started on port {LOCAL_PORT}")
    return server

# Function to send a message to a peer via gRPC
def send_message_to_peer(user, message):
    with grpc.insecure_channel(f'{TARGET_IP}:{TARGET_PORT}') as channel: # Create a gRPC channel to communicate with the target peer
        stub = chat_pb2_grpc.ChatServiceStub(channel) # Create a stub (client) to access the Chat service on the target peer
        response = stub.Chat(iter([chat_pb2.ChatMessage(user=user, message=message)])) # Send the message to the target peer using the Chat method and stream the response
        for reply in response:
            return reply.message # Retrieve and return the reply message from the peer

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json() 
    user = data.get('user')
    message = data.get('message')
    
    if message:
        reply = send_message_to_peer(user, message) # Send the message to the peer via gRPC
        return jsonify({'user': user, 'reply': reply}) # Return the peer's reply as a JSON response
    return jsonify({'error': 'Message not sent'}), 400  

@app.route('/receive_message', methods=['GET'])
def receive_message():
    if not MESSAGE_QUEUE.empty():
        user, message = MESSAGE_QUEUE.get()
        return jsonify({'user': user, 'message': message})
    return jsonify({'message': None}), 204

def serve_flask():
    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False, port=FLASK_PORT, host="0.0.0.0")

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