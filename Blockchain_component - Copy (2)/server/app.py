import base64
import json
import zipfile
from io import BytesIO

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from web3 import Web3

app = Flask(__name__)
CORS(app)

# Connect to Ethereum (Ganache or Infura)
WEB3_PROVIDER = "http://127.0.0.1:7545"  # Update if using Infura or Alchemy
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

# ✅ Fix: Use `.is_connected()` instead of `.isConnected()`
if not web3.is_connected():
    print("❌ ERROR: Web3 connection failed. Ensure Ganache is running.")
    exit()

# Smart contract details
CONTRACT_ADDRESS = "0x70eF2ba8450DD30b1Cd08670730a2cB1D7A3053E"
SENDER_ACCOUNT = web3.eth.accounts[0]  # Ensure this is the correct account

# ✅ Replace with actual ABI from build/contracts/DataStorage.json
CONTRACT_ABI = json.loads("""
[
  {
    "inputs": [],
    "name": "getZipFile",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_zipData",
        "type": "string"
      }
    ],
    "name": "storeZipFile",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
""")

# Load the contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Function to zip a file and encode it to Base64
def zip_file(file):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("vehicle_data.xlsx", file.read())  # Save Excel inside ZIP
    zip_buffer.seek(0)
    return base64.b64encode(zip_buffer.getvalue()).decode("utf-8")

# Function to decode Base64 ZIP and extract Excel
def decode_zip(base64_data):
    zip_buffer = BytesIO(base64.b64decode(base64_data))
    with zipfile.ZipFile(zip_buffer, "r") as zipf:
        extracted_file = zipf.open("vehicle_data.xlsx")
        return BytesIO(extracted_file.read())

# API to store ZIP file on blockchain
@app.route("/store", methods=["POST"])
def store():
    try:
        if "file" not in request.files:
            print("❌ ERROR: No file uploaded")
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        print(f"✅ Received file: {file.filename}")

        encoded_zip = zip_file(file)
        print(f"✅ Encoded ZIP size: {len(encoded_zip)} bytes")

        # Check ETH balance
        balance = web3.eth.get_balance(SENDER_ACCOUNT)
        if balance < web3.to_wei(0.01, "ether"):
            return jsonify({"error": "Not enough ETH to store data"}), 400

        # Send transaction to smart contract
        tx_hash = contract.functions.storeZipFile(encoded_zip).transact({
            "from": SENDER_ACCOUNT,
            "gas": 3000000
        })
        web3.eth.wait_for_transaction_receipt(tx_hash)

        print("✅ Transaction successful:", tx_hash.hex())

        return jsonify({"message": "File stored on blockchain"}), 200
    except Exception as e:
        print("❌ ERROR:", str(e))  # Log the actual error
        return jsonify({"error": str(e)}), 500

# API to retrieve ZIP from blockchain and extract Excel file
@app.route("/retrieve", methods=["GET"])
def retrieve():
    try:
        encoded_zip = contract.functions.getZipFile().call()
        excel_file = decode_zip(encoded_zip)

        return send_file(excel_file, download_name="retrieved_vehicle_data.xlsx", as_attachment=True)
    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
