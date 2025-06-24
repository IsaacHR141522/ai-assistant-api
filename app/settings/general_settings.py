from pydantic_settings import BaseSettings

class GeneralSettings(BaseSettings):

    MODEL: str
    SYSTEM_PROMPT: str
    TEMPERATURE: float
    MAX_LENGHT: int
    TASK: str
    MONGO_URI: str 
    COLLECTION_HISTORY: str
    BASE_NAME: str 

    class Config:
        env_file = "app/env/general_settings.env"
