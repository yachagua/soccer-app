import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Configuración inicial
st.set_page_config(page_title="SofaScore", layout="wide")

# Inicializar almacenamiento
if "eventos" not in st.session_state:
    st.session_state.eventos = pd.DataFrame(
        columns=["FechaHora", "Minuto", "Jugador", "Equipo", "Evento", "Observacion"]
    )

if "jugadores" not in st.session_state:
    st.session_state.jugadores = {}

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "⚽ Eventos"  # arrancar en eventos

if "observacion" not in st.session_state:
    st.session_state.observacion = ""  # valor inicial vacío

# --- Control de pestañas con radio ---
st.sidebar.title("📌 Navegación")
tab = st.sidebar.radio(
    "Ir a:", 
    ["👥 Nóminas", "⚽ Eventos"], 
    index=0 if st.session_state.active_tab == "👥 Nóminas" else 1
)
st.session_state.active_tab = tab

# --- TAB 1: Registrar nóminas ---
if st.session_state.active_tab == "👥 Nóminas":
    st.header("👥 Registrar equipos y jugadores")

    equipo = st.text_input("Nombre del equipo")
    jugador = st.text_input("Nombre del jugador")
    agregar = st.button("➕ Agregar jugador")

    if agregar and equipo and jugador:
        if equipo not in st.session_state.jugadores:
            st.session_state.jugadores[equipo] = []
        if jugador not in st.session_state.jugadores[equipo]:
            st.session_state.jugadores[equipo].append(jugador)
            st.success(f"Jugador {jugador} agregado al equipo {equipo}")

    if st.session_state.jugadores:
        st.subheader("📋 Nóminas registradas")
        for eq, jugadores in st.session_state.jugadores.items():
            st.write(f"**{eq}**: {', '.join(jugadores)}")
    else:
        st.info("No hay jugadores registrados todavía.")

# --- TAB 2: Registrar eventos ---
if st.session_state.active_tab == "⚽ Eventos":
    st.header("⚽ Registrar eventos del partido")

    evento = st.selectbox(
        "Evento",
        [
            "Comienza el encuentro","Asistencia","Balón Perdido","Duelo Ganado","Duelo Perdido","Falta cometida",
            "Falta recibida","Lesionado","Gol","Pase clave","Pase completado","Pase perdido","Recuperaciones",
            "Regate Exitoso","Regate Fallido","Tarjeta amarilla","Tarjeta roja","Tiro al arco",
            "Tiro desviado","Medio Tiempo","Finaliza el encuentro","Marcador Final"
        ]
    )

    minuto = st.number_input("Minuto", min_value=0, max_value=120, step=1)

    jugador, equipo = "", ""
    eventos_sin_jugador = ["Comienza el encuentro", "Medio Tiempo", "Finaliza el encuentro", "Marcador Final"]

    if evento not in eventos_sin_jugador and st.session_state.jugadores:
        equipo = st.selectbox("Equipo", options=list(st.session_state.jugadores.keys()))
        jugador = st.selectbox("Jugador", options=st.session_state.jugadores[equipo])

    # Observación ligada al session_state
    observacion = st.text_area(
        "Observación (opcional)",
        placeholder="Ej: tiro libre al ángulo, falta fuerte, golazo...",
        key="observacion"
    )

    # Función callback para guardar evento
    def guardar_evento():
        hora_colombia = datetime.now(pytz.timezone("America/Bogota")).strftime("%Y-%m-%d %H:%M:%S")
        nuevo_evento = {
            "FechaHora": hora_colombia,
            "Minuto": minuto,
            "Jugador": jugador,
            "Equipo": equipo,
            "Evento": evento,
            "Observacion": st.session_state.observacion
        }
        st.session_state.eventos = pd.concat(
            [st.session_state.eventos, pd.DataFrame([nuevo_evento])],
            ignore_index=True
        )
        st.success(f"Evento registrado: {evento} en el minuto {minuto}")
        st.session_state.active_tab = "⚽ Eventos"  # quedarse en eventos
        st.session_state.observacion = ""          # limpiar observación 👈

    st.button("➕ Guardar evento", on_click=guardar_evento)

    # --- Mostrar eventos ---
    st.subheader("📋 Eventos registrados")
    st.dataframe(st.session_state.eventos, use_container_width=True)

    # --- Estadísticas ---
    st.subheader("📊 Estadísticas por jugador")
    if not st.session_state.eventos.empty:
        stats = st.session_state.eventos.groupby(["Jugador", "Evento"]).size().unstack(fill_value=0)
        st.dataframe(stats, use_container_width=True)
    else:
        st.info("Aún no hay eventos registrados.")
