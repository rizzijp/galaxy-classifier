import streamlit as st
import requests
import pandas as pd
from PIL import Image
import os

# Obtener la ruta absoluta del directorio donde está ESTE archivo (ui.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta a la imagen uniendo las partes
image_path = os.path.join(current_dir, "assets", "galaxy.jpg")

# Leer variable de entorno, si no existe usa localhost (para pruebas sin docker)
API_URL = os.getenv("API_URL", "http://localhost:5000")
#API_URL = "https://galaxy-classifier-api.onrender.com" # Para pruebas en local



# --------------------------
# BANNER
# --------------------------
banner = Image.open(image_path)
st.image(
    banner,
    use_container_width=True
)

# Título superpuesto más arriba
st.markdown(
    """
    <h1 style="
        text-align: center;
        margin-top: -120px;     /* súbelo más o menos según necesites */
        color: white;
        text-shadow: 3px 3px 8px black;
        font-size: 3.2rem;
    ">
        Clasificador de Galaxias
    </h1>
    """,
    unsafe_allow_html=True)

# ====================================================================
# 1️⃣ SUBIR IMAGEN Y PREDECIR
# ====================================================================

st.header("🔭 Realizar predicción")

uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png"])

if st.button("Predecir"):
    if uploaded_file:
        # Mostrar imagen subida
        st.image(uploaded_file, caption="Imagen subida", width=300)

        uploaded_file.seek(0)
        bytes_data = uploaded_file.getvalue()

        files = {"image": (uploaded_file.name, bytes_data, uploaded_file.type)}
        resp = requests.post(f"{API_URL}/predict", files=files)

        if resp.status_code == 200:
            data = resp.json()
            st.success("Predicción exitosa")
            st.write(f"**Tipo de galaxia:** {data.get('label','desconocido')}")
            st.write(f"**Confianza:** {data.get('confidence','?')}")
            st.write(f"**ID predicción:** {data.get('id')}")
        
        else:
            st.error(f"Error en API: {resp.text}")

    else:
        st.error("Primero sube una imagen.")


st.write("---")


# ====================================================================
# 2️⃣ CONSULTAR TODAS LAS PREDICCIONES (TABLA)
# ====================================================================

st.header("📄 Ver todas las predicciones")

if st.button("Ver predicciones"):
    resp = requests.get(f"{API_URL}/predictions")
    if resp.status_code == 200:
        data = resp.json()

        # Convertir a tabla
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.error("No se pudieron obtener las predicciones")


st.write("---")


# ====================================================================
# 3️⃣ CONSULTAR POR ID
# ====================================================================

st.header("🔎 Buscar predicción por ID")

pred_id = st.number_input("ID:", min_value=1, step=1)

if st.button("Buscar por ID"):
    resp = requests.get(f"{API_URL}/predictions/{pred_id}")
    st.write(resp.json())


st.write("---")


# ====================================================================
# 4️⃣ CONSULTAR POR FILENAME
# ====================================================================

st.header("📁 Buscar predicción por nombre de archivo")

filename = st.text_input("Nombre del archivo (ej: galaxy_01.png)")

if st.button("Buscar por filename"):
    resp = requests.get(f"{API_URL}/predictions/filename/{filename}")
    if resp.status_code == 200:
        st.write(resp.json())
    else:
        st.error("Archivo no encontrado")


st.write("---")


# ====================================================================
# 5️⃣ RESET — BORRAR TODA LA BASE DE DATOS
# ====================================================================

st.header("🗑️ Resetear base de datos")

if st.button("Borrar todas las predicciones"):
    resp = requests.delete(f"{API_URL}/predictions/delete")

    if resp.status_code == 200:
        st.success("Base de datos vaciada")
        st.write(resp.json())
    else:
        st.error("Error al borrar los datos")