from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

class AmarillasBot:

    def __init__(self) -> None:
        self.options = Options()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(options=self.options)
        
        self.url = 'https://www.paginasamarillas.es/search/nutricionistas/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/120?what=Nutricionistas'
        self.driver.get(self.url)
        
        sleep(5)

        # Intenta aceptar o rechazar las cookies si aparece el banner
        try:
            cookie_button = WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            cookie_button.click()
        except Exception as e:
            print("No cookie banner found or error occurred:", e)

    def link_nutrios(self):
        divs = self.driver.find_elements(By.XPATH, '//div[contains(@class, "col-xs-11 comercial-nombre")]')

        # Lista para almacenar los links
        links = []

        # Itera sobre los divs encontrados y extrae los links
        for div in divs:
            a_tag = div.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            links.append(link)
        
        return links

    def total_nutris(self):
        all_links = []
        data = []
        page_counter = 1

        while True:
            all_links.extend(self.link_nutrios())

            try:
                # Verifica la URL actual
                current_url = self.driver.current_url
                
                # Espera hasta que el botón de la siguiente página esté disponible y haz clic en él
                next_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[2]/ul/li[8]/a'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                sleep(1)  # Añadir una pequeña pausa después del scroll
                next_button.click()
                sleep(5)  # Añadir una pausa para permitir que la nueva página se cargue completamente
                
                # Verifica si la URL ha cambiado
                if self.driver.current_url == current_url:
                    print("Reached the last page or cannot proceed to the next page.")
                    break

                page_counter += 1
                print(f"Processed page {page_counter}")

            except Exception as e:
                print("No more pages or an error occurred:", e)
                break

        print("Total links found:", len(all_links))
        for link in all_links:
            details = self.get_data(link)
            data.append(details)

        # Asegúrate de que data sea una lista de diccionarios antes de crear el DataFrame
        df = pd.DataFrame(data)
        df.to_excel('nutris.xlsx', index=False)
        print("Data saved to nutris.xlsx")

    def get_data(self, link):
        page = 1
        print(page)
        self.driver.get(link)
        page +=1
        sleep(3)  # Añadir una pequeña pausa para permitir que la página se cargue completamente

        try:
            name = self.driver.find_element(By.XPATH, '//h1[contains(@class, "mt-3")]')
            name = name.get_attribute("innerText").split('\n')[0].strip()
        except:
            name = None

        try:
            location = self.driver.find_element(By.CLASS_NAME, 'localidad')
            location = location.text.strip()
        except:
            location = None

        try:
            phone = self.driver.find_element(By.CLASS_NAME, 'telephone')
            phone = phone.text.strip()
        except:
            phone = None

        try:
            address = self.driver.find_element(By.CLASS_NAME, 'address')
            address = address.text.strip()
        except:
            address = None

        try:
            website_element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'sitio-web'))
            )
            website = website_element.get_attribute('href')
            
            # Extraer solo el enlace base sin los parámetros de consulta
            if '?' in website:
                website = website.split('?')[0]
            else:
                website = website

        except:
            website = None

        try:
            description_element = self.driver.find_element(By.CSS_SELECTOR, 'div[itemprop="description"]')
            description = description_element.text.strip()
            
        except:
            description = None

   
    
        return {
            'name': name,
            'location': location,
            'phone': phone,
            'address': address,
            'website': website,
            'description': description
        }
    
    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    bot = AmarillasBot()
    bot.total_nutris()
    bot.close()
