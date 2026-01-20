import streamlit as st
from datetime import date
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Para mi Pandita Eterno", page_icon="🐼",
                   layout="centered")

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #fff5f7;
    }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        border: 2px solid #ff4b4b;
        background-color: #ff4b4b;
        color: white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: white;
        color: #ff4b4b;
    }
    h1, h2, h3 {
        color: #d33682;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("❤️ Menú de Amor")
opcion = st.sidebar.radio("Ir a:", ["Inicio", "Nuestra Galería", "Mensajes Especiales"])

# --- SECCIÓN 1: INICIO ---
if opcion == "Inicio":
    st.title(f"¡Hola, mi {random.choice(['bb', 'bomboncito', 'pandita'])}! ❤️")

    # Imagen principal
    # Nombre sugerido: portada.jpg
    try:
        st.image("portada.jpg", caption="Tú y yo, siempre.", use_container_width=True)
    except:
        st.warning(
            "📌 (Aquí aparecerá la imagen 'portada.jpg' cuando la guardes en la carpeta)")

    st.write("---")

    # Contador de tiempo
    st.subheader("Tiempo recorriendo el mundo juntos")
    fecha_inicio = date(2024, 11, 19)  # CAMBIA ESTA FECHA: (Año, Mes, Día)
    hoy = date.today()
    dias_pasados = (hoy - fecha_inicio).days

    col1, col2, col3 = st.columns(3)
    col1.metric("Días", dias_pasados)
    col2.metric("Horas", dias_pasados * 24)
    col3.metric("Minutos", dias_pasados * 24 * 60)

    st.balloons()

# --- SECCIÓN 2: GALERÍA ---
elif opcion == "Nuestra Galería":
    st.header("📸 Nuestros Momentos Favoritos")
    st.write("Cada foto es un recuerdo que guardo en mi corazón, Adonis.")

    col1, col2 = st.columns(2)

    with col1:
        try:
            st.image("foto1.jpg", caption="Momentos divertidos")
        except:
            st.info("Sube 'foto1.jpg'")

        try:
            st.image("foto2.jpg", caption="Ese día especial")
        except:
            st.info("Sube 'foto2.jpg'")

    with col2:
        try:
            st.image("foto3.jpg", caption="Mi lugar favorito eres tú")
        except:
            st.info("Sube 'foto3.jpg'")

        st.write("✨ **Nota:** Eres el pandita más guapo del mundo.")

# --- SECCIÓN 3: MENSAJES ---
elif opcion == "Mensajes Especiales":
    st.header("💌 Un mensaje para cada momento")

    mensajes = [
        "Eres mi pensamiento favorito cada mañana.",
        "Gracias por ser mi bomboncito y cuidarme tanto.",
        "Adonis, contigo la vida es mucho más bonita.",
        "No importa el lugar, siempre que sea contigo, mi bb.",
        "Eres el regalo más lindo que me ha dado la vida.",
        "¡Te amo más de lo que las palabras pueden decir!"
    ]

    if st.button("Generar un mensaje de amor"):
        mensaje_hoy = random.choice(mensajes)
        st.success(mensaje_hoy)
        st.snow()

    st.write("---")
    st.text_area("Déjame una nota aquí (solo para tus ojos):",
                 placeholder="Escribe algo tierno...")