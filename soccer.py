import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Configuración inicial
st.set_page_config(page_title="SofaScore", layout="wide")

# Zona horaria de Colombia
tz_colombia = pytz.timezone("America/Bogota")

# --- Entrada de datos ---
st.sidebar.header("Registrar evento")

evento = st.sidebar.selectbox(
    "Evento",
    [
        "Comienza el encuentro","Asistencia","Balón Perdido","Duelo Ganado","Duelo Perdido","Falta cometida","Falta recibida","Gol",
        "Pase clave","Pase completado","Pase perdido","Recuperaciones","Regate Exitoso","Regate Fallido",
        "Tarjeta amarilla","Tarjeta roja","Tiro al arco","Tiro desviado","Medio Tiempo","Finaliza el encuentro","Marcador Final"
    ]
)

minuto = st.sidebar.number_input("Minuto", min_value=0, max_value=120, step=1)

# Dependiendo del tipo de evento, habilitar/deshabilitar jugador/equipo
eventos_sin_jugador = ["Comienza el encuentro", "Medio Tiempo", "Finaliza el encuentro", "Marcador Final"]

if evento not in eventos_sin_jugador:
    jugador = st.sidebar.text_input("Jugador")
    equipo = st.sidebar.text_input("Equipo")
else:
    jugador = ""
    equipo = ""

guardar = st.sidebar.button("➕ Guardar evento")

# --- Almacenamiento de eventos ---
if "eventos" not in st.session_state:
    st.session_state.eventos = pd.DataFrame(columns=["Jugador","Evento","Minuto","Equipo","FechaHoraEvento"])

if guardar:
    fecha_hora_evento = datetime.now(tz_colombia).strftime("%Y-%m-%d %H:%M:%S")
    nuevo_evento = {
      "Jugador": jugador,
        "Evento": evento,
        "Minuto": minuto,
        "Equipo": equipo,
        "FechaHoraEvento": fecha_hora_evento
    }
    st.session_state.eventos = pd.concat(
        [st.session_state.eventos, pd.DataFrame([nuevo_evento])],
        ignore_index=True
    )
    st.success(f"✅ Evento registrado: {evento} - Min {minuto} - {jugador if jugador else 'N/A'} - {equipo if equipo else 'N/A'}")

# --- Mostrar tabla de eventos ---
st.subheader("📋 Eventos registrados")
st.dataframe(st.session_state.eventos, use_container_width=True)

# --- Estadísticas ---
st.subheader("📊 Estadísticas por jugador")
if not st.session_state.eventos.empty:
    stats = st.session_state.eventos.groupby(["Jugador", "Evento"]).size().unstack(fill_value=0)
    st.dataframe(stats, use_container_width=True)
else:
    st.info("Aún no hay eventos registrados.")
