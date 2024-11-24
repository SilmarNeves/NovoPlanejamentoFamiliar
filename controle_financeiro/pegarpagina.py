import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Inicializa o navegador (Selenium Manager cuida do ChromeDriver automaticamente)
driver = webdriver.Chrome()

# URL alvo
url = "https://investidor.suno.com.br/videos"  # Substitua pela URL do site
driver.get(url)

# Espera 15 segundos para o login
print("Por favor, faça o login na página. Aguardando 15 segundos...")
time.sleep(15)

# Coletando todos os links (elementos <a>)
links = driver.find_elements(By.TAG_NAME, "a")

# Arrays para armazenar links visíveis e ocultos
links_visiveis = []
links_ocultos = []

# Verificando a visibilidade de cada link
for link in links:
    href = link.get_attribute("href")  # Obtém o href do link
    if href:  # Ignora elementos sem href
        if link.is_displayed():  # Verifica se o link está visível
            links_visiveis.append(href)
        else:
            links_ocultos.append(href)

# Exibindo os resultados
print("Links Visíveis:")
print("\n".join(links_visiveis))

print("\nLinks Ocultos:")
print("\n".join(links_ocultos))

# Fechando o navegador
driver.quit()
