import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import fitz  # PyMuPDF

load_dotenv()

# Load API key
api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain LLM
llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)

# PDF file info
pdf_path = "./test/_NET_WPF_New__Product_Fact_Sheet_file_1.pdf"
actual_filename = os.path.basename(pdf_path)

# Extract text from PDF
with fitz.open(pdf_path) as doc:
    pdf_text = "\n".join(page.get_text() for page in doc)

# Prepare prompt
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

# Run LLM
response = llm.invoke([system_msg, user_msg])
response_text = response.content.strip()

# ✅ Clean markdown-style JSON fencing if present
if response_text.startswith("```json"):
    response_text = response_text[7:]
if response_text.endswith("```"):
    response_text = response_text[:-3]
response_text = response_text.strip()

# ✅ Try to parse the cleaned JSON
try:
    data = json.loads(response_text)

    # ✅ Fix file_name using slicing (not os.path.basename)
    if "file_name" in data:
        file_name = data["file_name"]
        last_slash = max(file_name.rfind("/"), file_name.rfind("\\"))
        data["file_name"] = file_name[last_slash + 1:] if last_slash != -1 else file_name

    # ✅ Output final clean JSON
    print(json.dumps(data, indent=2))

except json.JSONDecodeError:
    print("❌ Failed to parse JSON from cleaned response.")
    print(response_text)
