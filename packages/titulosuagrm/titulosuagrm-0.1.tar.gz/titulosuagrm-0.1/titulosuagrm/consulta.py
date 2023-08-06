import requests
import time 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager


def obtener_token_titulo(): 
    # Definir las opciones
    options = webdriver.ChromeOptions() 
    # Es más escalable para trabajar en modo sin cabecera
    options.headless = True 
    # Normalmente, selenium espera a que se descarguen todos los recursos
    # No lo necesitamos ya que la página también se completa con el código javascript en ejecución. 
    options.page_load_strategy = 'none' 
    
    # Esto devuelve la ruta de descarga del controlador web
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 

    # Pasar las opciones definidas y los objetos de servicio para inicializar el controlador web 
    driver = Chrome(options=options, service=chrome_service) 
    driver.implicitly_wait(5)

    url = "https://www.uagrm.edu.bo/udigital/titulos" 
    driver.get(url) 
    time.sleep(10)

    content = driver.find_element(By.CLASS_NAME, "token")
    valor_token = content.get_attribute('value')
    return valor_token

class EndpointClient:
    def __init__(self):
        self.base_url = "https://www.uagrm.edu.bo/udigital/ajax/2"
        self.token = obtener_token_titulo()
    
    def consultar_endpoint(self, cedula, procedencia):
        url = f"{self.base_url}?token={self.token}&cedula={cedula}&procedencia={procedencia}"
        
        try:
            # Realizar la petición GET
            response = requests.get(url)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la respuesta en formato JSON
                data = response.json()
                # Retornar la respuesta
                return data
            else:
                # Retornar None en caso de una respuesta no exitosa
                print("La petición GET no fue exitosa. Código de estado:", response.status_code)
                return None

        except requests.exceptions.RequestException as e:
            # Manejar errores de conexión u otros errores de la petición
            print("Error en la petición GET:", e)
            return None