FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /usr/local/app

# Copy in the source code and the startup script
COPY . .

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the startup script has execute permissions
RUN chmod +x ./start_clients.sh

# Expose the necessary ports
EXPOSE 50050
EXPOSE 50051
EXPOSE 5000
EXPOSE 5001

# Run the script to start both clients
CMD ["./start_clients.sh"]
