from pydantic import BaseModel

class ConversationInput(BaseModel):
    conversation_id: str
