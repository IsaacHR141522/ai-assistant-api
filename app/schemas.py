from pydantic import BaseModel

class StartConversationResponse(BaseModel):
    conversation_id: str

class PromptRequest(BaseModel):
    conversation_id: str
    input_text: str

class PromptResponse(BaseModel):
    response: str

