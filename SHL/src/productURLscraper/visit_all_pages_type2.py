import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def visit_all_catalog_pages(base_url, type_id):
    start = 0
    page_number = 2
    all_product_urls = []

    while True:
        # Construct URL depending on the page number
        if page_number == 2:
            url = f"{base_url}?start=12&type={type_id}"
        else:
            url = f"{base_url}?start={start}&type={type_id}&type={type_id}"

        print(f"\nVisiting page {page_number}: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        product_entries = soup.select('a[href*="/solutions/products/product-catalog/view/"]')

        if not product_entries:
            print(f"No products found on page {page_number}. Ending pagination.")
            break

        for entry in product_entries:
            href = entry.get('href')
            if href:
                full_url = requests.compat.urljoin(base_url, href)
                all_product_urls.append(full_url)
                print(f"Found product URL: {full_url}")

        start += 12
        page_number += 1
        time.sleep(1)

    return all_product_urls


if __name__ == "__main__":
    base_url = "https://www.shl.com/solutions/products/product-catalog/"

    # Scrape product URLs for both types
    urls_type2 = visit_all_catalog_pages(base_url, type_id=2)

    # Create DataFrames for each type
    df_type2 = pd.DataFrame({'Product URLs': urls_type2})

    # Write to Excel with separate sheets
    output_file = "product_catalog_urls_type2.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_type2.to_excel(writer, sheet_name='Type 2 Products', index=False)

    print(f"\n✅ URLs saved to '{output_file}' in separate sheets.")
