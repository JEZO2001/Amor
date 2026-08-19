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
import streamlit.components.v1 as components
from datetime import date, timedelta
import random
import time
import base64
import os
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
    /* ───────── Sección "Un Mes Más" ───────── */
    .mes-hero {
        position: relative;
        overflow: hidden;
        margin-bottom: 28px;
        padding: 42px 24px 36px;
        border-radius: 24px;
        text-align: center;
        color: #fff5f8;
        background: linear-gradient(135deg, #7d1a3c 0%, #d8376b 45%, #b6407f 100%);
        background-size: 220% 220%;
        animation: mesGradiente 14s ease infinite;
        box-shadow: 0 18px 45px -18px rgba(125, 26, 60, .75);
    }
    @keyframes mesGradiente {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    /* brillo que cruza la tarjeta cada cierto tiempo */
    .mes-hero::after {
        content: "";
        position: absolute;
        top: -60%; left: -30%;
        width: 40%; height: 220%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,.22), transparent);
        transform: rotate(18deg);
        animation: mesBrillo 6.5s ease-in-out infinite;
    }
    @keyframes mesBrillo {
        0%, 65%  { left: -30%; }
        100%     { left: 130%; }
    }
    .mes-hero__kicker {
        margin: 0 0 6px !important;
        font-size: .78rem !important;
        letter-spacing: .34em;
        text-transform: uppercase;
        opacity: .85;
    }
    .mes-hero__num {
        margin: 0 !important;
        font-family: Georgia, serif !important;
        font-size: clamp(4.5rem, 22vw, 8rem) !important;
        font-weight: 700 !important;
        line-height: .92 !important;
        text-shadow: 0 8px 30px rgba(0,0,0,.35);
        animation: mesLatido 2.6s ease-in-out infinite;
    }
    @keyframes mesLatido {
        0%, 100% { transform: scale(1); }
        14%      { transform: scale(1.06); }
        28%      { transform: scale(1); }
        42%      { transform: scale(1.03); }
    }
    .mes-hero__label {
        margin: 2px 0 14px !important;
        font-size: 1.5rem !important;
        letter-spacing: .06em;
    }
    .mes-hero__frase {
        margin: 0 auto !important;
        max-width: 30rem;
        font-family: Georgia, serif !important;
        font-style: italic !important;
        font-size: 1.05rem !important;
        opacity: .95;
    }
    /* pétalos que caen de fondo */
    .petalo {
        position: fixed;
        top: -8vh;
        z-index: 0;
        font-size: 1.4rem;
        pointer-events: none;
        animation: petaloCae linear infinite;
    }
    @keyframes petaloCae {
        0%   { transform: translateY(0) rotate(0deg);      opacity: 0; }
        10%  {                                             opacity: .9; }
        100% { transform: translateY(112vh) rotate(420deg); opacity: 0; }
    }
    /* tarjetas del recorrido */
    .hito {
        margin-bottom: 12px;
        padding: 14px 18px;
        border-radius: 14px;
        border-left: 4px solid #d8376b;
        background: linear-gradient(90deg, rgba(216,55,107,.10), rgba(216,55,107,.02));
        animation: hitoEntra .7s ease both;
    }
    @keyframes hitoEntra {
        from { opacity: 0; transform: translateX(-14px); }
        to   { opacity: 1; transform: none; }
    }
    .hito b { color: #d33682; }

    /* ───────── Juego: las cajitas del mes ───────── */
    /* Streamlit pone la clase st-key-<key> en el envoltorio del widget,
       así que apuntamos solo a los botones cuya key empieza por "caja_". */
    /* Streamlit apila las columnas en pantallas angostas; aquí queremos que
       la cuadrícula siga siendo de 3x3 también en el celular. */
    .st-key-cajitas [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }
    .st-key-cajitas [data-testid="stColumn"] {
        flex: 1 1 0 !important;
        width: 33.333% !important;
        min-width: 0 !important;
    }
    [class*="st-key-caja_"] button {
        min-height: 104px !important;
        border-radius: 18px !important;
        border: 2px dashed #f0a8c4 !important;
        background: linear-gradient(160deg, #fff0f5, #ffdcea) !important;
        color: #d33682 !important;
        font-size: 2rem !important;
        line-height: 1 !important;
        box-shadow: 0 6px 16px -8px rgba(216, 55, 107, .5);
        transition: transform .25s ease, box-shadow .25s ease,
                    background .25s ease !important;
    }
    [class*="st-key-caja_"] button:hover {
        transform: translateY(-4px) rotate(-3deg);
        background: linear-gradient(160deg, #ffe4ef, #ffc9de) !important;
        box-shadow: 0 12px 26px -10px rgba(216, 55, 107, .65);
    }
    .cajita-abierta {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 104px;
        padding: 10px 8px;
        text-align: center;
        border-radius: 18px;
        border: 2px solid #f2c1d6;
        background: linear-gradient(160deg, #ffffff, #ffeef5);
        box-shadow: 0 8px 20px -10px rgba(216, 55, 107, .45);
        font-family: Georgia, serif;
        font-size: clamp(.68rem, 2.7vw, .88rem);
        line-height: 1.3;
        hyphens: auto;
        color: #7d1a3c;
        animation: cajitaAbre .55s cubic-bezier(.34, 1.56, .64, 1) both;
    }
    @keyframes cajitaAbre {
        0%   { opacity: 0; transform: scale(.45) rotate(-14deg); }
        60%  { opacity: 1; }
        100% { opacity: 1; transform: none; }
    }
    .cajita-final {
        margin-top: 20px;
        padding: 28px 22px;
        border-radius: 22px;
        text-align: center;
        color: #fff5f8;
        background: linear-gradient(135deg, #7d1a3c, #d8376b 60%, #b6407f);
        box-shadow: 0 18px 40px -18px rgba(125, 26, 60, .85);
        animation: cajitaAbre .75s cubic-bezier(.34, 1.56, .64, 1) both;
    }
    .cajita-final__t {
        margin: 0 0 10px !important;
        font-family: Georgia, serif !important;
        font-size: 1.6rem !important;
    }
    /* La barra de progreso de Streamlit viene en azul; la pasamos al rosa.
       El relleno cuelga tres niveles por debajo del contenedor. */
    [data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #d8376b, #ff5c8a) !important;
        border-radius: 999px !important;
    }
    .cajita-final__p {
        margin: 0 auto !important;
        max-width: 28rem;
        font-size: 1rem !important;
        opacity: .95;
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

def medio(nombre):
    """Ruta de una foto o audio, esté en la raíz del repo o dentro de assets/
    (donde vive la versión web). Si no aparece, devuelve el nombre a secas
    para que los avisos de "sube este archivo" sigan saliendo igual."""
    for carpeta in ("", "assets/img/", "assets/audio/"):
        if os.path.exists(carpeta + nombre):
            return carpeta + nombre
    return nombre


# --- FECHA EN QUE TODO EMPEZÓ ---
FECHA_INICIO = date(2024, 11, 19)


def meses_cumplidos(desde, hoy):
    """Meses completos entre dos fechas (el día 19 de cada mes suma uno)."""
    meses = (hoy.year - desde.year) * 12 + (hoy.month - desde.month)
    if hoy.day < desde.day:
        meses -= 1
    return meses


def proximo_mesiversario(desde, hoy):
    """Fecha del siguiente mesiversario a partir de hoy."""
    siguiente = meses_cumplidos(desde, hoy) + 1
    anio = desde.year + (desde.month - 1 + siguiente) // 12
    mes = (desde.month - 1 + siguiente) % 12 + 1
    # si el mes destino no tiene ese día (ej. 31), usamos el último día del mes
    dia = desde.day
    while True:
        try:
            return date(anio, mes, dia)
        except ValueError:
            dia -= 1


def arrancar_musica():
    """Pone la canción en marcha sin que haya que darle al play.

    El navegador bloquea el sonido automático hasta que la persona toca algo,
    y el <audio> de Streamlit no vuelve a intentarlo por su cuenta. Este
    componente vive en un iframe con acceso al documento padre, así que
    reintenta al cargar y además al primer toque en cualquier parte."""
    components.html("""
        <script>
        (function () {
          var doc;
          try { doc = window.parent.document; } catch (e) { return; }

          function arranca() {
            var a = doc.querySelector('audio');
            if (!a) return;
            a.loop = true;              // Streamlit no fija el atributo loop
            if (a.paused) { a.volume = 0.6; a.play().catch(function () {}); }
          }

          arranca();                    // por si la política del navegador lo permite
          ['pointerdown', 'touchstart', 'keydown'].forEach(function (ev) {
            doc.addEventListener(ev, arranca, true);
          });
        })();
        </script>
    """, height=0)


def reproducir_en_bucle(*candidatos):
    """Reproduce el primer archivo que exista, en bucle y sin controles.
    Devuelve el nombre del archivo usado, o None si no encontró ninguno."""
    for archivo in candidatos:
        try:
            with open(archivo, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""<audio autoplay loop style="display:none;">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>""",
                unsafe_allow_html=True)
            return archivo
        except FileNotFoundError:
            continue
    return None


# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("❤️ Menú de Amor")

SECCIONES = ["Un Mes Más 💞", "Inicio", "Nuestra Galería", "Mensajes Especiales",
             "San Valentín 💘", "Cumpleaños 🎂"]

# El día del mesiversario la página abre sola en esa sección.
_indice = 0 if date.today().day == FECHA_INICIO.day else 1
opcion = st.sidebar.radio("Ir a:", SECCIONES, index=_indice)

# --- SECCIÓN 0: UN MES MÁS (mesiversario) ---
if opcion == "Un Mes Más 💞":

    hoy = date.today()
    meses = meses_cumplidos(FECHA_INICIO, hoy)
    dias_juntos = (hoy - FECHA_INICIO).days
    siguiente = proximo_mesiversario(FECHA_INICIO, hoy)
    faltan = (siguiente - hoy).days
    es_hoy = hoy.day == FECHA_INICIO.day

    # --- La canción del mes ---
    cancion = next((r for r in (medio("gone_gone_gone.mp3"),
                                medio("cancion.mp3")) if os.path.exists(r)), None)

    # --- Lluvia de pétalos de fondo ---
    petalos = ""
    for _ in range(22):
        petalos += (
            f'<div class="petalo" style="'
            f'left:{random.randint(0, 99)}vw;'
            f'animation-duration:{random.uniform(7, 13):.1f}s;'
            f'animation-delay:{random.uniform(0, 6):.1f}s;'
            f'font-size:{random.uniform(1.0, 2.0):.1f}rem;">'
            f'{random.choice(["🌸", "🌷", "💮", "🤍", "💖"])}</div>')
    st.markdown(petalos, unsafe_allow_html=True)

    # --- Tarjeta principal ---
    frase = ("Hoy se cumple otro mes, y otra vez me toca la mejor parte: seguir siendo tuyo."
             if es_hoy else
             "Cada mes celebro lo mismo: que sigues aquí, y que yo sigo eligiéndote.")

    st.markdown(f"""
    <div class="mes-hero">
        <p class="mes-hero__kicker">Hoy cumplimos un mes más</p>
        <p class="mes-hero__num">{meses}</p>
        <p class="mes-hero__label">{'meses juntos' if meses != 1 else 'mes juntos'}</p>
        <p class="mes-hero__frase">{frase}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Números del amor ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Días juntos", f"{dias_juntos:,}".replace(",", " "))
    col2.metric("Mesiversarios", meses)
    col3.metric("Próximo mes", "¡Es hoy! 🎉" if es_hoy else f"en {faltan} días")

    # --- Cuánto llevamos del mes en curso ---
    if not es_hoy:
        anterior = proximo_mesiversario(FECHA_INICIO, hoy - timedelta(days=32))
        total = (siguiente - anterior).days
        avance = max(0.0, min(1.0, (hoy - anterior).days / total))
        st.write(" ")
        st.progress(avance, text=f"Vamos {int(avance * 100)}% rumbo al mes {meses + 1} 💞")

    st.write("---")

    # --- La canción ---
    st.subheader("🎵 La canción de este mes")
    if cancion:
        es_gone = cancion.endswith("gone_gone_gone.mp3")
        st.caption("**Gone, Gone, Gone** — Phillip Phillips" if es_gone
                   else "La canción de siempre.")
        # autoplay + loop nativos de Streamlit: sirve el archivo tal cual,
        # sin incrustar megas de base64 en el HTML.
        st.audio(cancion, format="audio/mp3", loop=True, autoplay=True)
        arrancar_musica()
        if not es_gone:
            st.info("💿 Para que suene **Gone, Gone, Gone**, guarda el archivo como "
                    "`gone_gone_gone.mp3` en esta misma carpeta. La página lo toma sola.")
    else:
        st.info("💿 Guarda `gone_gone_gone.mp3` en esta carpeta y sonará aquí.")

    st.markdown(
        "> *«Like a drum, baby, don't stop beating…»*  \n"
        "> Porque eso haces tú: mantienes el ritmo de todo esto.")

    st.write("---")

    # --- Carta del mes ---
    st.subheader("💌 Lo que quiero decirte este mes")
    st.markdown(f"""
    <div class="carta">
    <strong>MI PANDITA,</strong><br><br>
    Otro mes que se nos pasó volando y que, sin embargo, alcanzó para
    muchísimo. {meses} meses ya, y todavía se me hace raro lo fácil que es
    quererte 🤍.<br><br>
    No sé en qué momento lo cotidiano contigo se volvió mi parte favorita del
    día: hablarte, contarte tonterías, saber que estás. Eso no lo planeé, pero
    lo cuido con todo.<br><br>
    Gracias por {dias_juntos} días de aguantarme, de cuidarme y de hacerme reír
    cuando menos ganas tenía. Vamos por el mes {meses + 1}, y por todos los que
    vengan 🐼.<br><br>
    <em>Tuyo, hoy y el mes que viene.</em>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # --- Razón del mes ---
    st.subheader("🎁 Las cajitas del mes")
    st.caption("Nueve cajitas, nueve cosas que quiero decirte. "
               "Ábrelas cuando quieras, no hay prisa.")

    REGALITOS = [
        "Tu risa me arregla el día.",
        "Contigo lo aburrido se vuelve plan.",
        "Me haces sentir seguro, siempre.",
        "Mi lugar favorito eres tú.",
        "Me sigues eligiendo, mes tras mes.",
        "Serendipia tiene tu cara.",
        "Tu abrazo apaga los días malos.",
        "Contigo no finjo nada.",
        "Me escuchas aunque no diga nada coherente.",
    ]

    # El reparto se baraja una vez por sesión: cada cajita guarda otra cosa.
    if "cajitas_orden" not in st.session_state:
        st.session_state.cajitas_orden = random.sample(range(len(REGALITOS)),
                                                       len(REGALITOS))
        st.session_state.cajitas_abiertas = []

    abiertas = st.session_state.cajitas_abiertas

    with st.container(key="cajitas"):
        for fila in range(3):
            columnas = st.columns(3)
            for c in range(3):
                i = fila * 3 + c
                with columnas[c]:
                    if i in abiertas:
                        mensaje = REGALITOS[st.session_state.cajitas_orden[i]]
                        st.markdown(f'<div class="cajita-abierta">{mensaje}</div>',
                                    unsafe_allow_html=True)
                    elif st.button("🎁", key=f"caja_{i}", width="stretch"):
                        abiertas.append(i)
                        st.rerun()

    total = len(REGALITOS)
    st.write(" ")
    st.progress(len(abiertas) / total,
                text=f"{len(abiertas)} de {total} cajitas abiertas")

    if len(abiertas) == total:
        st.markdown(f"""
        <div class="cajita-final">
            <p class="cajita-final__t">Las abriste todas 🤍</p>
            <p class="cajita-final__p">Y aun así se me quedaron cosas por decir.
            Para eso tenemos el mes {meses + 1}, y el siguiente, y el siguiente.</p>
        </div>
        """, unsafe_allow_html=True)
        lluvia_de_corazones()
        st.balloons()

    if abiertas:
        if st.button("Cerrarlas y empezar de nuevo ↺", key="reiniciar_cajitas"):
            st.session_state.cajitas_orden = random.sample(range(total), total)
            st.session_state.cajitas_abiertas = []
            st.rerun()

    st.write("---")

    # --- Nuestro recorrido ---
    st.subheader("🗓️ Nuestro recorrido")
    hitos = [
        (f"{FECHA_INICIO.strftime('%d/%m/%Y')}", "El día uno. Mi mejor hallazgo."),
        ("Mes 3", "Ya no había vuelta atrás."),
        ("Mes 12", "Un año entero, y sabía a poco."),
        (f"Mes {meses}", "Hoy. Y sigo aquí, feliz."),
    ]
    for i, (cuando, que) in enumerate(hitos):
        if cuando.startswith("Mes ") and int(cuando.split()[1]) > meses:
            continue
        st.markdown(
            f'<div class="hito" style="animation-delay:{i * .12:.2f}s">'
            f'<b>{cuando}</b> — {que}</div>',
            unsafe_allow_html=True)

    if es_hoy:
        st.balloons()

# --- SECCIÓN 1: INICIO ---
elif opcion == "Inicio":
    st.title(f"¡Hola, mi {random.choice(['bb', 'bomboncito', 'pandita'])}! ❤️")

    # Imagen principal
    try:
        st.image(medio("portada.jpg"), caption="Tú y yo, siempre.", use_container_width=True)
    except:
        st.warning(
            "📌 (Aquí aparecerá la imagen 'portada.jpg' cuando la guardes en la carpeta)")

    st.write("---")

    # Contador de tiempo
    st.subheader("Tiempo recorriendo el mundo juntos")
    fecha_inicio = FECHA_INICIO
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
            st.image(medio("foto1.jpg"), caption="Momentos divertidos")
        except:
            st.info("Sube 'foto1.jpg'")

        try:
            st.image(medio("foto2.jpg"), caption="Ese día especial")
        except:
            st.info("Sube 'foto2.jpg'")

    with col2:
        try:
            st.image(medio("foto3.jpg"), caption="Mi lugar favorito eres tú")
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
        with open(medio("cancion.mp3"), "rb") as audio_file:
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
