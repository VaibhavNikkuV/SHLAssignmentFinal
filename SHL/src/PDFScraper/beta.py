import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Create download folder
DOWNLOAD_FOLDER = 'downloadedPDF'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Regex to match specific SHL PDF links
PDF_PATTERN = re.compile(r'https://service\.shl\.com/docs/[^"\s>]+\.pdf')


def extract_urls_from_excel(file_path: str, url_column: str) -> list:
    """Extracts URLs from a given Excel file."""
    try:
        print("Reading Excel file...")
        df = pd.read_excel(file_path)
        return df[url_column].dropna().tolist()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []


def extract_pdf_links_from_url(page_url: str) -> list:
    """Extracts matching SHL PDF links from the HTML content of a URL."""
    try:
        print(f"Fetching {page_url}...")
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return PDF_PATTERN.findall(text)
    except Exception as e:
        print(f"Error fetching {page_url}: {e}")
        return []


def download_pdf(pdf_url: str, folder: str = DOWNLOAD_FOLDER):
    """Downloads a PDF from the given URL to the specified folder."""
    try:
        print(f"Downloading {pdf_url}...")
        filename = os.path.basename(pdf_url)
        filepath = os.path.join(folder, filename)

        if os.path.exists(filepath):
            print(f"Skipped (already exists): {filename}")
            return

        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")


def process_excel_files(excel_files: list, url_column: str):
    """Processes multiple Excel files, extracts PDF links, and downloads them."""
    all_matched_pdfs = []

    for file in excel_files:
        print(f"\nProcessing file: {file}")
        urls = extract_urls_from_excel(file, url_column=url_column)

        for url in urls:
            pdf_links = extract_pdf_links_from_url(url)
            all_matched_pdfs.extend(pdf_links)

            for pdf_url in pdf_links:
                download_pdf(pdf_url)

    print("\nAll matched PDF URLs:")
    for pdf in all_matched_pdfs:
        print(pdf)


# Example usage
if __name__ == '__main__':
    excel_files = [
        'C:\\Users\\admin\\Desktop\\Personal\\SHL\\src\\productURLscraper\\product_catalog_urls_type1.xlsx',
        'C:\\Users\\admin\\Desktop\\Personal\\SHL\\src\\productURLscraper\\product_catalog_urls_type2.xlsx'
    ]

    process_excel_files(excel_files, url_column='Product URLs')  # Adjust column name if needed
    print("Process completed.")
