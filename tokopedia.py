import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TOTAL_PAGES = 54

url = 'https://www.tokopedia.com/search?st=&q=laptop'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(url)

time.sleep(5)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "css-5wh65g"))
)

with open("denbagoes_laptop.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["No", "Nama Produk", "Harga", "Rating", "Terjual", "Toko"])  
    
    page = 1
    barisNomor= 1
    while page <= TOTAL_PAGES:
        print(f"Scraping halaman {page}...")

        for _ in range(5): 
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        container_class = soup.find_all("div", class_="css-5wh65g")

        for container in container_class:
            product_name = container.find("span", class_="_0T8-iGxMpV6NEsYEhwkqEg==")
            price_list = container.find("div", class_="_67d6E1xDKIzw+i2D2L0tjw==")
            rating = container.find("span", class_="_9jWGz3C-GX7Myq-32zWG9w==")
            terjual=container.find("span", class_="se8WAnkjbVXZNA8mT+Veuw==")
            toko=container.find("span", class_="T0rpy-LEwYNQifsgB-3SQw== pC8DMVkBZGW7-egObcWMFQ== flip")

            product_name = product_name.text.strip() if product_name else "Tidak Ada Nama"
            price_list = price_list.text.strip() if price_list else "Tidak Ada Harga"
            rating = rating.text.strip() if rating else "Tidak Ada Rating"
            terjual = terjual.text.strip() if terjual else "Tidak Ada Data"
            toko = toko.text.strip() if toko else "Tidak Ada Data"

            writer.writerow([barisNomor, product_name, price_list, rating, terjual, toko])
            barisNomor+=1

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Laman berikutnya']"))
            )
            next_button.click()
            time.sleep(5)
        except:
            print("Tombol Next tidak ditemukan atau sudah di halaman terakhir.")
            break 

        page += 1

# Tutup browser
driver.quit()
print("Scraping selesai! Data disimpan di tokopedia_laptop.csv")