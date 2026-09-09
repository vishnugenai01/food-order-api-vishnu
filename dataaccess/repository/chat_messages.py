from sqlalchemy.orm import Session
from dataaccess.models import ChatMessage

class ChatMessageRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def save_message(self, user_id: str, role: str, content: str):
        message = ChatMessage(user_id=user_id, role=role, content=content)
        
        self.db.add(message)
        self.db.commit() 
        self.db.refresh(message)
        return message

    def get_messages(self):
        return self.db.query(ChatMessage).all()