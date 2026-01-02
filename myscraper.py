# import requests
# from bs4 import BeautifulSoup
# import csv
# from datetime import datetime

# # 1. Configuration - Easy to change later
# URL = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
# CSV_FILE = "price_log.csv"
# BUDGET_THRESHOLD = 20.00  # Alert if price is below this

# def run_automation():
#     print(f"--- Workflow Started: {datetime.now()} ---")
    
#     # Setup headers to look like a real user
#     headers = {"User-Agent": "Mozilla/5.0"}
    
#     try:
#         # Step 1: Fetch Data
#         response = requests.get(URL, headers=headers)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         books = soup.find_all('article', class_='product_pod')

#         # Step 2: Prepare for Saving
#         with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             if f.tell() == 0:
#                 writer.writerow(["Timestamp", "Title", "Price", "Status"])

#             # Step 3: Loop through and Apply Logic
#             for book in books:
#                 title = book.h3.a['title']
#                 price_raw = book.find('p', class_='price_color').text
#                 price = float(price_raw.replace('£', '').replace('$', ''))
#                 timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

#                 # Logic: Is it a deal?
#                 status = "Normal"
#                 if price <= BUDGET_THRESHOLD:
#                     status = "🔥 ALERT: CHEAP"
#                     print(f"NOTIFICATION: {title} dropped to £{price}!")

#                 # Step 4: Save to History
#                 writer.writerow([timestamp, title, price, status])

#         print(f"--- Workflow Complete: Data saved to {CSV_FILE} ---")

#     except Exception as e:
#         print(f"Error during execution: {e}")

# if __name__ == "__main__":
#     run_automation()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def scrape_ecommerce():
    # 1. Setup Chrome options to look 'human'
    options = Options()
    # options.add_argument("--headless") # Uncomment this to run without a window opening
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 2. Initialize the Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Change this URL to a specific Amazon or Flipkart product search page
    TARGET_URL = "https://www.amazon.com/s?k=laptop" 
    
    try:
        driver.get(TARGET_URL)
        time.sleep(3) # Wait for JavaScript to load

        # 3. Locate Product Containers (Amazon uses 's-result-item')
        products = driver.find_elements(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')

        with open('market_data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Product Name", "Price", "Link"])

            for product in products[:10]: # Let's grab the top 10 results
                try:
                    # Amazon-specific selectors
                    name = product.find_element(By.TAG_NAME, 'h2').text
                    price_whole = product.find_element(By.CLASS_NAME, 'a-price-whole').text
                    link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    
                    writer.writerow([name, price_whole, link])
                    print(f"Found: {name[:50]}... | Price: ${price_whole}")
                except:
                    continue # Skip products that don't have a price listed

    finally:
        driver.quit()
        print("Scraping finished. Data saved to market_data.csv")

if __name__ == "__main__":
    scrape_ecommerce()