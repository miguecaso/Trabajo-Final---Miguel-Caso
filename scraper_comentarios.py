import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from textblob import TextBlob

# Cargar tu archivo con los enlaces a películas
df = pd.read_csv("peliculas_nolan_con_imagenes.csv")

comentarios_data = []

def get_reviews(peli_titulo, url, max_paginas=5):
    base_url = url.replace(".html", "_comments.html")
    pagina = 1
    while pagina <= max_paginas:
        full_url = f"{base_url}?pag={pagina}"
        response = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        bloques = soup.select(".user-review-text")

        if not bloques:
            break

        for b in bloques:
            texto = b.get_text(strip=True)
            if len(texto) >= 50:
                sentimiento = TextBlob(texto).sentiment.polarity
                clasificacion = "Positivo" if sentimiento >= 0 else "Negativo"
                comentarios_data.append({
                    "Película": peli_titulo,
                    "Comentario": texto,
                    "Sentimiento": clasificacion
                })

        pagina += 1
        time.sleep(1)  # Evitar bloqueo

# Ejecutar scraping
for _, row in df.iterrows():
    titulo = row["Título"]
    enlace = row["Enlace"]
    print(f"Extrayendo comentarios de: {titulo}")
    get_reviews(titulo, enlace)

# Guardar CSV final
df_comentarios = pd.DataFrame(comentarios_data)
df_comentarios.to_csv("comentarios_nolan.csv", index=False)
print("¡Comentarios guardados exitosamente en comentarios_nolan.csv!")
