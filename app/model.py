from transformers import pipeline
from app.settings.general_settings import GeneralSettings
from pymongo import MongoClient
import uuid
from app.metrics_logger import get_metrics
import time

SETTINGS = GeneralSettings()

# Conexión a MongoDB
client = MongoClient(SETTINGS.MONGO_URI)
db = client[SETTINGS.BASE_NAME]
conversations_collection = db[SETTINGS.COLLECTION_HISTORY]
metrics_collection = db["metrics_history"]

# Cargar modelo desde HuggingFace
generator = pipeline(task=SETTINGS.TASK, model=SETTINGS.MODEL)

def create_conversation() -> str:
    conversation_id = str(uuid.uuid4())
    conversations_collection.insert_one({
        "conversation_id": conversation_id,
        "messages": []
    })
    return conversation_id

def generate_response(prompt: str, conversation_id: str) -> str:
    system_prompt = SETTINGS.SYSTEM_PROMPT

    # Buscar si ya existe la conversación
    conv = conversations_collection.find_one({"conversation_id": conversation_id})

    if not conv:
        conversations_collection.insert_one({
            "conversation_id": conversation_id,
            "messages": []
        })
        history = ""
    else:
        history = ""
        for msg in conv["messages"]:
            history += f"Usuario: {msg['prompt']}\nAsistente: {msg['response']}\n"

    # Construir el prompt con historial
    full_prompt = f"{system_prompt}\n{history}Usuario: {prompt}\nAsistente: "

    start_time = time.time()
    result = generator(
        full_prompt, 
        max_length=SETTINGS.MAX_LENGHT, 
        do_sample=True, 
        temperature=SETTINGS.TEMPERATURE
    )
    elapsed, cpu, mem, time_module = get_metrics(start_time)
    metrics_collection.insert_one({
        "elapsed_time": elapsed,
        "cpu_percent": cpu,
        "memory_percent": mem,
        "timestamp": time_module.time()
    })

    response_text = result[0]['generated_text'].replace(full_prompt, "").strip()

    # Guardar el nuevo mensaje
    conversations_collection.update_one(
        {"conversation_id": conversation_id},
        {"$push": {"messages": {"prompt": prompt, "response": response_text}}}
    )

    return response_text