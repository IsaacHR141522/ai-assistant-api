from fastapi import FastAPI, HTTPException
from app.schemas import PromptRequest, PromptResponse, StartConversationResponse
from app.model import generate_response, create_conversation
import time

app = FastAPI(title="AI Assistant API con Historial")

# Variable global para almacenar la última métrica
last_metrics = {}

@app.post("/start_conversation", response_model=StartConversationResponse)
def start_conversation():
    conversation_id = create_conversation()
    return StartConversationResponse(conversation_id=conversation_id)

@app.post("/generate", response_model=PromptResponse)
def generate(prompt: PromptRequest):
    start_time = time.time()
    try:
        response_text = generate_response(prompt.input_text, prompt.conversation_id)
        elapsed = time.time() - start_time
        import psutil
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        # Guarda las métricas en la variable global
        global last_metrics
        last_metrics = {
            "elapsed_time": elapsed,
            "cpu_percent": cpu,
            "memory_percent": mem
        }
        return PromptResponse(response=response_text)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/metrics")
def get_last_metrics():
    if not last_metrics:
        return {"detail": "No metrics available yet."}
    return last_metrics