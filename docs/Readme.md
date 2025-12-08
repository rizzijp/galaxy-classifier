# 🌌 GALAXY CLASSIFIER

**Proyecto:** Galaxy Classifier — Proof of Concept (PoC)  
**Autores:** Álvaro Martínez, Juan Pablo Rizzi, Rocío Ortiz, José Benegas, Sara Gil  
    **DEEP LEARNING Y PRODUCTIVIZACIÓN**

---

## 1️⃣ Resumen del proyecto

Galaxy Classifier es una **PoC** de productivización de un modelo de clasificación morfológica de galaxias basado en imágenes del dataset **Galaxy10 DECaLS**.  

💡 **Objetivo:** mostrar el flujo completo desde el entrenamiento y validación de un modelo Deep Learning hasta su despliegue como **API REST (Flask)** en la nube con persistencia de predicciones en **PostgreSQL**.  

🔹 Se prioriza trazabilidad (git branching, PRs), endpoints REST completos y despliegue reproducible.  
🔹 La métrica final no es requisito; lo importante es la **pipeline completa**.

---

## 2️⃣ Estructura del repositorio

```
galaxy-classifier/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ requirements.txt
├─ .env.example
├─ src/
│  ├─ app.py                  # Flask app & endpoints
│  ├─ config.py
│  ├─ model/
│  │  ├─ model.py             # carga y wrapper del modelo (EfficientNetB0)
│  │  ├─ predict.py
│  ├─ db/
│  │  ├─ models.py            # SQLAlchemy models
│  │  ├─ migrations/          # (opcional) Alembic
│  ├─ utils/
│  │  ├─ preprocessing.py
│  │  ├─ dataset.py
│  └─ scripts/
│     ├─ train.ipynb      # Notebook de entrenamiento
│     ├─ eval.ipynb
│     ├─ prepare_data.ipynb
├─ notebooks/                 # Notebooks de pruebas / EDA
├─ docs/
│  ├─ architecture.png
│  └─ endpoint_documentation.md
├─ deployment/
│  ├─ Dockerfile
│  ├─ docker-compose.yml
│  └─ render.yaml (o notas de configuración)
└─ assets/
   └─ sample_images/
```
## 3️⃣ Instalación y ejecución local
**Requisitos:** Python 3.9+, PostgreSQL (local o remoto), Git  

**Instalación rápida (entorno virtual):**

git clone (https://github.com/rizzijp/galaxy-classifier)
cd galaxy-classifier
python -m venv .venv
source .venv/bin/activate # Linux / Mac
.venv\Scripts\activate # Windows
pip install -r requirements.txt
cp .env.example .env # Edita .env con las credenciales de BD y la ruta al modelo

## 4️⃣ Endpoints (documentación y ejemplos)
Todos los endpoints devuelven JSON y usan códigos HTTP estándar. Permite predicción individual o por lotes, auditoría de predicciones y gestión de la base de datos.

**POST /predict 🖼️**

Ejemplo de respuesta:
{
"predictions": [
{
"filename": "galaxy.jpg",
"predicted_class": "Spiral",
"confidence": 0.87,
"prediction_id": 123,
"timestamp": "2025-12-01T18:30:00Z"
}
]
}
**GET /predictions 📜**
**GET /predictions/<id> 🔍**
**DELETE /predictions/delete 🗑️**
**POST /reset_db ♻️**
**GET /health ✅**

## 5️⃣ Modelo — arquitectura y entrenamiento
Dataset: Galaxy10 DECaLS (~18.000 imágenes, 10 clases). Tamaño original 224×224. División: train/validation/test (70/15/15).  
Resize: 128×128 pruebas, 224×224 producción.  

Preprocesado: normalización, aumentación (rotaciones, flips, brillo/zoom), balanceo de clases (undersampling/oversampling).  

**Arquitectura:** EfficientNetB0 (transfer learning), últimas 100 capas descongeladas, dropout 0.3, FC: 256→128→64 (ReLU), salida: 10 clases (softmax), optimizador Adam 1e-5, loss sparse_categorical_crossentropy, métricas: accuracy, early stopping: patience=10.  

Artefacto final: `model.h5` (no subir al repo, usar almacenamiento externo).

---

## 6️⃣ Base de datos (PostgreSQL) 🐘
Tabla `predictions`:

CREATE TABLE predictions (
id SERIAL PRIMARY KEY,
filename TEXT,
predicted_class TEXT,
confidence REAL,
metadata JSONB,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## 7️⃣ Git: flujo de trabajo 🐙
Ramas: main, develop, release, hotfix, feature-*  

Flujo recomendado:

git checkout develop
git pull upstream develop
git checkout -b feature-<tu-nombre>
git add .
git commit -m "feat: agregar funcionalidad X"
git fetch upstream
git rebase upstream/develop
git push origin feature-<tu-nombre>

Crear PR a develop. Documentar capturas de PRs, resolución de conflictos y merges.

---

## 8️⃣ Despliegue en la nube ☁️
Ejemplo: Render (PaaS) para API Flask y PostgreSQL.  

Variables entorno: DATABASE_URL, MODEL_PATH, SECRET_KEY  
Startup command:

gunicorn -w 4 -b 0.0.0.0:$PORT src.app:app

Descargar modelo desde almacenamiento externo al iniciar, probar endpoints y grabar demo.

---

## 9️⃣ Docker (opcional) 🐳
Dockerfile:

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]

docker-compose.yml puede incluir servicios web y db para pruebas locales.

---

## 🔟 Notebooks, pruebas y métricas
- `train.ipynb`: pipeline entrenamiento y curvas  
- `eval.ipynb`: matriz de confusión, ejemplos de error  
- `inference_tests.ipynb`: pruebas unitarias  

Métrica principal PoC: accuracy + matriz de confusión.

---

## 📦 Entregables
- Repo GitHub completo  
- PDF explicativo con capturas  
- Notebooks (entrenamiento/evaluación/pruebas)  
- Scripts reproducibles (train.sh, predict.sh)  
- Presentación (PowerPoint/Streamlit)  
- Vídeo demo  
- Enlace al endpoint desplegado y credenciales demo

---

## ⚡ Ejecución end-to-end
1. Subir imagen a `/predict`  
2. API valida, preprocesa y predice  
3. Guarda registro en DB  
4. Devuelve JSON con predicted_class y confidence  
5. Consultar `/predictions` para historial

---

## 💡 Buenas prácticas
- No subir `.h5` al repo  
- Usar almacenamiento externo y variables de entorno  
- Tests unitarios básicos  
- Documentar `model_version` en metadata  
- Registrar experimentos (Weights & Biases / MLflow)

---

## 🤝 Cómo colaborar / PRs

git fetch upstream && git rebase upstream/develop

- Revisar tests locales  
- Describir cambios y pasos para probar en PR  
- Documentar aceptación/rechazo

---

## 🔗 Links y recursos
- Dataset: `docs/dataset.md`  
- Notebooks: `notebooks/`  
- Vídeo demo: `assets/demo.mp4`  
- Documentación endpoints: `docs/endpoint_documentation.md`

---

## ⚖️ Licencia y créditos
PoC académico, incluye EfficientNet, TensorFlow, etc. Licencia MIT o la que elijan.

---

## 👥 Contacto / Responsables
Álvaro Martínez — Coordinador / DevOps  
Juan Pablo Rizzi — Modelo / Entrenamiento  
Rocío Ortiz — Backend / API  
José Benegas — DB / Infra  
Sara Gil — Documentación / QA

---