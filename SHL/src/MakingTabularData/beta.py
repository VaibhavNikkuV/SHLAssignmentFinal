import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import fitz  # PyMuPDF
import pandas as pd

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain LLM
llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)

# Prompt template
def generate_messages(pdf_text, actual_filename):
    system_msg = SystemMessage(
        content="You are an AI assistant that extracts specific information from PDF documents."
    )
    user_msg = HumanMessage(
        content=f"""
You are provided with the following text extracted from a PDF:

--- START OF DOCUMENT ---
{pdf_text}
--- END OF DOCUMENT ---

Extract the following information:
1. File name.
2. Average testing time in minutes.
3. Relevant job roles.

Return the result strictly in JSON format with the following structure:
{{
  "file_name": "{actual_filename}",
  "average_testing_time_minutes": ...,
  "relevant_job_roles": ["...", "...", ...]
}}
"""
    )
    return [system_msg, user_msg]

# Extract text from a single PDF
def extract_pdf_text(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)

# Parse JSON response safely
def parse_response(response_text):
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    try:
        data = json.loads(response_text)

        # Clean filename
        if "file_name" in data:
            file_name = data["file_name"]
            last_slash = max(file_name.rfind("/"), file_name.rfind("\\"))
            data["file_name"] = file_name[last_slash + 1:] if last_slash != -1 else file_name

        return data
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON from response:")
        print(response_text)
        return None

# Process folder of PDFs
def process_pdf_folder(folder_path, output_excel_path):
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")

            pdf_text = extract_pdf_text(pdf_path)
            messages = generate_messages(pdf_text, filename)
            response = llm.invoke(messages)
            data = parse_response(response.content.strip())

            if data:
                results.append(data)

    # Save to Excel
    if results:
        df = pd.DataFrame(results)
        df.to_excel(output_excel_path, index=False)
        print(f"✅ Excel file created: {output_excel_path}")
    else:
        print("⚠️ No valid data extracted.")

# Usage example
if __name__ == "__main__":
    folder_path = "C:/Users/admin/Desktop/Personal/SHL/src/PDFScraper/downloadedPDFs" 
    output_excel = "pdf_summary.xlsx"
    process_pdf_folder(folder_path, output_excel)
