from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

url = 'https://www.tokopedia.com/p/makanan-minuman/makanan-kering'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(url)

data = []

for i in range(50): 
    # Tunggu sampai elemen produk muncul
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-16vw0vn"))
    )
    
    # Parse halaman dengan BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    containers = soup.find_all('div', class_='css-16vw0vn')  
    
    for idx, container in enumerate(containers, start=len(data) + 1):
        try:
            title = container.find('span', class_='css-20kt3o').text
            data.append([idx, title])  # Menyimpan data dalam format tabel (list of lists)
        except AttributeError:
            continue  # Skip jika elemen tidak ditemukan
        
    # Tunggu sebelum klik tombol berikutnya
    time.sleep(15)
    
    # Klik tombol "Laman Berikutnya" jika ada
    try:
        next_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label^="Laman berikutnya"]'))
        )
        next_button.click()
    except Exception as e:
        print(f"Gagal klik halaman berikutnya: {e}")
        break
    
    time.sleep(3)

# Tutup WebDriver setelah selesai
driver.quit()

# Cek apakah data kosong sebelum menampilkan
if data:
    for idx, item in enumerate(data, start=1):
        print(f"{item}")
else:
    print("Tidak ada data yang berhasil diambil.")
