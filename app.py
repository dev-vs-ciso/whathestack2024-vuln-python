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
    try:
        data = request.get_json(force=True)  # Force parsing JSON, raise error if not valid
        if not data:
            raise ValueError("No data received")

        # Get the X-Forwarded-For IP address
        x_forwarded_for = request.headers.get('X-Forwarded-For', None)
        # Get the original IP address
        original_ip = request.remote_addr

        # Logging
        logger.info(f"Data received from client: {data}")
        logger.info(f"X-Forwarded-For IP: {x_forwarded_for}")
        logger.info(f"Original IP: {original_ip}")

        response_data = {
            "status": "success",
            "message": "Data received successfully",
            "details": data,
            "x_forwarded_for_ip": x_forwarded_for,
            "original_ip": original_ip
        }
        logger.info(f"Sending data to CC server: {response_data}")
        return jsonify(response_data)

    except ValueError as e:
        logger.error(f"Error in processing request: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
