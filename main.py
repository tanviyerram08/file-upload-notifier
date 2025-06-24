from flask import Flask, request
import base64
import json
import logging
import os

app = Flask(__name__)

# Setup logger
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["POST"])
def index():
    try:
        # Print raw body
        raw_body = request.get_data(as_text=True)
        logging.info(f"🔍 RAW REQUEST BODY:\n{raw_body}")

        # Try to parse JSON
        envelope = request.get_json()
        if not envelope:
            logging.warning("❌ No JSON received")
            return "Bad Request: No JSON", 400

        # Log full envelope
        logging.info(f"📦 JSON envelope:\n{json.dumps(envelope, indent=2)}")

        # Get the Pub/Sub message
        message = envelope.get("message")
        if not message or "data" not in message:
            logging.warning("❌ No 'message.data' found in request")
            return "Bad Request: Malformed message", 400

        # Decode and parse the actual event payload
        payload_json = base64.b64decode(message["data"]).decode("utf-8")
        logging.info(f"📄 Decoded payload: {payload_json}")

        payload = json.loads(payload_json)
        filename = payload.get("name")
        bucket = payload.get("bucket")
        logging.info(f"📁 File uploaded: {filename} in bucket {bucket}")

        return "OK", 200

    except Exception as e:
        logging.error(f"❌ Exception occurred: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
