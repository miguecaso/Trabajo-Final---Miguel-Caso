import streamlit as st
import pandas as pd
import random

# Cargar la base de datos actualizada
df = pd.read_csv("peliculas_nolan_con_imagenes.csv")

# --- INTERFAZ INICIAL ---
st.set_page_config(page_title="Chatbot Nolan", page_icon="🎬")
st.title("🎬 ¿Qué película de Nolan te representa?")
nombre = st.text_input("¿Cómo te llamas?")

if nombre:
    st.write(f"¡Hola, {nombre}! Bienvenido/a al recomendador de películas de Christopher Nolan.")
    
    conoce = st.radio("¿Conoces a Christopher Nolan?", ["Sí", "No"])
    
    st.markdown("### 📖 ¿Quién es Christopher Nolan?")
    st.info("""
Christopher Nolan es un director, guionista y productor británico, conocido por sus películas de estructura narrativa compleja, temas filosóficos y visuales impactantes.
    
Es autor de películas como *Inception*, *Interstellar*, *Tenet*, *Memento*, entre otras.
    """)

    st.markdown("---")
    st.markdown("### 🧠 Descubre qué película va contigo")
    
    # --- PREGUNTAS DE PERFIL ---
    opcion1 = st.radio("¿Qué tema te atrae más?", [
        "Sueños y subconsciente",
        "Viajes en el tiempo y el espacio",
        "Realidades paralelas",
        "Magia y rivalidad",
        "La guerra y el heroísmo",
        "El caos y el crimen",
        "Ética científica"
    ])

    opcion2 = st.radio("¿Qué emoción quieres sentir al ver una película?", [
        "Asombro intelectual",
        "Suspenso e intriga",
        "Conmoción emocional",
        "Inspiración moral",
        "Adrenalina pura"
    ])

    if st.button("🎞️ Recomiéndame una película"):
        # Lógica simple de recomendación
        recomendaciones = []

        if "sueños" in opcion1.lower():
            recomendaciones = df[df["Título"] == "Inception"]
        elif "tiempo" in opcion1.lower() or "espacio" in opcion1.lower():
            recomendaciones = df[df["Título"].isin(["Interstellar", "Tenet"])]
        elif "magia" in opcion1.lower():
            recomendaciones = df[df["Título"] == "The Prestige"]
        elif "guerra" in opcion1.lower():
            recomendaciones = df[df["Título"] == "Dunkirk"]
        elif "crimen" in opcion1.lower():
            recomendaciones = df[df["Título"] == "The Dark Knight"]
        elif "ética" in opcion1.lower():
            recomendaciones = df[df["Título"] == "Oppenheimer"]
        elif "paralelas" in opcion1.lower():
            recomendaciones = df[df["Título"] == "Memento"]
        else:
            recomendaciones = df.sample(1)

        pelicula = recomendaciones.sample(1).iloc[0]

        st.image(pelicula["Imagen"], use_container_width=True)
        st.success(f"🎬 {pelicula['Título']} ({pelicula['Año']})")
        st.write(f"**Género:** {pelicula['Género']}")
        st.write(f"**Valoración:** {pelicula['Valoración']}")
        st.write(f"**Sinopsis:** {pelicula['Sinopsis']}")
        st.markdown(f"[🔗 Ver en Filmaffinity]({pelicula['Enlace']})")
