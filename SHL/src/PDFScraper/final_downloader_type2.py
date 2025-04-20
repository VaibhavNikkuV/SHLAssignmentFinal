import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import time
import random
import os
from urllib.parse import unquote

# Folder to save PDFs
DOWNLOAD_FOLDER = Path("./downloadedPDFs")
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Regex to match SHL PDF links
PDF_PATTERN = re.compile(r'https://service\.shl\.com/docs/.*\.pdf')


def extract_urls_from_excel(file_path: str, url_column: str, name_column: str) -> list:
    """Extracts URL and Name pairs from Excel file."""
    try:
        print(f"Reading Excel file: {file_path}")
        df = pd.read_excel(file_path)
        return df[[url_column, name_column]].dropna().to_dict(orient="records")
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []


def extract_pdf_links_from_url(page_url: str, base_name: str) -> list:
    """Extracts matching SHL PDF links and names from a webpage."""
    pdf_info_list = []

    try:
        print(f"🔎 Fetching: {page_url}")
        time.sleep(random.uniform(1, 3))
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        counter = 1
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            if PDF_PATTERN.match(href):
                link_text = a.get_text(strip=True)
                pdf_info_list.append({
                    "url": href,
                    "link_name": link_text,
                    "counter": counter,
                    "prefix": base_name
                })
                counter += 1

    except Exception as e:
        print(f"❌ Error fetching {page_url}: {e}")

    return pdf_info_list


def download_pdf(pdf_entry: dict, folder: Path = DOWNLOAD_FOLDER):
    """Downloads a PDF with a formatted filename including prefix and link name."""
    try:
        pdf_url = pdf_entry["url"]
        link_name = pdf_entry["link_name"]
        count = pdf_entry["counter"]
        prefix = pdf_entry["prefix"]

        print(f"⬇️  Downloading: {pdf_url}")

        clean_prefix = re.sub(r'\W+', '_', prefix)
        clean_link_name = re.sub(r'\W+', '_', link_name)
        filename = f"{clean_prefix}_{clean_link_name}_file_{count}.pdf"

        filepath = folder / filename
        if filepath.exists():
            print(f"✅ Skipped (already exists): {filename}")
            return

        time.sleep(random.uniform(1, 3))
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()
        filepath.write_bytes(response.content)
        print(f"✅ Downloaded: {filename}")

    except Exception as e:
        print(f"❌ Failed to download {pdf_url}: {e}")


def process_excel_files(excel_files: list, url_column: str, name_column: str):
    """Processes Excel files, extracts PDF links, and downloads them with naming prefix."""
    all_matched_pdfs = []

    for file in excel_files:
        print(f"\n📄 Processing file: {file}")
        entries = extract_urls_from_excel(file, url_column=url_column, name_column=name_column)

        for entry in entries:
            url = entry[url_column]
            name_prefix = entry[name_column]

            pdf_entries = extract_pdf_links_from_url(url, base_name=name_prefix)
            all_matched_pdfs.extend([e["url"] for e in pdf_entries])

            for pdf_entry in pdf_entries:
                download_pdf(pdf_entry)

    print("\n📝 All matched PDF URLs:")
    for pdf in all_matched_pdfs:
        print(pdf)


# ==== Example usage ====
if __name__ == '__main__':
    excel_files = [
        r'C:\Users\admin\Desktop\Personal\SHL\src\productURLscraper\Saved name and URLs\product_catalog_names_and_urls_type2.xlsx'
    ]

    process_excel_files(excel_files, url_column='URL', name_column='Name')
    print("\n🎉 All done!")
