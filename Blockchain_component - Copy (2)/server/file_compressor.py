import base64
import zipfile
from io import BytesIO


def zip_file(file_path):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        with open(file_path, "rb") as f:
            zipf.writestr(file_path, f.read())
    zip_buffer.seek(0)
    return base64.b64encode(zip_buffer.getvalue()).decode("utf-8")

def unzip_file(base64_data, output_filename):
    zip_buffer = BytesIO(base64.b64decode(base64_data))
    with zipfile.ZipFile(zip_buffer, "r") as zipf:
        extracted_file = zipf.open(output_filename)
        return extracted_file.read()

if __name__ == "__main__":
    compressed_data = zip_file("vehicle_data.xlsx")
    print("Compressed ZIP (Base64):", compressed_data[:100], "...")  # Show a preview
