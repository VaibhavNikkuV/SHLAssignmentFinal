import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os



def visit_all_catalog_pages(base_url, type_id):
    start = 0
    page_number = 2
    extracted_data = []

    while True:
        if page_number == 1:
            url = base_url
        elif page_number == 2:
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
            raw_html = str(entry)
            match = re.search(r'<a href="([^"]+)">([^<]+)</a>', raw_html)
            if match:
                relative_link = match.group(1)
                name = match.group(2).strip()
                full_url = requests.compat.urljoin(base_url, relative_link)
                extracted_data.append({'Name': name, 'URL': full_url})
                print(f"Found: {name} -> {full_url}")

        start += 12
        page_number += 1
        time.sleep(1)

    return extracted_data


if __name__ == "__main__":
    base_url = "https://www.shl.com/solutions/products/product-catalog/"

    data_type2 = visit_all_catalog_pages(base_url, type_id=2)

    df_type2 = pd.DataFrame(data_type2)

    # Create a directory named 'my_directory'
    os.makedirs("Saved name and URLs", exist_ok=True)  # `exist_ok=True` avoids error if dir already exists


    output_file = "./Saved name and URLs/product_catalog_names_and_urls_type2.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_type2.to_excel(writer, sheet_name='Type 2 Products', index=False)

    print(f"\n✅ Product names and URLs saved to '{output_file}' in separate sheets.")
