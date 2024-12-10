# Adicione ao final do script anterior de Selenium
import time

def open_browser(youtube_url, index, duration):
    print(f"Iniciando navegador {index + 1}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chrome_options)
    driver.get(youtube_url)
    time.sleep(duration)  # Mantém aberto pelo tempo especificado
    driver.quit()
    print(f"Navegador {index + 1} fechado")
