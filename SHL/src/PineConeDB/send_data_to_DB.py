import os
import uuid
import time
import re
import cohere
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_HOST)

# Path to the log file
LOG_FILE = "processed_txt_files.log"

def read_text_file(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def chunk_text(text, max_length=400):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def load_processed_files():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def mark_file_as_processed(filename):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{filename}\n")

def process_txt(txt_path):
    text = read_text_file(txt_path)
    chunks = chunk_text(text)
    print(f"Processing '{os.path.basename(txt_path)}' with {len(chunks)} chunks.")

    # Generate embeddings
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embeddings = response.embeddings

    vectors = []
    for i, embedding in enumerate(embeddings):
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {
                "source": os.path.basename(txt_path),
                "chunk_index": i,
                "text": chunks[i]
            }
        })

    time.sleep(2)
    index.upsert(vectors=vectors)
    print(f"✅ Uploaded {len(vectors)} vectors from '{os.path.basename(txt_path)}' to Pinecone.")
    mark_file_as_processed(os.path.basename(txt_path))

if __name__ == "__main__":
    txt_directory = input("Input .txt folder path: ").strip()
    processed_files = load_processed_files()
    for filename in os.listdir(txt_directory):
        if filename.endswith(".txt") and filename not in processed_files:
            txt_path = os.path.join(txt_directory, filename)
            try:
                process_txt(txt_path)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
