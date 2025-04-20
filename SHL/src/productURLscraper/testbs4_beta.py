import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Selenium WebDriver
options = Options()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=options)

def extract_urls_from_page(url):
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', href=True)
    product_urls = [link['href'] for link in links if re.match(r"/solutions/products/product-catalog/view/[a-z0-9\-]+/", link['href'])]
    return product_urls

def get_all_product_urls(base_url):
    all_urls = set()
    page_number = 0

    while True:
        paginated_url = f"{base_url}?start={page_number * 12}&type=1"
        product_urls = extract_urls_from_page(paginated_url)
        if not product_urls:
            break
        all_urls.update(product_urls)
        page_number += 1
        time.sleep(1.5)  # Respectful delay

    return list(all_urls)

# Main execution
base_url = 'https://www.shl.com/solutions/products/product-catalog/'
product_urls = get_all_product_urls(base_url)

# Save to Excel
df = pd.DataFrame({'Product URLs': product_urls})
df.to_excel("shl_product_urls.xlsx", index=False)

# Clean up
driver.quit()
