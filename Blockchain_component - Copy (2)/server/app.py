from flask import Flask, request, jsonify
import pandas as pd
import base64
import torch
from transformers import AutoTokenizer, AutoModel
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Data Encoding Function
def encode_data(data):
    encoded_data = []
    for _, row in data.iterrows():
        # Combine fields into a single string
        combined = f"{row['License Plate']}|{row['Timestamp']}|{row['Vehicle Type']}"
        
        # Use transformer model for encoding
        inputs = tokenizer(combined, return_tensors="pt", max_length=50, truncation=True, padding="max_length")
        with torch.no_grad():
            embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().numpy()

        # Convert embeddings to Base64 string
        encoded_string = base64.b64encode(embeddings.tobytes()).decode("utf-8")
        encoded_data.append(encoded_string)
    return encoded_data

# Data Decoding Function
def decode_data(encoded_data):
    decoded_data = []
    try:
        for encoded_row in encoded_data:
            # Decode Base64 string to binary
            binary_data = base64.b64decode(encoded_row)
            
            # Mock decoding logic (update with real logic if available)
            license_plate, timestamp, vehicle_type = "MockLP", "MockTime", "MockType"
            decoded_data.append({
                "License Plate": license_plate,
                "Timestamp": timestamp,
                "Vehicle Type": vehicle_type
            })
        return pd.DataFrame(decoded_data)
    except Exception as e:
        raise ValueError(f"Decoding Error: {e}")

@app.route("/encode", methods=["POST"])
def encode():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    try:
        data = pd.read_csv(file)
        required_columns = ["License Plate", "Timestamp", "Vehicle Type"]
        if not all(col in data.columns for col in required_columns):
            return jsonify({"error": "Invalid file format"}), 400

        encoded_data = encode_data(data)
        return jsonify({"encodedData": encoded_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/decode", methods=["POST"])
def decode():
    try:
        encoded_data = request.json.get("encodedData", [])
        if not encoded_data:
            return jsonify({"error": "No encoded data provided"}), 400

        decoded_data = decode_data(encoded_data)
        return jsonify({"decodedData": decoded_data.to_dict(orient="records")}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
