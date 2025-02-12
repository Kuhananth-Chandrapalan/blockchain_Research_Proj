import pandas as pd
import base64
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# Load Pretrained Model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Encode Function
def encode_data(data):
    encoded_data = []
    for _, row in data.iterrows():
        combined = f"{row['License Plate']}|{row['Timestamp']}|{row['Vehicle Type']}"
        inputs = tokenizer(combined, return_tensors="pt", max_length=50, truncation=True, padding="max_length")
        with torch.no_grad():
            embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().numpy()
        encoded_string = base64.b64encode(embeddings.tobytes()).decode("utf-8")
        encoded_data.append(encoded_string)
    return encoded_data

# Decode Function
def decode_data(encoded_data):
    decoded_data = []
    for encoded_row in encoded_data:
        binary_data = base64.b64decode(encoded_row)
        # Reverse logic or mock decoding (This should match your logic)
        license_plate, timestamp, vehicle_type = "Mock_License", "Mock_Timestamp", "Mock_Type"
        decoded_data.append({
            "License Plate": license_plate,
            "Timestamp": timestamp,
            "Vehicle Type": vehicle_type
        })
    return pd.DataFrame(decoded_data)
