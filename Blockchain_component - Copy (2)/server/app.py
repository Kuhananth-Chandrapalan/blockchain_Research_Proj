import base64
import json
import zipfile
from io import BytesIO

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from web3 import Web3

app = Flask(__name__)
CORS(app)

WEB3_PROVIDER = "http://127.0.0.1:7545"  
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

if not web3.is_connected():
    print("❌ ERROR: Web3 connection failed. Ensure Ganache is running.")
    exit()

CONTRACT_ADDRESS = "0xed257163E7688a7100ff4CA3dF3AAC9624b29088"  # Replace with your latest deployed contract
SENDER_ACCOUNT = web3.eth.accounts[0]  

CONTRACT_ABI = json.loads("""
[
  {
    "inputs": [],
    "name": "getFileNames",
    "outputs": [
      {
        "internalType": "string[]",
        "name": "",
        "type": "string[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_fileId",
        "type": "uint256"
      }
    ],
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
        "name": "_fileName",
        "type": "string"
      },
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

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def zip_file(file, file_name):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(file_name, file.read())  
    zip_buffer.seek(0)
    return base64.b64encode(zip_buffer.getvalue()).decode("utf-8")

def decode_zip(base64_data, file_name):
    zip_buffer = BytesIO(base64.b64decode(base64_data))
    with zipfile.ZipFile(zip_buffer, "r") as zipf:
        extracted_file = zipf.open(file_name)
        return BytesIO(extracted_file.read())

@app.route("/store", methods=["POST"])
def store():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        file_name = file.filename  
        encoded_zip = zip_file(file, file_name)

        tx_hash = contract.functions.storeZipFile(file_name, encoded_zip).transact({
            "from": SENDER_ACCOUNT,
            "gas": 3000000
        })
        web3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({"message": "File stored on blockchain"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list", methods=["GET"])
def list_files():
    try:
        file_names = contract.functions.getFileNames().call()
        return jsonify({"files": file_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/retrieve/<int:file_id>", methods=["GET"])
def retrieve(file_id):
    try:
        encoded_zip = contract.functions.getZipFile(file_id).call()
        file_names = contract.functions.getFileNames().call()

        if file_id >= len(file_names):
            return jsonify({"error": "Invalid file ID"}), 400

        excel_file = decode_zip(encoded_zip, file_names[file_id])
        return send_file(excel_file, download_name=file_names[file_id], as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
