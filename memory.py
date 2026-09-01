from sqlalchemy.orm import Session
from models import ChatMessage

def save_message(db: Session, user_id: str, role: str, content: str):
    
    message = ChatMessage(
        user_id=user_id,
        role=role,
        content=content
    )
    
    db.add(message)
    db.commit() 

def get_messages(db: Session, user_id: str):
    
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.id)
        .all()
    )
    
    return messages