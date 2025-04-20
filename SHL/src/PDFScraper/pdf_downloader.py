import requests
from pathlib import Path

# Define the path
directory_path = Path("./downloadedPDFs")

# Create the directory (and any parent folders)
directory_path.mkdir(parents=True, exist_ok=True)

print(f"Directory created at: {directory_path}")


url = "https://service.shl.com/docs/Fact%20Sheet_%20Agency%20Manager%20Solution%20One%20Sitting_USE.pdf"
file_path = "./downloadedPDFs/Agency_Manager_Fact_Sheet.pdf"  # Change to your desired path

response = requests.get(url)

with open(file_path, "wb") as f:
    f.write(response.content)

print(f"PDF downloaded successfully to {file_path}")
