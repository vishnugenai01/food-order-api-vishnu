from sqlalchemy.orm import Session
from fastapi import HTTPException
from dataaccess.repository.chat_messages import ChatMessageRepository

class ChatMessageLogic:
    def __init__(self, db: Session):
        self.db = db
        self.chat_message_repo = ChatMessageRepository(self.db)

    def save_message(self, user_id: str, role: str, content: str):
        try:
            db_result = self.chat_message_repo.save_message(
                user_id = user_id,
                role = role,
                content = content
            )
            
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_messages(self):
        try:
            db_result = self.chat_message_repo.get_messages()
            return db_result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        