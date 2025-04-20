import os
from pathlib import Path
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# Set up Mistral API
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise EnvironmentError("MISTRAL_API_KEY environment variable not set.")
client = Mistral(api_key=api_key)

def extract_text_from_pdf_with_mistral(pdf_path: Path) -> str:
    try:
        # Upload the PDF file to Mistral
        uploaded_pdf = client.files.upload(
            file={
                "file_name": pdf_path.name,
                "content": open(pdf_path, "rb")
            },
            purpose="ocr"
        )

        # Get the signed URL for the uploaded PDF
        signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

        # Perform OCR using the document URL
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url.url
            }
        )

        return ocr_response.text if hasattr(ocr_response, "text") else str(ocr_response)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def extract_texts_from_folder(pdf_folder_path):
    input_folder = Path(pdf_folder_path)
    if not input_folder.is_dir():
        print("Invalid folder path.")
        return

    output_folder = input_folder.parent / f"{input_folder.name}_extracted_text"
    output_folder.mkdir(exist_ok=True)
    log_file = output_folder / "processed_files.log"

    # Load already processed files
    processed_files = set()
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as log:
            processed_files = set(line.strip() for line in log)

    for file in input_folder.iterdir():
        if file.suffix.lower() == ".pdf" and file.name not in processed_files:
            print(f"Processing {file.name} with Mistral OCR...")
            text = extract_text_from_pdf_with_mistral(file)
            if text is not None:
                output_file = output_folder / f"{file.stem}.md"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(file.name + "\n")

    print(f"OCR extraction complete. Output saved in: {output_folder}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing PDFs: ").strip()
    extract_texts_from_folder(folder_path)
