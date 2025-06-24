# AI Assistant API

API REST construida con FastAPI que utiliza modelos LLM (Large Language Model) para responder preguntas sobre marketing digital y otros temas. Incluye endpoints para inicio de conversación, generación de respuestas y métricas básicas de uso.

---
## Comparacion de modelos 

* **distilgpt2** es un modelo de lenguaje general preentrenado en inglés, optimizado para ser ligero y rápido, pero no está especializado en español ni en tareas específicas de marketing digital. Su rendimiento en tareas en español o contextos específicos puede ser limitado, y tiende a generar respuestas menos relevantes o coherentes en otros idiomas, pero es una buena alternativa su idioma entrenado

* **datificate/gpt2-small-spanish** es una variante de GPT-2 entrenada específicamente para el idioma español. Esto le permite comprender mejor los matices, la gramática y el contexto cultural del español, generando respuestas más adecuadas y naturales para usuarios, se logra una mayor cpherencia ajustando el prompt en las variables de entorno.

* Ambos modelos pueden ejecutarse en CPU, pero los modelos entrenados en español, como datificate/gpt2-small-spanish , pueden requerir más recursos computacionales dependiendo de su tamaño y optimización. En tus métricas, se observa que el modelo en español utiliza más CPU, aunque menos memoria en comparación con distilgpt2. (se pueden ver sus metricas en la API)

* La selección del modelo se puede ajustar fácilmente desde las variables de entorno, permitiendo cambiar entre modelos sin modificar el código fuente. Para aplicaciones en español o dominios específicos, es preferible utilizar un modelo entrenado en ese idioma, como **datificate/gpt2-small-spanish** o **PlanTL-GOB-ES/gpt2-spanish**, si se requiere mayor calidad en las respuestas, se recomienda cargar un modelo más grande o especializado, siempre **considerando la capacidad de hardware disponible**.



## 🚀 Características

- Carga y sirve modelos LLM con Hugging Face Transformers.
- API REST lista para producción con documentación automática (Swagger UI).
- Soporta múltiples modelos: phi-2, distilgpt2, gpt-neo, Mistral, Falcon, Llama, etc.
- Métricas de uso (latencia, tokens, número de requests).
- Prompt pipeline para ingeniería de instrucciones básica.
- Ejemplo de uso CLI incluido.
- Docker listo para despliegue y compatibilidad multiplataforma.
- Historial de conversaciones persistente usando MongoDB, lo que permite almacenar, consultar y actualizar fácilmente los mensajes de cada usuario o sesión. 
---

## 📦 Requisitos

- Python 3.10 o superior
- pip
- (Opcional) Docker
- MongoDB

---

## ⚙️ Instalación local

```bash
# Clona el repositorio y entra al directorio
git clone <tu-repo>
cd <carpeta-del-proyecto>

# Crea un entorno virtual (opcional)
python -m venv venv

# Activa el entorno virtual
# En Windows
.\venv\Scripts\Activate.ps1 (recomendado)

# Instala dependencias
pip install -r requirements.txt

# Ejecuta el servidor FastAPI
uvicorn app.main:app --reload
```



## Carga en GitHub Codespaces

1. Abre el repositorio en GitHub y haz clic en el botón **"Code"** > **"Open with Codespaces"** > **"New codespace"**.
2. Espera a que Codespaces configure el entorno automáticamente.
3. Instala las dependencias (si no se instalan automáticamente):

```bash

# Instala dependencias
pip install -r requirements.txt

# Ejecuta el servidor FastAPI
python -m uvicorn app.main:app --reload

```

En GitHub Codespaces, el servidor se ejecuta dentro de un contenedor remoto, así que no puedes acceder directamente a http://127.0.0.1:8000 desde tu navegador local. Debes usar el reenvío de puertos que ofrece Codespaces.

1.- Cuando corres el servidor, Codespaces detecta que el puerto 8000 está en uso y te muestra un botón o enlace en la parte inferior o superior de VS Code (o en la interfaz web) para abrir el puerto en el navegador.
2.- Haz clic en ese enlace (usualmente dice algo como “Open in Browser” o “Abrir en navegador”).
3.- Se abrirá una URL similar a:

https://<tu-usuario>-<id>-8000.app.github.dev/docs

**¡Agrega /docs al final si no aparece automáticamente!**



---

## 🛠️ Variables de entorno

Configura tus variables de entorno en un archivo `.env` o en `app/settings/general_settings.py`:

- `MODEL`: Nombre del modelo Hugging Face a usar (ejemplo: `datificate/gpt2-small-spanish`)
- `SYSTEM_PROMPT`: Prompt inicial del sistema para las respuestas del asistente
- `TEMPERATURE`: Temperatura para la generación de texto (controla la creatividad, valor recomendado: 0.7)
- `MAX_LENGHT`: Longitud máxima de la respuesta generada (por ejemplo: 150)
- `TASK`: Tarea del pipeline de transformers (por ejemplo, `text-generation`)
- `MONGO_URI`: URI de conexión a MongoDB (ejemplo: `mongodb://localhost:27017/`)
- `COLLECTION_HISTORY`: Nombre de la colección para historial de conversaciones (ejemplo: `conversations`)
- `BASE_NAME`: Nombre de la base de datos en MongoDB (ejemplo: `ai_assistant_db`)

---

## 📚 Uso

Una vez iniciado el servidor, accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

### Ejemplo de endpoints principales

- **Iniciar conversación**
  ```
  POST /start_conversation
  ```

- **Generar respuesta**
  ```
  POST /generate
  ```

- **Obtener métricas**
  ```
  GET /metrics
  ```

---

## 📁 Estructura del proyecto

```
app/
├── __pycache__/
├── env/
│   └── general_settings.env
├── settings/
│   ├── __init__.py
│   └── general_settings.py
├── main.py
├── model.py
├── metrics_logger.py
├── schemas.py
venv/
Dockerfile
README.md
requirements.txt

```

---

## 🐳 Docker

Puedes construir y correr el proyecto con Docker:

```bash
docker build -t ai-assistant-api .
docker run -p 8000:8000 --env-file .env ai-assistant-api
```

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.