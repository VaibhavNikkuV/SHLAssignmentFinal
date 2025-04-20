import json
import pandas as pd
import re
import time
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
load_dotenv()

FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

main_URL = 'https://www.shl.com/solutions/products/product-catalog/'

main_page_URL = []
type1_URL = []
type2_URL = []

# Extract URL's from first page
main_page_json = app.scrape_url(url=main_URL, params={
	'formats': [ 'markdown' ],
})

def extract_url_from_json(data):
    json_str = json.dumps(data)
    urls = re.findall(r"https:\/\/www\.shl\.com\/solutions\/products\/product-catalog\/view\/[a-z0-9\-]+\/", json_str)
    unique_urls = list(set(urls))
    return unique_urls

main_page_URL = extract_url_from_json(main_page_json)


# Extracting URL's from type 1
def visit_all_catalog_pages_type1(base_url):
    start = 0
    page_number = 2
    urls = []

    while True:
        # Determine the URL based on the page number
        if page_number == 1:
            url = base_url
        elif page_number == 2:
            url = f"{base_url}?start=12&type=1"
        else:
            url = f"{base_url}?start={start}&type=1&type=1"

        print(f"\nVisiting page {page_number}: {url}")
        time.sleep(7)  # Add a delay of 7 seconds


        # Scrape the URL and extract the JSON data
        json_data = app.scrape_url(url=url, params={
            'formats': ['markdown'],
        })

        extracted_urls = extract_url_from_json(json_data)

        if not extracted_urls:
            break

        urls.extend(extracted_urls)

        start += 12
        page_number += 1

    return list(set(urls))


type1_URL = visit_all_catalog_pages_type1(main_URL)


# Extracting URL's from type 2
def visit_all_catalog_pages_type2(base_url):
    start = 0
    page_number = 2
    urls = []

    while True:
        # Determine the URL based on the page number
        if page_number == 1:
            url = base_url
        elif page_number == 2:
            url = f"{base_url}?start=12&type=2"
        else:
            url = f"{base_url}?start={start}&type=2&type=2"

        print(f"\nVisiting page {page_number}: {url}")
        time.sleep(7)  # Add a delay of 7 seconds


        # Scrape the URL and extract the JSON data
        json_data = app.scrape_url(url=url, params={
            'formats': ['markdown'],
        })

        extracted_urls = extract_url_from_json(json_data)

        if not extracted_urls:
            break

        urls.extend(extracted_urls)

        start += 12
        page_number += 1

    return list(set(urls))


type2_URL = visit_all_catalog_pages_type2(main_URL)


all_URL = list(set(main_page_URL + type1_URL + type2_URL))

df = pd.DataFrame({'Product URLs': all_URL})
output_filename = "shl_product_urls.xlsx"
df.to_excel(output_filename, index=False)

print(f"\n✅ Saved {len(all_URL)} unique URLs to '{output_filename}'")