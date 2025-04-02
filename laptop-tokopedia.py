import time
import csv
import re
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TOTAL_PAGES = 85

url = 'https://www.tokopedia.com/search?st=&q=laptop&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='

options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("--disable-gpu") 
options.add_argument("--no-sandbox") 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "css-5wh65g"))
)

products = []
seen_products = set() 

page = 1
while page <= TOTAL_PAGES:
    print(f"Scraping halaman {page}...")

    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 1200);")
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    container_class = soup.find_all("div", class_="css-5wh65g")

    for container in container_class:
        product_name = container.find("span", class_="_0T8-iGxMpV6NEsYEhwkqEg==")
        price_list = container.find("div", class_="_67d6E1xDKIzw+i2D2L0tjw==")
        rating = container.find("span", class_="_9jWGz3C-GX7Myq-32zWG9w==")
        terjual = container.find("span", class_="se8WAnkjbVXZNA8mT+Veuw==")
        toko = container.find("span", class_="T0rpy-LEwYNQifsgB-3SQw== pC8DMVkBZGW7-egObcWMFQ== flip")
        lokasi = container.find("span", class_="pC8DMVkBZGW7-egObcWMFQ== flip")

        product_name = product_name.text.strip() if product_name else "Tidak Ada Nama"
        price_list = price_list.text.strip() if price_list else "Tidak Ada Harga"
        rating = rating.text.strip() if rating else "Tidak Ada Rating"
        terjual = terjual.text.strip() if terjual else "Tidak Ada Data"
        toko = toko.text.strip() if toko else "Tidak Ada Data"
        lokasi = lokasi.text.strip() if lokasi else "Tidak Ada lokasi"

        price_list = re.sub(r'[^0-9]', '', price_list)
        price_list = int(price_list) if price_list.isdigit() else 0

        if (product_name, price_list) not in seen_products:
            seen_products.add((product_name, price_list))
            products.append([product_name, price_list, rating, terjual, toko, lokasi])
    
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Laman berikutnya']"))
        )
        next_button.click()
        time.sleep(2)
    except:
        print("Tombol Next tidak ditemukan atau sudah di halaman terakhir.")
        break

    page += 1

products.sort(key=lambda x: x[1], reverse=True)

with open("datalaptop2.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["No", "Nama Produk", "Harga", "Rating", "Terjual", "Toko", "Lokasi"])
    for i, product in enumerate(products, start=1):
        writer.writerow([i] + product)

driver.quit()
print("Scraping selesai! Data disimpan di datalaptoptokopedia.csv")

kategori = {
    "Di bawah 5 juta": 0,
    "5 - 10 juta": 0,
    "10 - 20 juta": 0,
    "Di atas 20 juta": 0
}

for product in products:
    harga = product[1]
    if harga < 5000000:
        kategori["Di bawah 5 juta"] += 1
    elif 5000000 <= harga < 10000000:
        kategori["5 - 10 juta"] += 1
    elif 10000000 <= harga < 20000000:
        kategori["10 - 20 juta"] += 1
    else:
        kategori["Di atas 20 juta"] += 1

plt.figure(figsize=(8, 8))
plt.pie(kategori.values(), labels=kategori.keys(), autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], startangle=90)
plt.title("Distribusi Harga Laptop")
plt.savefig("diagram_lingkaran.png")
plt.show()
