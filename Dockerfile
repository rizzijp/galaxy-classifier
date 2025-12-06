# /Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar curl para bajar el modelo
RUN apt-get update && apt-get install -y curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# DESCARGA DEL MODELO (Hugging Face)
# Sustituye el enlace por el tuyo real de Hugging Face
RUN curl -L "ENLACE_DIRECTO_HUGGING_FACE" -o src/models/galaxy_cnn.pkl

# Exponer puerto interno
EXPOSE 10000

# Arrancar Flask con Gunicorn
CMD ["gunicorn", "src.api.app:app", "--bind", "0.0.0.0:10000"]