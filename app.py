import streamlit as st
import pandas as pd
from collections import defaultdict

# Cargar base de datos
df = pd.read_csv("peliculas_nolan_con_imagenes.csv")

# Configuración de página
st.set_page_config(page_title="Test Nolan", page_icon="🎬")
st.title("Test de Personalidad: ¿Qué película de Nolan eres tú?")

# Inicializar estado
if "pregunta" not in st.session_state:
    st.session_state.pregunta = 1
    st.session_state.puntajes = defaultdict(int)

# Diccionario de preguntas y opciones con puntos
preguntas = {
    1: {
        "texto": "¿Qué tema central te atrae más?",
        "opciones": {
            "Sueños y subconsciente": ["Inception"],
            "Viajes espaciales y tiempo": ["Interstellar", "Tenet"],
            "Identidad y memoria": ["Memento"],
            "Ética y ciencia": ["Oppenheimer"],
            "Magia y obsesión": ["The Prestige"],
            "Guerra y supervivencia": ["Dunkirk"],
            "Crimen y caos": ["The Dark Knight"]
        }
    },
    2: {
        "texto": "¿Qué emoción disfrutas más al ver cine?",
        "opciones": {
            "Confusión estimulante": ["Memento", "Tenet"],
            "Admiración científica": ["Interstellar", "Oppenheimer"],
            "Asombro y creatividad": ["Inception", "The Prestige"],
            "Tensión y adrenalina": ["Dunkirk", "The Dark Knight"],
            "Reflexión filosófica": ["Oppenheimer", "Inception"]
        }
    },
    3: {
        "texto": "¿Te gustan los protagonistas...?",
        "opciones": {
            "Con traumas o pérdidas": ["Inception", "Memento"],
            "Científicos o exploradores": ["Interstellar", "Oppenheimer"],
            "Heroicos y éticos": ["The Dark Knight"],
            "Obsesivos y ambiguos": ["The Prestige", "Tenet"],
            "Realistas y vulnerables": ["Dunkirk"]
        }
    },
    4: {
        "texto": "¿Conoces a alguno de estos actores?",
        "opciones": {
            "Leonardo DiCaprio": ["Inception"],
            "Cillian Murphy": ["Oppenheimer", "Dunkirk", "Inception"],
            "Christian Bale": ["The Prestige", "The Dark Knight"],
            "Matthew McConaughey": ["Interstellar"],
            "Guy Pearce": ["Memento"],
            "Robert Pattinson": ["Tenet"]
        },
        "multiple": True
    },
    5: {
        "texto": "¿Qué estilo visual prefieres?",
        "opciones": {
            "Realismo bélico": ["Dunkirk"],
            "Espacios vastos y estéticos": ["Interstellar"],
            "Ilusiones y teatralidad": ["The Prestige"],
            "Ambientes urbanos distorsionados": ["Inception"],
            "Oscuridad y caos": ["The Dark Knight"],
            "Estética limpia y futurista": ["Tenet"]
        }
    },
    6: {
        "texto": "¿Qué frase te representa más?",
        "opciones": {
            "La mente puede construir mundos.": ["Inception"],
            "El tiempo es relativo.": ["Interstellar", "Tenet"],
            "No confíes ni en ti mismo.": ["Memento"],
            "El fin justifica los medios.": ["The Dark Knight", "Oppenheimer"],
            "La perfección cuesta todo.": ["The Prestige"]
        }
    },
    7: {
        "texto": "¿Qué tipo de final te gusta más?",
        "opciones": {
            "Sorprendente y abierto": ["Inception", "Tenet"],
            "Reflexivo y filosófico": ["Oppenheimer"],
            "Trágico o ambiguo": ["Memento", "The Prestige"],
            "Heroico y potente": ["The Dark Knight"],
            "Realista y sin redención": ["Dunkirk"]
        }
    },
    8: {
        "texto": "¿Te interesa la ciencia en el cine?",
        "opciones": {
            "Sí, me fascina": ["Oppenheimer", "Interstellar"],
            "Solo si es entendible": ["Inception", "Tenet"],
            "Prefiero emociones": ["The Prestige", "The Dark Knight"]
        }
    },
    9: {
        "texto": "¿Qué tipo de historia te motiva más?",
        "opciones": {
            "Una misión imposible": ["Interstellar", "Tenet"],
            "Un duelo de mentes": ["The Prestige", "The Dark Knight"],
            "Una lucha interna": ["Inception", "Memento"],
            "Una tragedia inevitable": ["Oppenheimer", "Dunkirk"]
        }
    },
    10: {
        "texto": "¿Qué tan dispuesto estás a pensar mucho durante la película?",
        "opciones": {
            "¡Me encanta!": ["Memento", "Inception", "Tenet"],
            "Me gusta, pero no todo el tiempo": ["Oppenheimer", "The Prestige"],
            "Prefiero algo más directo": ["The Dark Knight", "Dunkirk"]
        }
    }
}

# Obtener número de pregunta actual
p = st.session_state.pregunta

if p <= 10:
    pregunta_actual = preguntas[p]
    st.markdown(f"### Pregunta {p}: {pregunta_actual['texto']}")
    opciones = pregunta_actual["opciones"]

    if pregunta_actual.get("multiple", False):
        seleccion = st.multiselect("Selecciona todas las que conoces:", list(opciones.keys()))
    else:
        seleccion = st.radio("Selecciona una opción:", list(opciones.keys()))

    if st.button("Siguiente"):
        if seleccion:
            if isinstance(seleccion, list):
                for s in seleccion:
                    for peli in opciones[s]:
                        st.session_state.puntajes[peli] += 1
            else:
                for peli in opciones[seleccion]:
                    st.session_state.puntajes[peli] += 1
            st.session_state.pregunta += 1
        else:
            st.warning("Por favor selecciona al menos una opción.")

# Mostrar resultado final
if p > 10:
    st.success("¡Test completado!")
    peli_final = max(st.session_state.puntajes, key=st.session_state.puntajes.get)
    pelicula = df[df["Título"] == peli_final].iloc[0]

    frases = {
        "Inception": "Eres creativo, complejo y vives entre ideas profundas.",
        "Interstellar": "Eres curioso, sentimental y amas lo desconocido.",
        "Memento": "Valoras la verdad, incluso si duele. Tu mente nunca descansa.",
        "The Prestige": "Eres perfeccionista, apasionado y algo misterioso.",
        "Tenet": "Te encanta el caos ordenado. Piensas en 4 dimensiones.",
        "Dunkirk": "Eres realista, valiente y directo. El silencio también te dice mucho.",
        "The Dark Knight": "Tienes un fuerte sentido de justicia, aunque luchas con tu oscuridad.",
        "Oppenheimer": "Eres reflexivo, profundo y te cuestionas el impacto de tus decisiones."
    }

    st.image(pelicula["Imagen"], use_container_width=True)
    st.markdown(f"## {pelicula['Título']} ({pelicula['Año']})")
    st.write(f"**Género:** {pelicula['Género']}")
    st.write(f"**Valoración:** {pelicula['Valoración']}")
    st.write(f"**Sinopsis:** {pelicula['Sinopsis']}")
    st.markdown(f"[Ver en Filmaffinity]({pelicula['Enlace']})")
    st.info(f" {frases.get(pelicula['Título'], '')}")
