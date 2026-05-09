def lluvia_de_corazones():
    corazones_html = """
    <style>
    .corazon {
        position: fixed;
        top: -10vh;
        font-size: 2rem;
        z-index: 9999;
        animation: caer 4s linear forwards;
    }
    @keyframes caer {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }
    </style>
    """

    # Generamos varios corazones con posiciones y tiempos de caída aleatorios
    import random
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        duration = random.uniform(3, 5)
        emoji = random.choice(["❤️", "💖", "💘", "💕", "💗"])

        corazones_html += f'<div class="corazon" style="left: {left}vw; animation-delay: {delay}s; animation-duration: {duration}s;">{emoji}</div>'

    st.markdown(corazones_html, unsafe_allow_html=True)

import streamlit as st
from datetime import date
import random
import time
import base64
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Para mi Pandita Eterno", page_icon="🐼",
                   layout="centered")

# --- FUNCIÓN TELEGRAM ---
def notificar_telegram(deseo):
    # Usamos Secrets por seguridad
    try:
        token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
        mensaje = f"🎂 ¡NUEVO DESEO RECIBIDO! 🎂\n\nTu Pandita ha pedido:\n\"{deseo}\""
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
        requests.get(url)
    except Exception as e:
        st.error(f"Error de configuración en Telegram: {e}")

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
    /* Estilo especial para la carta de San Valentín */
    .carta {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #d33682;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        font-family: 'Georgia', serif;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("❤️ Menú de Amor")
# ¡Agregamos la nueva sección aquí!
opcion = st.sidebar.radio("Ir a:", ["Inicio", "Nuestra Galería", "Mensajes Especiales",
                                    "San Valentín 💘", "Cumpleaños 🎂"])

# --- SECCIÓN 1: INICIO ---
if opcion == "Inicio":
    st.title(f"¡Hola, mi {random.choice(['bb', 'bomboncito', 'pandita'])}! ❤️")

    # Imagen principal
    try:
        st.image("portada.jpg", caption="Tú y yo, siempre.", use_container_width=True)
    except:
        st.warning(
            "📌 (Aquí aparecerá la imagen 'portada.jpg' cuando la guardes en la carpeta)")

    st.write("---")

    # Contador de tiempo
    st.subheader("Tiempo recorriendo el mundo juntos")
    fecha_inicio = date(2024, 11, 19)  # Fecha de inicio
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

# --- SECCIÓN 4: ESPECIAL SAN VALENTÍN ---
elif opcion == "San Valentín 💘":

    # --- MÚSICA INVISIBLE ---
    try:
        # 1. Leemos el archivo de la canción
        with open("cancion.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()
            # 2. Lo codificamos para inyectarlo en HTML
            audio_base64 = base64.b64encode(audio_bytes).decode()

        # 3. Creamos un reproductor HTML completamente oculto (display:none) que se repita (loop)
        audio_html = f"""
            <audio autoplay loop style="display:none;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Si aún no subes el archivo, el código no se rompe

    st.title("Feliz San Valentín, mi Pandita 🐼💘")
    st.write("---")

    st.markdown("### Un pequeño detalle para ti en este día especial...")
    st.write(" ")

    # 1. El Medidor de Amor (Interactivo)
    st.write("#### 🎚️ ¿Cuánto te amo hoy?")
    amor_nivel = st.slider("Desliza la barra para descubrirlo...", min_value=0,
                           max_value=100, value=10)

    if amor_nivel == 0:
        st.error(
            "🥺 ¿Cero? Ouch... Mi corazoncito acaba de romperse un poquito. ¡Sabes que eso es imposible, yo te adoro!")
    elif 1 <= amor_nivel <= 25:
        st.warning(
            "😭 Ay no, ¿tan poquito? Si supieras que te pienso en cada momento del día...")
    elif 26 <= amor_nivel <= 50:
        st.warning(
            "😕 Mmm... ¿estás seguro? Yo diría que te estás quedando muy, muy corto corazón.")
    elif 51 <= amor_nivel <= 75:
        st.info(
            "🥰 ¡Ahí vamos mejorando! Es muchísimo más que eso, pero vas por buen camino hacia la respuesta correcta.")
    elif 76 <= amor_nivel <= 99:
        st.success(
            "💖 ¡Uy, cerquita! Estás a punto de adivinar, pero te aseguro que es todavía más de lo que marca ahí.")
    elif amor_nivel == 100:
        st.success(
            "¡Exacto! Y aún así, la escala de 100 se queda cortísima porque lo mío por ti es completamente infinito. ♾️🤍️")
        lluvia_de_corazones()
    st.write("---")

    # 2. Carta Desplegable Oculta
    st.write("#### 💌 Mi Carta para Ti")
    with st.expander("Toca aquí para abrir tu carta de San Valentín"):
        st.markdown("""
        <div class="carta">
        <strong>AMORE MIO,</strong><br><br>
        Mi chiquito precioso, mi bomboncito, quiero ser tu Valentín hoy y siempre 🤍. Aunque los planes de hoy no salieron exactamente como quería, nada de eso importa porque lo verdaderamente valioso es tenernos. Quiero que sepas que te amo con todo lo que soy y que siempre estás en mi corazón, a pesar de todo 🫶🏾.
        
¿Recuerdas que el primer apodo que te puse fue 'Mi Serendipia'? ✨ Sigue siendo tan real como ese primer día, porque llegaste a mi vida como la sorpresa más hermosa; un hallazgo afortunado y precioso que no estaba buscando, pero que terminó siendo mi mejor descubrimiento.

Quiero seguir construyendo un futuro contigo, paso a paso, mi Pandita 🐼. Acompañándonos en todo, porque eres tú con quien quiero compartir cada momento. Eres mi persona favorita en el mundo entero 🫰🏾<br><br>
        <em>Tuyo siempre.</em>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # 3. Regalo Virtual
    st.write("#### 🎁 Tienes un regalo virtual esperando")
    if st.button("Abrir regalo sorpresa"):
        with st.spinner('Abriendo con mucho cuidado...'):
            time.sleep(2)
        st.success(
            "🎟️ **¡CUPÓN VÁLIDO POR:** Un abrazo gigante y mil besos 🥰")

# --- SECCIÓN 5: CUMPLEAÑOS ---
elif opcion == "Cumpleaños 🎂":
    st.title("🎂 Próximamente... ¡Tu gran día! 🥳")
    st.write("---")
    
    st.markdown(f"""
    <div class="carta">
    <h3>Mi Pandita Precioso 🐼✨</h3>
    Sé que se acerca tu cumpleaños y mi corazón ya está saltando de alegría. Me hace tan feliz poder celebrar tu vida, porque eres lo mejor que me ha pasado. 
    <br><br>
    Quiero que este día sea perfecto, tal como tú lo eres para mí. Por eso, me encantaría saber qué es aquello que te haría más feliz, qué sueñas o qué te gustaría vivir en este nuevo año que comienzas.
    <br><br>
    <em>"Eres mi regalo diario, y quiero ser yo quien te consienta al máximo."</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Animación de globos
    st.balloons()
    
    # Apartado interactivo con botones
    st.write("#### 🕯️ ¿Qué te haría feliz en tu cumpleaños?")
    st.write("Dime, mi amor... ¿qué prefieres para este año?")
    
    col1, col2 = st.columns(2)
    
    if col1.button("🎁 1 regalo a mi elección"):
        st.session_state.tipo_regalo = "uno"
    if col2.button("🎁 Muchos regalos"):
        st.session_state.tipo_regalo = "muchos"
    
    if 'tipo_regalo' in st.session_state:
        st.write("---")
        if st.session_state.tipo_regalo == "uno":
            st.markdown("### ✨ ¡Tú eliges!")
            deseo = st.text_area("Escribe aquí ese regalo especial que tienes en mente...", 
                                 placeholder="Me gustaría que mi regalo fuera...", height=100)
            
            if st.button("¡Enviar mi elección! 🎂✨"):
                if deseo:
                    with st.spinner('Guardando tu elección secreta...'):
                        time.sleep(2)
                    
                    # Guardamos y notificamos
                    with open("deseos_secretos.txt", "a", encoding="utf-8") as f:
                        from datetime import datetime
                        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"[{ahora}] Eligió 1 regalo: {deseo}\n")
                    
                    notificar_telegram(f"Ha elegido 1 REGALO: {deseo}")
                    
                    st.success("✨ ¡Elección guardada! Haré todo lo posible para que ese regalo llegue a tus manos. ¡Te amo! ❤️")
                    st.snow()
                    st.balloons()
                else:
                    st.warning("¡Mmm! No has escrito qué regalo quieres todavía. 😉")
        
        elif st.session_state.tipo_regalo == "muchos":
            st.markdown("""
            <div class="carta">
            <h3 style='color: #d33682;'>¡Qué emoción! ✨</h3>
            Has elegido la opción de <strong>muchos regalos</strong>. ¡Prepárate para las sorpresas, mi amor! 
            Me encargaré de que cada detalle sea especial y de que este cumpleaños sea inolvidable y lleno de mimos.
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("¡Confirmar sorpresas! 🚀❤️"):
                with st.spinner('Preparando la maquinaria de sorpresas...'):
                    time.sleep(2)
                
                # Guardamos y notificamos
                with open("deseos_secretos.txt", "a", encoding="utf-8") as f:
                    from datetime import datetime
                    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{ahora}] Eligió MUCHOS REGALOS (Sorpresa)\n")
                
                notificar_telegram("¡HA ELEGIDO MUCHOS REGALOS! 🎉 (Prepárate para sorprender)")
                
                st.success("¡Confirmado! El plan de sorpresas infinitas ha comenzado. 🐼💖")
                st.snow()
                st.balloons()