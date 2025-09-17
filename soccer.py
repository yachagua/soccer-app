import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="SofaScore", layout="wide")

# --- Entrada de datos ---
st.sidebar.header("Registrar evento")

jugador = st.sidebar.text_input("Jugador")
minuto = st.sidebar.number_input("Minuto", min_value=0, max_value=120, step=1)

evento = st.sidebar.selectbox(
    "Evento",
    [
        "Comienza el encuentro","Asistencia","Balón Perdido","Duelo Ganado","Duelo Perdido","Falta cometida","Falta recibida","Gol",
        "Pase clave","Pase completado","Pase perdido","Recuperaciones","Regate Exitoso","Regate Fallido",
        "Tarjeta amarilla","Tarjeta roja","Tiro al arco","Tiro desviado","Medio Tiempo","Finaliza el encuentro","Marcador Final"
    ]
)


equipo = st.sidebar.text_input("Equipo")
guardar = st.sidebar.button("➕ Guardar evento")

# --- Almacenamiento de eventos ---
if "eventos" not in st.session_state:
    st.session_state.eventos = pd.DataFrame(columns=["Minuto", "Jugador", "Equipo", "Evento"])

if guardar and jugador and equipo:
    nuevo_evento = {"Minuto": minuto, "Jugador": jugador, "Equipo": equipo, "Evento": evento}
    st.session_state.eventos = pd.concat(
        [st.session_state.eventos, pd.DataFrame([nuevo_evento])],
        ignore_index=True
    )
    st.success(f"Evento registrado: {jugador} - {evento} en el minuto {minuto}")

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
