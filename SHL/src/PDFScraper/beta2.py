import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import unquote

# Folder to save PDFs
DOWNLOAD_FOLDER = Path("./downloadedPDFs")
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Regex to match SHL PDF links
PDF_PATTERN = re.compile(r'https://service\.shl\.com/docs/[^"\s>]+\.pdf')


def extract_urls_from_excel(file_path: str, url_column: str) -> list:
    """Extracts URLs from a given Excel file."""
    try:
        print(f"Reading Excel file: {file_path}")
        df = pd.read_excel(file_path)
        return df[url_column].dropna().tolist()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []


def extract_pdf_links_from_url(page_url: str) -> list:
    """Extracts matching SHL PDF links from anchor tags on a webpage."""
    try:
        print(f"🔎 Fetching: {page_url}")
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return [link for link in links if PDF_PATTERN.match(link)]
    except Exception as e:
        print(f"❌ Error fetching {page_url}: {e}")
        return []


def download_pdf(pdf_url: str, folder: Path = DOWNLOAD_FOLDER):
    """Downloads a PDF from the given URL to the specified folder with cleaned filename."""
    try:
        print(f"⬇️  Downloading: {pdf_url}")
        
        # Clean up filename
        original_name = Path(pdf_url).name
        decoded_name = unquote(original_name)           # Decode %20 etc.
        cleaned_name = decoded_name.replace(" ", "_")   # Replace spaces with _
        
        filepath = folder / cleaned_name

        if filepath.exists():
            print(f"✅ Skipped (already exists): {cleaned_name}")
            return

        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()
        filepath.write_bytes(response.content)
        print(f"✅ Downloaded: {cleaned_name}")

    except Exception as e:
        print(f"❌ Failed to download {pdf_url}: {e}")


def process_excel_files(excel_files: list, url_column: str):
    """Processes multiple Excel files, extracts PDF links, and downloads them."""
    all_matched_pdfs = []

    for file in excel_files:
        print(f"\n📄 Processing file: {file}")
        urls = extract_urls_from_excel(file, url_column=url_column)

        for url in urls:
            pdf_links = extract_pdf_links_from_url(url)
            all_matched_pdfs.extend(pdf_links)

            for pdf_url in pdf_links:
                download_pdf(pdf_url)

    print("\n📝 All matched PDF URLs:")
    for pdf in all_matched_pdfs:
        print(pdf)


# ==== Example usage ====
if __name__ == '__main__':
    excel_files = [
        r'C:\Users\admin\Desktop\Personal\SHL\src\productURLscraper\product_catalog_urls_type1.xlsx',
        r'C:\Users\admin\Desktop\Personal\SHL\src\productURLscraper\product_catalog_urls_type2.xlsx'
    ]

    process_excel_files(excel_files, url_column='Product URLs')
    print("\n🎉 All done!")
